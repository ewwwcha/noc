# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# default activator
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db


class Migration(object):
    def forwards(self):
        if db.execute("SELECT COUNT(*) FROM sa_activator")[0][0] == 0:
            db.execute(
                "INSERT INTO sa_activator(name,ip,is_active,auth) VALUES('default','127.0.0.1',true,'xxxxxxxxxxx')"
            )

    def backwards(self):
        pass
