# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# profile preview theme
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
            "main_userprofile",
            "preview_theme",
            models.CharField("Preview Theme", max_length=32, null=True, blank=True),
        )
