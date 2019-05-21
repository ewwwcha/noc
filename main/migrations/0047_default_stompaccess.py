# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Default stomp users
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.nosql import get_db
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        s = get_db().noc.stomp_access
        if not s.count_documents({}):
            s.insert_one({"user": "noc", "password": "noc", "is_active": True})
