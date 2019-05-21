# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectselector pool
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration
from noc.core.model.fields import DocumentReferenceField


class Migration(BaseMigration):
    depends_on = [("main", "0055_default_pool")]

    def migrate(self):
        self.db.add_column("sa_managedobjectselector", "filter_pool", DocumentReferenceField("self", null=True, blank=True))
        self.db.create_index("sa_managedobjectselector", ["filter_pool"], unique=False, db_tablespace="")
