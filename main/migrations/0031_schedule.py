# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# schedule
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

    depends_on = [
        ("sa", "0003_task_schedule"),
    ]

    def migrate(self):
        # TimePattern
        TimePattern = db.mock_model(
            model_name="TimePattern",
            db_table="main_timepattern",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        # Model "TaskSchedule"
        self.db.create_table(
            "main_schedule", (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("periodic_name", models.CharField("Periodic Task", max_length=64)),
                ("is_enabled", models.BooleanField("Enabled?", default=False)),
                ("time_pattern", models.ForeignKey(TimePattern, verbose_name="Time Pattern")),
                ("run_every", models.PositiveIntegerField("Run Every (secs)", default=86400)),
                ("timeout", models.PositiveIntegerField("Timeout (secs)", null=True, blank=True)),
                ("last_run", models.DateTimeField("Last Run", blank=True, null=True)),
                ("last_status", models.BooleanField("Last Status", default=True))
            )
        )
