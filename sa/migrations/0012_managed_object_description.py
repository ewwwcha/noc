# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobject description
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.rename_column("sa_managedobject", "location", "description")
