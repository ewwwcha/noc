# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# community
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party models
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        # Model 'CommunityType'
        self.db.create_table(
            'peer_communitytype', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField("Description", max_length=32, unique=True))
            )
        )

        # Mock Models
        CommunityType = db.mock_model(
            model_name='CommunityType',
            db_table='peer_communitytype',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # Model 'Community'
        self.db.create_table(
            'peer_community', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('community', models.CharField("Community", max_length=20, unique=True)),
                ('type', models.ForeignKey(CommunityType, verbose_name="Type")),
                ('description', models.CharField("Description", max_length=64))
            )
        )
