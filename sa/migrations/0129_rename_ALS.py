# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# rename ALS
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute("UPDATE sa_managedobject SET profile_name='Alsitec.7200' WHERE profile_name LIKE 'ALS.7200'")
