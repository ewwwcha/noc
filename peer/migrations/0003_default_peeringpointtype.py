# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# default peeringpointtype
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db

LEGACY = [
    ("Cisco", "Cisco.IOS"),
    ("Juniper", "Juniper.JUNOS"),
    ("IOS", "Cisco.IOS"),
    ("JUNOS", "Juniper.JUNOS"),
]
TYPES = ["Cisco.IOS", "Juniper.JUNOS"]


class Migration(object):
    def forwards(self):
        for f, t in LEGACY:
            db.execute("UPDATE peer_peeringpointtype SET name=%s WHERE name=%s", [t, f])
        for t in TYPES:
            if db.execute("SELECT COUNT(*) FROM peer_peeringpointtype WHERE name=%s", [t])[0][0] == 0:
                db.execute("INSERT INTO peer_peeringpointtype(name) VALUES(%s)", [t])

    def backwards(self):
        for f, t in LEGACY:
            db.execute("UPDATE peer_peeringpointtype SET name=%s WHERE name=%s", [t, f])
