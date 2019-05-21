# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnsserver ip
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------


# Third-party modules
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        self.db.add_column("dns_dnsserver", "ip", models.IPAddressField("IP", null=True, blank=True))
