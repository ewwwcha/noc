# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Create "default" VC domain, if not exists
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
        if db.execute("SELECT COUNT(*) FROM vc_vcdomain WHERE name=%s", ["default"])[0][0] == 0:
            db.execute("INSERT INTO vc_vcdomain(name,description) VALUES(%s,%s)", ["default", "Default VC Domain"])

    def backwards(self):
        pass
