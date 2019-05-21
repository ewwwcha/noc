# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Initialize inventory hierarchy
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.lib.nosql import get_db
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db = get_db()
        # Initialize container models
        collection = db.noc.networksegments

        if collection.count_documents({}) == 0:
            collection.insert_one({"name": "ALL", "parent": None, "description": "All network", "settings": {}})
