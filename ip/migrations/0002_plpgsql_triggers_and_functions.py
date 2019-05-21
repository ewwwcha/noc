# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# plpgsql triggers and functions
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    depends_on = (("sa", "0002_trigger"),)

    def migrate(self):
        if not self.has_column("ip_ipv4block", "prefix_cidr"):
            self.db.execute("ALTER TABLE ip_ipv4block ADD prefix_cidr CIDR")
            self.db.execute("UPDATE ip_ipv4block SET prefix_cidr=prefix::cidr")
            self.db.execute("ALTER TABLE ip_ipv4block ALTER prefix_cidr SET NOT NULL")
            self.db.execute("CREATE INDEX x_ip_ipv4block_prefix_cidr ON ip_ipv4block(prefix_cidr)")
        if not self.has_column("ip_ipv4blockaccess", "prefix_cidr"):
            self.db.execute("ALTER TABLE ip_ipv4blockaccess ADD prefix_cidr CIDR")
            self.db.execute("UPDATE ip_ipv4blockaccess SET prefix_cidr=prefix::cidr")
            self.db.execute("ALTER TABLE ip_ipv4blockaccess ALTER prefix_cidr SET NOT NULL")
        self.db.execute(RAW_SQL_CREATE)
        if not self.has_trigger("ip_ipv4block", "t_ip_ipv4block_modify"):
            self.db.execute(t_ip_ipv4block_modify)
        if not self.has_trigger("ip_ipv4blockaccess", "t_ip_ipv4blockaccess_modify"):
            self.db.execute(t_ip_ipv4blockaccess_modify)

    def has_column(self, table, name):
        return self.db.execute(
            """SELECT COUNT(*)>0
            FROM pg_attribute a JOIN pg_class p ON (p.oid=a.attrelid)
            WHERE p.relname='%s'
              AND a.attname='%s'
            """ % (table, name)
        )[0][0]

    def has_trigger(self, table, name):
        return self.db.execute(
            """SELECT COUNT(*)>0
            FROM pg_trigger t JOIN pg_class p ON (p.oid=t.tgrelid)
            WHERE p.relname='%s'
              AND t.tgname='%s'""" % (table, name)
        )[0][0]


RAW_SQL_CREATE = """
CREATE OR REPLACE
FUNCTION ip_ipv4_block_depth(INTEGER,CIDR,CIDR)
RETURNS INTEGER
AS $$
DECLARE
    vrf         ALIAS FOR $1;
    inner_block ALIAS FOR $2;
    outer_block ALIAS FOR $3;
    c   INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO   c
    FROM ip_ipv4block
    WHERE vrf_id=vrf AND prefix_cidr >> inner_block AND prefix_cidr << outer_block;

    RETURN c;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE
FUNCTION ip_ipv4_block_depth_in_vrf_group(INTEGER,CIDR,CIDR)
RETURNS INTEGER
AS $$
DECLARE
    p_vrf_group_id ALIAS FOR $1;
    inner_block    ALIAS FOR $2;
    outer_block    ALIAS FOR $3;
    c   INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO   c
    FROM   ip_ipv4block b JOIN ip_vrf v ON (b.vrf_id=v.id)
    WHERE  v.vrf_group_id=p_vrf_group_id AND prefix_cidr >> inner_block AND prefix_cidr << outer_block;

    RETURN c;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE
FUNCTION hostname(TEXT)
RETURNS TEXT
AS $$
SELECT SUBSTRING($1 from E'^[a-zA-Z0-9\\-]+');
$$ LANGUAGE SQL IMMUTABLE;

CREATE OR REPLACE
FUNCTION domainname(TEXT)
RETURNS TEXT
AS $$
SELECT SUBSTRING($1 from E'^[a-zA-Z0-9\\-]+\\.(.+)');
$$ LANGUAGE SQL IMMUTABLE;

CREATE OR REPLACE
FUNCTION f_trigger_ip_ipv4block()
RETURNS TRIGGER
AS $$
BEGIN
    NEW.prefix_cidr:=NEW.prefix;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE
FUNCTION f_trigger_ip_ipv4blockaccess()
RETURNS TRIGGER
AS $$
BEGIN
    NEW.prefix_cidr:=NEW.prefix;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;"""

t_ip_ipv4block_modify = """
CREATE TRIGGER t_ip_ipv4block_modify
BEFORE INSERT OR UPDATE ON ip_ipv4block
FOR EACH ROW EXECUTE PROCEDURE f_trigger_ip_ipv4block();
"""

t_ip_ipv4blockaccess_modify = """
CREATE TRIGGER t_ip_ipv4blockaccess_modify
BEFORE INSERT OR UPDATE ON ip_ipv4blockaccess
FOR EACH ROW EXECUTE PROCEDURE f_trigger_ip_ipv4blockaccess();
"""
