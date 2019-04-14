# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectprofile topology discovery
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------
"""
"""
# Third-party modules
from south.db import db
from django.db import models


class Migration(object):
    d_types = ["lldp", "cdp", "fdp", "stp"]

    def forwards(self):
        for d in self.d_types:
            db.add_column("sa_managedobjectprofile", "enable_%s_discovery" % d, models.BooleanField("", default=True))
            db.add_column(
                "sa_managedobjectprofile", "%s_discovery_min_interval" % d, models.IntegerField("", default=600)
            )
            db.add_column(
                "sa_managedobjectprofile", "%s_discovery_max_interval" % d, models.IntegerField("", default=86400)
            )

    def backwards(self):
        for d in self.d_types:
            db.delete_column("sa_managedobjectprofile", "enable_%s_discovery" % d)
            db.delete_column("sa_managedobjectprofile", "%s_discovery_min_interval" % d)
            db.delete_column("sa_managedobjectprofile", "%s_discovery_max_interval" % d)
