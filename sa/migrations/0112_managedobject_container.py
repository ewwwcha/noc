# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# managedobject container
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration
from noc.core.model.fields import DocumentReferenceField


class Migration(BaseMigration):
    def migrate(self):
        self.db.add_column("sa_managedobject", "container", DocumentReferenceField("self", null=True, blank=True))
