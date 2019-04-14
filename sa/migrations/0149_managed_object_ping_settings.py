# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectprofile ping
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
            "sa_managedobjectprofile", "ping_policy",
            models.CharField(
                "Ping check policy",
                max_length=1,
                choices=[("f", "First Success"), ("a", "All Successes")],
                default="f"
            )
        )
        db.add_column("sa_managedobjectprofile", "ping_size", models.IntegerField("Ping packet size", default=64))
        db.add_column("sa_managedobjectprofile", "ping_count", models.IntegerField("Ping packets count", default=3))
        db.add_column(
            "sa_managedobjectprofile", "ping_timeout_ms", models.IntegerField("Ping timeout (ms)", default=1000)
        )

    def backwards(self):
        db.delete_column("sa_managedobjectprofile", "ping_policy")
        db.delete_column("sa_managedobjectprofile", "ping_size")
        db.delete_column("sa_managedobjectprofile", "ping_count")
        db.delete_column("sa_managedobjectprofile", "ping_timeout_ms")
