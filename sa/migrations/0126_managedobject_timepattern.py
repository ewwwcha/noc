# ----------------------------------------------------------------------
# managedobject time_pattern
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        TimePattern = db.mock_model(
            model_name="TimePattern",
            db_table="main_timepattern",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        self.db.add_column("sa_managedobject", "time_pattern", models.ForeignKey(TimePattern, null=True, blank=True))
