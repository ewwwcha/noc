# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# as name and routes maintainer
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    def forwards(self):
        db.add_column("peer_as", "as_name", models.CharField("AS Name", max_length=64, null=True, blank=True))
        Maintainer = db.mock_model(
            model_name='Maintainer',
            db_table='peer_maintainer',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        db.add_column(
            "peer_as", "routes_maintainer",
            models.ForeignKey(
                Maintainer, verbose_name="Routes Maintainer", null=True, blank=True, related_name="routes_maintainer"
            )
        )

    def backwards(self):
        db.delete_column("peer_as", "as_name")
        db.delete_column("peer_as", "routes_maintainer_id")
