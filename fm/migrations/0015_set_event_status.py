# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# set event status
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db.execute("UPDATE fm_event SET status='U' WHERE subject IS NULL")
        db.execute(
            """UPDATE fm_event SET status='C' WHERE subject IS NOT NULL
               AND \"timestamp\"<('now'::timestamp-'1day'::interval)"""
        )
        db.execute(
            """UPDATE fm_event SET status='A' WHERE subject IS NOT NULL
               AND \"timestamp\">=('now'::timestamp-'1day'::interval)"""
        )
