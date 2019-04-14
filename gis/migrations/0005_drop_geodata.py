# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# drop geodata
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
        db.execute("DROP TABLE IF EXISTS gis_geodata")

    def backwards(self):
        pass
