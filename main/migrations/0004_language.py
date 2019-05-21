# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# language
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
        # Model 'Language'
        db.create_table(
            'main_language', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField("Name", max_length=32, unique=True)),
                ('native_name', models.CharField("Native Name", max_length=32)),
                ('is_active', models.BooleanField("Is Active", default=False))
            )
        )
