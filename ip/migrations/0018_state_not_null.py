# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Set .state NOT NULL
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.execute("ALTER TABLE ip_vrf ALTER state_id SET NOT NULL")
        db.execute("ALTER TABLE ip_prefix ALTER state_id SET NOT NULL")
        db.execute("ALTER TABLE ip_address ALTER state_id SET NOT NULL")
