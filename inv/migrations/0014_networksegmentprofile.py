# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Create default NetworkSegmentProfile
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
import bson
# NOC modules
from noc.lib.nosql import get_db
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db = get_db()
        coll = db["noc.networksegmentprofiles"]
        result = coll.insert_one(
            {
                "name": "default",
                "description": "Default segment profile",
                "discovery_interval": 0,
                "mac_restrict_to_management_vlan": False,
                "enable_lost_redundancy": True,
                "topology_methods": [
                    {
                        "method": m,
                        "is_active": True
                    } for m in ["oam", "lacp", "udld", "lldp", "cdp", "huawei_ndp", "stp", "nri"]
                ]
            }
        )
        if isinstance(result, bson.ObjectId):
            profile_id = result
        else:
            profile_id = result.inserted_id

        db["noc.networksegments"].update_many({}, {"$set": {"profile": profile_id}})
