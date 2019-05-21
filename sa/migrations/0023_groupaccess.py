# ----------------------------------------------------------------------
# group access
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
        # Adding model 'GroupAccess'
        Group = db.mock_model(model_name="Group", db_table="auth_group")
        ManagedObjectSelector = db.mock_model(model_name="ManagedObjectSelector", db_table="sa_managedobjectselector")
        self.db.create_table(
            'sa_groupaccess', (
                ('id', models.AutoField(primary_key=True)),
                ('group', models.ForeignKey(Group, verbose_name="Group")),
                ('selector', models.ForeignKey(ManagedObjectSelector, verbose_name="Object Selector")),
            )
        )
