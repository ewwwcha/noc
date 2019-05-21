# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Add CommandSnippet.ignore_cli_errors
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.add_column("sa_commandsnippet", "ignore_cli_errors", models.BooleanField("Ignore CLI errors", default=False))
