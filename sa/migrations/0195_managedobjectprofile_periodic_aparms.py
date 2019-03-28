# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
from south.db import db
from django.db import models


class Migration:
    def forwards(self):
        db.add_column(
            "sa_managedobjectprofile",
            "enable_periodic_discovery_alarms",
            models.BooleanField(default=False)
        )
        db.add_column(
            "sa_managedobjectprofile",
            "enable_box_discovery_alarms",
            models.BooleanField(default=False)
        )

    def backwards(self):
        pass
