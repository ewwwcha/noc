# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# clean config
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):

    depends_on = (("sa", "0008_copy_objects"),)

    def migrate(self):
        db.execute("DROP INDEX cm_config_managed_object_id")
        db.execute("CREATE UNIQUE INDEX cm_config_managed_object_id ON cm_config(managed_object_id)")
        db.delete_column("cm_objectnotify", "category_id")
        db.delete_column("cm_objectnotify", "location_id")
        for column in ["activator_id", "profile_name", "scheme", "address", "port", "user", "password",
                       "super_password", "remote_path", "trap_source_ip", "trap_community"]:
            db.delete_column("cm_config", column)
        for table in ["cm_config", "cm_rpsl", "cm_dns", "cm_prefixlist"]:
            db.delete_column(table, "location_id")
            db.drop_table("%s_categories" % table)
        db.drop_table("cm_object_categories")
        db.drop_table("cm_objectaccess")
        db.execute("DELETE FROM cm_objectcategory")
        db.drop_table("cm_objectcategory")
        db.drop_table("cm_objectlocation")
