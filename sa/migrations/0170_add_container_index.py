# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# add container index
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.create_index("sa_managedobject", ["container"], unique=False, db_tablespace="")
