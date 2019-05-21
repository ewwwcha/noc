# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Make VRF.vrf_group nullable
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.execute("ALTER TABLE ip_vrf ALTER vrf_group_id DROP NOT NULL")
