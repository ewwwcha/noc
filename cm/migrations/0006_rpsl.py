# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# rpsl
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
        # Model 'RPSL'
        self.db.create_table(
            'cm_rpsl', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('repo_path', models.CharField("Repo Path", max_length=128, unique=True)),
                ('push_every', models.PositiveIntegerField("Push Every (secs)", default=86400, blank=True, null=True)),
                ('next_push', models.DateTimeField("Next Push", blank=True, null=True)),
                ('last_push', models.DateTimeField("Last Push", blank=True, null=True)),
                ('pull_every', models.PositiveIntegerField("Pull Every (secs)", default=86400, blank=True, null=True)),
                ('next_pull', models.DateTimeField("Next Pull", blank=True, null=True)),
                ('last_pull', models.DateTimeField("Last Pull", blank=True, null=True))
            )
        )
        # Mock Models
        RPSL = db.mock_model(
            model_name='RPSL', db_table='cm_rpsl', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField
        )
        ObjectCategory = db.mock_model(
            model_name='ObjectCategory',
            db_table='cm_objectcategory',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # M2M field 'RPSL.categories'
        self.db.create_table(
            'cm_rpsl_categories', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('rpsl', models.ForeignKey(RPSL, null=False)),
                ('objectcategory', models.ForeignKey(ObjectCategory, null=False))
            )
        )
