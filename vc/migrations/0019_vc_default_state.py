# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Set .state
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db


class Migration(object):
    def forwards(self):
        # Get default resource state id
        r = db.execute("SELECT id FROM main_resourcestate WHERE is_default = true")
        if len(r) != 1:
            raise Exception("Cannot get default state")
        ds = r[0][0]
        # Set up default state
        db.execute("UPDATE vc_vc SET state_id = %s", [ds])

    def backwards(self):
        pass
