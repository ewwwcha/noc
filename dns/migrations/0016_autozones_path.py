# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# autozones_path
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
        db.add_column(
            "dns_dnsserver", "autozones_path",
            models.CharField(
                "Autozones path", max_length=256, blank=True, null=True, default="autozones"
            )
        )

    def backwards(self):
        db.delete_column("dns_dnsserver", "autozones_path")
