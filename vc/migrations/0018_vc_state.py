# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# VRF, Prefix, IP state
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Third-party modules
from django.db import models
from south.db import db


class Migration(object):
    depends_on = (("main", "0043_default_resourcestates"),)

    def forwards(self):
        # Create .state
        ResourceState = db.mock_model(
            model_name="ResourceState",
            db_table="main_resourcestate",
            db_tablespace="",
            pk_field_name="id",
            pk_field_type=models.AutoField
        )
        db.add_column("vc_vc", "state", models.ForeignKey(ResourceState, verbose_name="State", null=True, blank=True))

    def backwards(self):
        db.drop_column("vc_vc", "state_id")
