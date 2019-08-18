# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# AlarmLog model
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import DateTimeField, StringField
import six


@six.python_2_unicode_compatible
class AlarmLog(EmbeddedDocument):
    meta = {"strict": False, "auto_create_index": False}
    timestamp = DateTimeField()
    from_status = StringField(max_length=1, regex=r"^[AC]$", required=True)
    to_status = StringField(max_length=1, regex=r"^[AC]$", required=True)
    message = StringField()

    def __str__(self):
        return "%s [%s -> %s]: %s" % (
            self.timestamp,
            self.from_status,
            self.to_status,
            self.message,
        )
