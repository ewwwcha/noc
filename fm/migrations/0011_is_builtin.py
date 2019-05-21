# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Add EventClass.is_builtin and EventClassificationRule.is_builtin
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.add_column("fm_eventclass", "is_builtin", models.BooleanField("Is Builtin", default=False))
        db.add_column("fm_eventclassificationrule", "is_builtin", models.BooleanField("Is Builtin", default=False))
