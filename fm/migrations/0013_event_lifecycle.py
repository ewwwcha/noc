# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# event lifecycle
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
        Event = db.mock_model(
            model_name='Event',
            db_table='fm_event',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        db.add_column("fm_event", "status", models.CharField("Status", max_length=1, default="U"))
        db.add_column("fm_event", "active_till", models.DateTimeField("Active Till", blank=True, null=True))
        db.add_column("fm_event", "close_timestamp", models.DateTimeField("Close Timestamp", blank=True, null=True))
        db.add_column("fm_event", "root", models.ForeignKey(Event, blank=True, null=True))
