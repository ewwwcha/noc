# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectselector drop repo_path
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.drop_column("sa_managedobjectselector", "filter_repo_path")
