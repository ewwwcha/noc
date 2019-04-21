# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Custom field types
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import ujson
import psycopg2
from psycopg2.extras import Json
from django.db import models
from django.core import exceptions
from six.moves.cPickle import loads, dumps, HIGHEST_PROTOCOL
import six
from bson import ObjectId
# NOC Modules
from noc.core.ip import IP
from noc.sa.interfaces.base import MACAddressParameter


class CIDRField(models.Field):
    """
    CIDRField maps to PostgreSQL CIDR
    """

    def __init__(self, *args, **kwargs):
        super(CIDRField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return "CIDR"

    def to_python(self, value):
        return str(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Convert value to pure network address to prevent
        # PostgreSQL exception
        return IP.prefix(value).first.prefix


class INETField(models.Field):
    """
    INETField maps to PostgreSQL INET Field
    """

    def db_type(self, connection):
        return "INET"

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return None
        return value


class MACField(models.Field):
    """
    MACField maps to the PostgreSQL MACADDR field
    """
    def db_type(self, connection):
        return "MACADDR"

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return value.upper()

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return None
        return MACAddressParameter().clean(value)


class BinaryField(models.Field):
    """
    Binary Field maps to PostgreSQL BYTEA
    """

    def db_type(self, connection):
        return "BYTEA"


class TextArrayField(models.Field):
    """
    Text Array field maps to PostgreSQL TEXT[] type
    """
    def db_type(self, connection):
        return "TEXT[]"

    def from_db_value(self, value, expression, connection, context):
        def to_unicode(s):
            if isinstance(s, unicode):
                return s
            else:
                return unicode(s, "utf-8")

        if value is None:
            return None
        return [to_unicode(x) for x in value]

    def get_default(self):
        if self.has_default():
            r = []
            for v in self.default:
                r += ["\"%s\"" % v.replace("\\", "\\\\").replace("\"", "\"\"")]
            return "{%s}" % ",".join(r)
        return ""


class InetArrayField(models.Field):
    """
    INETArrayField maps to PostgreSQL INET[] type
    """
    def db_type(self, connection):
        return "INET[]"

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, list):
            return value
        elif value == "{}":
            return []
        elif value is None:
            return None
        return value[1:-1].split(",")

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return "{ " + ", ".join(value) + " }"


class PickledField(models.Field):
    """
    Pickled object
    """
    def db_type(self, connection):
        return "BYTEA"

    def from_db_value(self, value, expression, connection, context):
        # if not value:
        #    return None
        try:
            return loads(str(value))
        except Exception:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        return psycopg2.Binary(dumps(value, HIGHEST_PROTOCOL))


class AutoCompleteTagsField(models.Field):
    """
    Autocomplete tags fields
    """
    def db_type(self, connection):
        return "TEXT"


class TagsField(models.Field):
    def db_type(self, connection):
        return "TEXT[]"

    def from_db_value(self, value, expression, connection, context):
        def to_unicode(s):
            if isinstance(s, unicode):
                return s
            return unicode(s, "utf-8")

        if value is None:
            return None
        elif isinstance(value, six.string_types):
            # Legacy AutoCompleteTagsField tweak
            if "," in value:
                value = value.split(",")
            value = [to_unicode(x) for x in value]
            return [x for x in value if x]
        else:
            return [to_unicode(x) for x in value]

    def get_db_prep_value(self, value, connection, prepared=False):
        return value


class DocumentReferenceDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.cache_name = field.get_cache_name()
        self.raw_name = field.raw_name
        self.has_get_by_id = hasattr(self.field.document, "get_by_id")

    def is_cached(self, instance):
        return hasattr(instance, self.cache_name)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        try:
            # Try already resolved value
            return getattr(instance, self.cache_name)
        except AttributeError:
            val = getattr(instance, self.raw_name)
            if val is None:
                # If NULL is an allowed value, return it.
                if self.field.null:
                    return None
                raise self.field.document.DoesNotExist()
            if self.has_get_by_id:
                rel_obj = self.field.document.get_by_id(val)
                if not rel_obj:
                    raise self.field.document.DoesNotExist()
            else:
                rel_obj = self.field.document.objects.get(id=val)
            setattr(instance, self.cache_name, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError(
                "%s must be accessed via instance" % self.field.name)
        # If null=True, we can assign null here, but otherwise the value needs
        # to be an instance of the related class.
        if value is None and self.field.null is False:
            raise ValueError(
                "Cannot assign None: \"%s.%s\" does not allow null values." % (
                    instance._meta.object_name, self.field.name)
            )
        elif value is not None and not isinstance(value, (self.field.document, six.string_types)):
            raise ValueError(
                "Cannot assign \"%r\": \"%s.%s\" must be a \"%s\" instance." % (
                    value, instance._meta.object_name,
                    self.field.name, self.field.document))
        elif value and isinstance(value, self.field.document):
            # Save to cache
            setattr(instance, self.cache_name, value)
            value = str(value.id)
        setattr(instance, self.raw_name, value)


class DocumentReferenceField(models.Field):
    def __init__(self, document, *args, **kwargs):
        self.document = document
        super(DocumentReferenceField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(DocumentReferenceField, self).contribute_to_class(cls,
                                                                name)
        self.raw_name = name + "_raw"
        setattr(cls, self.name, DocumentReferenceDescriptor(self))

    def db_type(self, connection):
        return "CHAR(24)"

    def get_prep_value(self, value):
        if value is None:
            return None
        elif isinstance(value, six.string_types):
            return value
        elif isinstance(value, ObjectId):
            return str(value)
        else:
            # Dereference
            # @todo: Maybe .pk is better way
            return str(value.id)


class CachedForeignKeyDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.cache_name = "_%s" % field.get_cache_name()

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.cache_name)
        except AttributeError:
            pass
        val = getattr(instance, self.field.attname)
        if val is None:
            raise AttributeError
        v = self.field.rel.to.get_by_id(val)
        if v is not None:
            setattr(instance, self.cache_name, v)
            return v
        raise AttributeError

    def __set__(self, instance, value):
        setattr(instance, self.cache_name, value)


class CachedForeignKey(models.ForeignKey):
    def contribute_to_class(self, cls, name):
        super(CachedForeignKey, self).contribute_to_class(cls, name)
        setattr(cls, self.get_cache_name(),
                CachedForeignKeyDescriptor(self))


class ObjectIDArrayField(models.Field):
    """
    ObjectIDArrayField maps to PostgreSQL CHAR[] type
    """
    def db_type(self, connection):
        return "CHAR(24)[]"

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, list):
            return value
        elif value == "{}":
            return []
        elif value is None:
            return None
        return value[1:-1].split(",")

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if isinstance(value, (six.string_types, ObjectId)):
            value = [value]
        return "{ %s }" % ", ".join(str(x) for x in value)

class JSONField(models.Field):
    empty_strings_allowed = False
    description = 'A JSON object'
    default_error_messages = {
        'invalid': "Value must be valid JSON.",
    }
    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        return 'jsonb'

    # def get_transform(self, name):
    #     transform = super(JSONField, self).get_transform(name)
    #     if transform:
    #         return transform
    #     return KeyTransformFactory(name)

    def get_prep_value(self, value):
        if value is not None:
            return psycopg2.extras.Json(value)
        return value

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('has_key', 'has_keys', 'has_any_keys'):
            return value
        if isinstance(value, (dict, list)):
            return Json(value)
        return super(JSONField, self).get_prep_lookup(lookup_type, value)

    def validate(self, value, model_instance):
        super(JSONField, self).validate(value, model_instance)
        try:
            ujson.dumps(value)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': JSONField}
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)
