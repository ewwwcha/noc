# ----------------------------------------------------------------------
# managedobject rules
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
        PyRule = db.mock_model(
            model_name="PyRule",
            db_table="main_pyrule",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        self.db.add_column(
            "sa_managedobject", "config_filter_rule",
            models.ForeignKey(PyRule, verbose_name="Config Filter pyRule", null=True, blank=True)
        )
        self.db.add_column(
            "sa_managedobject", "config_validation_rule",
            models.ForeignKey(PyRule, verbose_name="Config Validation pyRule", null=True, blank=True)
        )
