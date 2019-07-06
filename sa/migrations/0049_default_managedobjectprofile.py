# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# default managedobjectprofile
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute(
            """
        INSERT INTO sa_managedobjectprofile(name)
        VALUES('default')
        """
        )
