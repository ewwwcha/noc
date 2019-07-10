#!./bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Write channel service
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from six.moves.urllib.parse import quote as urllib_quote

# NOC modules
from noc.config import config
from noc.core.backport.time import perf_counter


class Channel(object):
    def __init__(self, service, fields, address, db):
        """
        :param fields: <table>.<field1>. .. .<fieldN>
        :return:
        """
        self.name = fields
        self.service = service
        self.address = address
        self.db = db
        if "|" in fields:
            # New format. Separated by '|'.
            # Nested fields are possible
            parts = tuple(fields.split("|"))
        else:
            # Old format. Separated by '.'.
            # Nested fields are not possible
            parts = tuple(fields.split("."))
        self.sql = "INSERT INTO %s(%s) FORMAT TabSeparated" % (parts[0], ",".join(parts[1:]))
        self.encoded_sql = urllib_quote(self.sql.encode("utf8"))
        self.n = 0
        self.data = []
        self.last_updated = perf_counter()
        self.last_flushed = perf_counter()
        self.flushing = False
        self.url = "http://%s/?user=%s&password=%s&database=%s&query=%s" % (
            address,
            config.clickhouse.rw_user,
            config.clickhouse.rw_password or "",
            db,
            self.encoded_sql,
        )

    def feed(self, data):
        n = data.count("\n")
        self.n += n
        self.data += [data]
        return n

    def is_expired(self):
        if self.n:
            return False
        t = perf_counter()
        if self.data or self.flushing:
            return False
        return t - self.last_updated > config.chwriter.channel_expire_interval

    def is_ready(self):
        if not self.data or self.flushing:
            return False
        if self.n >= config.chwriter.batch_size:
            return True
        t = perf_counter()
        return (t - self.last_flushed) * 1000 >= config.chwriter.batch_delay_ms

    def get_data(self):
        self.n = 0
        data = "".join(self.data)
        self.data = []
        return data

    def start_flushing(self):
        self.flushing = True

    def stop_flushing(self):
        self.flushing = False
        self.last_flushed = perf_counter()

    def get_insert_sql(self):
        return self.sql

    def get_encoded_insert_sql(self):
        return self.encoded_sql
