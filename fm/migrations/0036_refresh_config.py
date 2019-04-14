# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# refresh config
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Python modules
import datetime
# Third-party modules
from south.db import db


class Migration(object):
    def forwards(self):
        if db.execute("SELECT COUNT(*) FROM main_pyrule WHERE name=%s", ["refresh_config"])[0][0] == 0:
            db.execute(
                """INSERT INTO main_pyrule(name, interface, description, text, changed)
                       VALUES(%s, %s, %s, %s, %s)""", (
                    "refresh_config", "IEventTrigger", "stub", "@pyrule\ndef refresh_config(event):\n    pass",
                    datetime.datetime.now()
                )
            )
        r_id = db.execute("SELECT id FROM main_pyrule WHERE name = %s", ["refresh_config"])[0][0]
        db.execute(
            """INSERT INTO fm_eventtrigger(name, is_enabled, event_class_re, pyrule_id)
                   VALUES(%s, %s, %s, %s)
                   """, ["Refresh Config", True, r"Config \| Config Changed", r_id]
        )

    def backwards(self):
        pass
