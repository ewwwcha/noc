# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobjectprofile udld
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    d_types = ["udld"]

    def migrate(self):
        for d in self.d_types:
            self.db.add_column("sa_managedobjectprofile", "enable_%s_discovery" % d, models.BooleanField("", default=True))
            self.db.add_column(
                "sa_managedobjectprofile", "%s_discovery_min_interval" % d, models.IntegerField("", default=600)
            )
            self.db.add_column(
                "sa_managedobjectprofile", "%s_discovery_max_interval" % d, models.IntegerField("", default=86400)
            )
