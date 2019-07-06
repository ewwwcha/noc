# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# unhandled exception
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        if (
            self.db.execute(
                "SELECT COUNT(*) FROM main_systemnotification WHERE name=%s",
                ["main.unhandled_exception"],
            )[0][0]
            == 0
        ):
            self.db.execute(
                "INSERT INTO main_systemnotification(name) VALUES(%s)", ["main.unhandled_exception"]
            )
