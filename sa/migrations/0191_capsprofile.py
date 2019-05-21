# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# CapsProfile
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import bson
# NOC modules
from noc.core.migration.base import BaseMigration
from noc.core.model.fields import DocumentReferenceField


class Migration(BaseMigration):
    def migrate(self):
        p_id = bson.ObjectId()
        self.mongo_db["capsprofiles"].insert_one(
            {
                "_id": p_id,
                "name": "default",
                "description": "Default Caps Profile",
                "enable_snmp": True,
                "enable_snmp_v1": True,
                "enable_snmp_v2c": True,
                "enable_l2": True,
                "bfd_policy": "E",
                "cdp_policy": "E",
                "fdp_policy": "E",
                "huawei_ndp_policy": "E",
                "lacp_policy": "E",
                "lldp_policy": "E",
                "oam_policy": "E",
                "rep_policy": "E",
                "stp_policy": "E",
                "udld_policy": "E",
                "enable_l3": True,
                "hsrp_policy": "E",
                "vrrp_policy": "E",
                "vrrpv3_policy": "E",
                "bgp_policy": "E",
                "ospf_policy": "E",
                "ospfv3_policy": "E",
                "isis_policy": "E",
                "ldp_policy": "E",
                "rsvp_policy": "E"
            }
        )
        # Create MOP.caps_profile field
        self.db.add_column(
            "sa_managedobjectprofile", "caps_profile", DocumentReferenceField("sa.CapsProfile", null=True, blank=True)
        )
        # Set default caps profile
        self.db.execute("UPDATE sa_managedobjectprofile SET caps_profile = %s", [str(p_id)])
        # Make field required
        self.db.execute("ALTER TABLE sa_managedobjectprofile ALTER caps_profile SET NOT NULL")
