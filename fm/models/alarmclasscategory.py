# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# FM module database models
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import six

# NOC modules
import noc.lib.nosql as nosql


@six.python_2_unicode_compatible
class AlarmClassCategory(nosql.Document):
    meta = {
        "collection": "noc.alartmclasscategories",  # @todo: Fix bug
        "strict": False,
        "auto_create_index": False,
    }
    name = nosql.StringField()
    parent = nosql.ObjectIdField(required=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if " | " in self.name:
            p_name = " | ".join(self.name.split(" | ")[:-1])
            p = AlarmClassCategory.objects.filter(name=p_name).first()
            if not p:
                p = AlarmClassCategory(name=p_name)
                p.save()
            self.parent = p.id
        else:
            self.parent = None
        super(AlarmClassCategory, self).save(*args, **kwargs)
