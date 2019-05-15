# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Approved handlers
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from threading import Lock
import operator
# Third-party modules
import six
from mongoengine.document import Document
from mongoengine.fields import StringField, BooleanField
import cachetools
# NOC modules
from noc.core.model.decorator import on_delete_check
from noc.core.handler import get_handler

id_lock = Lock()


@on_delete_check(check=[
    ("sa.ManagedObjectProfile", "resolver_handler")
])
@six.python_2_unicode_compatible
class Handler(Document):
    meta = {
        "collection": "handlers",
        "strict": False,
        "auto_create_index": False,
    }

    handler = StringField(primary_key=True)
    name = StringField()
    description = StringField()
    allow_config_filter = BooleanField()
    allow_config_validation = BooleanField()
    allow_config_diff = BooleanField()
    allow_config_diff_filter = BooleanField()
    allow_housekeeping = BooleanField()
    allow_resolver = BooleanField()
    allow_threshold = BooleanField()

    _id_cache = cachetools.TTLCache(maxsize=1000, ttl=60)

    def __str__(self):
        return self.name

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_id_cache"), lock=lambda _: id_lock)
    def get_by_id(cls, id):
        return Handler.objects.filter(handler=id).first()

    def get_handler(self):
        return get_handler(self.handler)
