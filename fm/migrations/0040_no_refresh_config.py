# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# no refresh config
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
        DELETE FROM fm_eventtrigger
        WHERE pyrule_id IN (
            SELECT id FROM main_pyrule WHERE name = 'refresh_config'
        )
        """
        )
