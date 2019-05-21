# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# time pattern
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
        # Model 'TimePattern'
        self.db.create_table(
            'main_timepattern', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField("Name", max_length=64, unique=True)),
                ('description', models.TextField("Description", null=True, blank=True))
            )
        )

        # Mock Models
        TimePattern = self.db.mock_model(
            model_name='TimePattern',
            db_table='main_timepattern',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # Model 'TimePatternTerm'
        self.db.create_table(
            'main_timepatternterm', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('time_pattern', models.ForeignKey(TimePattern, verbose_name="Time Pattern")),
                ('term', models.CharField("Term", max_length=256))
            )
        )
        self.db.create_index('main_timepatternterm', ['time_pattern_id', 'term'], unique=True)
