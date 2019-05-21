# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# remove zone_transfer_acl
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
        db.delete_column("dns_dnszoneprofile", "zone_transfer_acl")
