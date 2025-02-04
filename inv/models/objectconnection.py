# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ObjectConnection model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import six
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    DictField,
    ListField,
    EmbeddedDocumentField,
    LineStringField,
    ReferenceField,
)
import geojson

# NOC modules
from noc.inv.models.object import Object
from noc.core.mongo.fields import PlainReferenceField
from noc.gis.models.layer import Layer


@six.python_2_unicode_compatible
class ObjectConnectionItem(EmbeddedDocument):
    _meta = {"strict": False, "auto_create_index": False}
    # Object reference
    object = PlainReferenceField(Object)
    # Connection name
    name = StringField()

    def __str__(self):
        return "%s: %s" % (unicode(self.object), self.name)


@six.python_2_unicode_compatible
class ObjectConnection(Document):
    """
    Inventory object connections
    """

    meta = {
        "collection": "noc.objectconnections",
        "strict": False,
        "auto_create_index": False,
        "indexes": [("connection.object", "connection.name")],
    }

    # 2 or more items
    connection = ListField(EmbeddedDocumentField(ObjectConnectionItem))
    data = DictField()
    type = StringField(required=False)
    # Map
    layer = ReferenceField(Layer)
    line = LineStringField(auto_index=True)

    def __str__(self):
        return "<%s>" % ", ".join(unicode(c) for c in self.connection)

    def clean(self):
        self.set_line()

    def set_line(self):
        if not self.layer:
            return
        if len(self.connection) != 2:
            self.line = None
            return
        o1 = self.connection[0].object
        o2 = self.connection[1].object
        if o1.point and o2.point and o1.point["coordinates"] != o2.point["coordinates"]:
            self.line = geojson.LineString(
                coordinates=[o1.point["coordinates"], o2.point["coordinates"]]
            )

    def p2p_get_other(self, object):
        """
        Return other side
        as object, name
        """
        for c in self.connection:
            if c.object != object:
                return c.object, c.name
        return None, None
