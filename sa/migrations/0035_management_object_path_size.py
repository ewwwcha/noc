# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobject path size
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute("ALTER TABLE sa_managedobject ALTER remote_path TYPE VARCHAR(256)")
