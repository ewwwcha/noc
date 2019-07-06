# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobject coordinates
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db import models

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.add_column("sa_managedobject", "x", models.FloatField(null=True, blank=True))
        self.db.add_column("sa_managedobject", "y", models.FloatField(null=True, blank=True))
        self.db.add_column(
            "sa_managedobject", "default_zoom", models.IntegerField(null=True, blank=True)
        )
