# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Custom Field Enums
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
        # CustomFieldEnumGroup
        db.create_table(
            "main_customfieldenumgroup", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("name", models.CharField("Name", max_length=128, unique=True)),
                ("is_active", models.BooleanField("Is Active", default=True)),
                ("description", models.TextField("Description", null=True, blank=True))
            )
        )
        # CustomFieldEnumValue
        CustomFieldEnumGroup = db.mock_model(
            model_name="CustomFieldEnumGroup",
            db_table="main_customfieldenumgroup",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )

        db.create_table(
            "main_customfieldenumvalue", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("enum_group", models.ForeignKey(CustomFieldEnumGroup, verbose_name="Enum Group")),
                ("is_active", models.BooleanField("Is Active", default=True)),
                ("key", models.CharField("Key", max_length=256)), ("value", models.CharField("Value", max_length=256))
            )
        )
        # CustomField.enum_group
        db.add_column(
            "main_customfield", "enum_group",
            models.ForeignKey(CustomFieldEnumGroup, verbose_name="Enum Group", null=True, blank=True)
        )
