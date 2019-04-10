# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# remove old tables
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
        db.delete_table("fm_eventrepeat")
        db.delete_table("fm_eventlog")
        db.delete_table("fm_eventdata")
        db.delete_table("fm_event")
        db.delete_table("fm_mibdata")
        db.delete_table("fm_mibdependency")
        db.delete_table("fm_mib")
        db.delete_table("fm_eventpriority")
        db.delete_table("fm_eventpostprocessingre")
        db.delete_table("fm_eventpostprocessingrule")
        db.delete_table("fm_eventcorrelationmatchedvar")
        db.delete_table("fm_eventcorrelationmatchedclass")
        db.delete_table("fm_eventclassificationre")
        db.delete_table("fm_eventclassificationrule")
        db.delete_table("fm_eventclassvar")
        db.delete_table("fm_eventclass")
        db.delete_table("fm_eventcategory")

    def backwards(self):
        pass
