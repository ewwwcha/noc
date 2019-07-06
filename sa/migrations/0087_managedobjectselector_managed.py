# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectselector filter_managed
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
        self.db.add_column(
            "sa_managedobjectselector",
            "filter_managed",
            models.NullBooleanField("Filter by Is Managed", null=True, blank=True, default=True),
        )
