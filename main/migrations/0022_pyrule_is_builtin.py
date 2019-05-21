# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# pyrule is_builtin
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
        self.db.add_column("main_pyrule", "is_builtin", models.BooleanField("Is Builtin", default=False))
