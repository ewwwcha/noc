# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# trap source ip
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.add_column("cm_config", "trap_source_ip", models.IPAddressField("Trap Source IP", blank=True, null=True))
        db.add_column(
            "cm_config", "trap_community", models.CharField("Trap Community", blank=True, null=True, max_length=64)
        )
