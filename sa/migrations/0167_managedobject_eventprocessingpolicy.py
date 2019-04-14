# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ManagedObject.event_processing_policy
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    def forwards(self):
        # Profile settings
        db.add_column(
            "sa_managedobjectprofile", "event_processing_policy",
            models.CharField(
                "Event Processing Policy",
                max_length=1,
                choices=[("E", "Process Events"), ("D", "Drop events")],
                default="E"
            )
        )
        # Object settings
        db.add_column(
            "sa_managedobject", "event_processing_policy",
            models.CharField(
                "Event Processing Policy",
                max_length=1,
                choices=[("P", "Profile"), ("E", "Process Events"), ("D", "Drop events")],
                default="P"
            )
        )

    def backwards(self):
        db.delete_column("sa_managedobjectprofile", "event_processing_policy")
        db.delete_column("sa_managedobject", "event_processing_policy")
