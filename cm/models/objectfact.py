# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Object Facts
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import datetime

# Third-party modules
import six
from mongoengine.document import Document
from mongoengine.fields import StringField, DictField, DateTimeField, UUIDField

# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.core.mongo.fields import ForeignKeyField


@six.python_2_unicode_compatible
class ObjectFact(Document):
    meta = {
        "collection": "noc.objectfacts",
        "strict": False,
        "auto_create_index": False,
        "indexes": ["object", "attrs.rule"],
    }
    uuid = UUIDField(binary=True, primary_key=True)
    object = ForeignKeyField(ManagedObject)
    cls = StringField()
    label = StringField()
    attrs = DictField()
    introduced = DateTimeField(default=datetime.datetime.now)
    changed = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.object.name
