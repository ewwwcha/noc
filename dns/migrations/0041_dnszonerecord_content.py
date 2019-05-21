# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Enlarge DNSZoneRecord.content
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.execute("ALTER TABLE dns_dnszonerecord ALTER content TYPE VARCHAR(65536)")
