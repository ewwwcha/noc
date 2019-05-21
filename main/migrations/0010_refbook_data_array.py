# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# refbook data array
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.model.fields import TextArrayField
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):

        db.delete_table('main_refbookdata')

        # Mock Models
        RefBook = db.mock_model(
            model_name='RefBook',
            db_table='main_refbook',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # Model 'RefBookData'
        db.create_table(
            'main_refbookdata', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('ref_book', models.ForeignKey(RefBook, verbose_name="Ref Book")), ('value', TextArrayField("Value"))
            )
        )

        db.execute("UPDATE main_refbook SET next_update='now'")
