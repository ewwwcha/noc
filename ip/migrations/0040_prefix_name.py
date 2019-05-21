# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Prefix.name
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
        self.db.add_column("ip_prefix", "name", models.CharField("Name", max_length=255, null=True, blank=True))
