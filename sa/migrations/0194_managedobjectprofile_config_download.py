# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ManagedObjectProfile config download settings
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.model.fields import DocumentReferenceField


class Migration(object):
    def forwards(self):
        Template = db.mock_model(
            model_name='Template',
            db_table='main_template',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        db.add_column(
            "sa_managedobjectprofile", "config_download_storage",
            DocumentReferenceField("main.ExtStorage", null=True, blank=True)
        )
        db.add_column(
            "sa_managedobjectprofile", "config_download_template",
            models.ForeignKey(Template, verbose_name="Config download Template", blank=True, null=True)
        )
        db.add_column(
            "sa_managedobjectprofile", "config_policy",
            models.CharField(
                "Config download Policy",
                max_length=1,
                choices=[("s", "Script"), ("S", "Script, Download"), ("D", "Download, Script"), ("d", "Download")],
                default="s"
            )
        )
        db.add_column(
            "sa_managedobject", "config_policy",
            models.CharField(
                "Config download Policy",
                max_length=1,
                choices=[
                    ("P", "Profile"), ("s", "Script"), ("S", "Script, Download"), ("D", "Download, Script"),
                    ("d", "Download")
                ],
                default="P"
            )
        )

    def backwards(self):
        pass
