# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# no lg
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.delete_table('peer_lgquerycommand')
        self.db.delete_table('peer_lgquerytype')


