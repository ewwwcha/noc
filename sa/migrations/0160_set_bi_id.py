# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Initialize bi_id field
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from pymongo import UpdateOne
import bson

# NOC modules
from noc.core.migration.base import BaseMigration
from noc.core.bi.decorator import bi_hash

PG_CHUNK = 500
MONGO_CHUNK = 500


class Migration(BaseMigration):
    def migrate(self):
        MODELS = [
            "sa_administrativedomain",
            "sa_authprofile",
            "sa_managedobject",
            "sa_managedobjectprofile",
            "sa_terminationgroup",
        ]
        # Update postgresql tables
        for table in MODELS:
            rows = self.db.execute("SELECT id FROM %s WHERE bi_id IS NULL" % table)
            values = ["(%d, %d)" % (r[0], bi_hash(r[0])) for r in rows]
            while values:
                chunk, values = values[:PG_CHUNK], values[PG_CHUNK:]
                self.db.execute(
                    """
                    UPDATE %s AS t
                    SET
                      bi_id = c.bi_id
                    FROM (
                      VALUES
                      %s
                    ) AS c(id, bi_id)
                    WHERE c.id = t.id
                    """
                    % (table, ",\n".join(chunk))
                )
        # Update mongodb collections
        mdb = self.mongo_db
        for coll_name in ["noc.profiles", "noc.services", "noc.serviceprofiles"]:
            coll = mdb[coll_name]
            updates = []
            for d in coll.find({"bi_id": {"$exists": False}}, {"_id": 1}):
                updates += [
                    UpdateOne({"_id": d["_id"]}, {"$set": {"bi_id": bson.Int64(bi_hash(d["_id"]))}})
                ]
                if len(updates) >= MONGO_CHUNK:
                    coll.bulk_write(updates)
                    updates = []
            if updates:
                coll.bulk_write(updates)
        # Alter bi_id fields and create indexes
        for table in MODELS:
            self.db.execute("ALTER TABLE %s ALTER bi_id SET NOT NULL" % table)
            self.db.create_index(table, ["bi_id"], unique=True)
