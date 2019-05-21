# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# prefix table
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.model.fields import CIDRField
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.create_table(
            "main_prefixtable", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("name", models.CharField("Name", max_length=128, unique=True)),
                ("description", models.TextField("Description", null=True, blank=True)),
            )
        )

        PrefixTable = db.mock_model(
            model_name="PrefixTable",
            db_table="main_prefixtable",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )

        db.create_table(
            "main_prefixtableprefix", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("table", models.ForeignKey(PrefixTable, verbose_name="Prefix Table")),
                ("afi", models.CharField("Address Family", max_length=1, choices=[("4", "IPv4"), ("6", "IPv6")])),
                ("prefix", CIDRField("Prefix"))
            )
        )
