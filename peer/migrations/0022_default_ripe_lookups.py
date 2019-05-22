# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# default ripe lookups
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        if self.db.execute("SELECT COUNT(*) FROM peer_whoisdatabase WHERE name=%s", ["RIPE"])[0][0] == 0:
            self.db.execute("INSERT INTO peer_whoisdatabase(name) VALUES(%s)", ["RIPE"])
        ripe_id = self.db.execute("SELECT id FROM peer_whoisdatabase WHERE name=%s", ["RIPE"])[0][0]
        for url, direction, key, value in [("ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.as-set.gz", "F", "as-set",
                                            "members"), ("ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.route.gz", "R",
                                                         "origin", "route")]:
            self.db.execute(
                "INSERT INTO peer_whoislookup(whois_database_id,url,direction,key,value) values(%s,%s,%s,%s,%s)",
                [ripe_id, url, direction, key, value]
            )
