# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# metrics uploading
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import print_function
import argparse
import gzip
import os

# NOC modules
from noc.config import config
from noc.core.management.base import BaseCommand
from noc.core.service.shard import Sharder


class Command(BaseCommand):
    TOPIC = "chwriter"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="cmd")
        # load command
        load_parser = subparsers.add_parser("load")
        load_parser.add_argument("--fields", help="Data fields: <table>.<field1>.<fieldN>")
        load_parser.add_argument(
            "--chunk", type=int, default=config.nsqd.ch_chunk_size, help="Size on chunk"
        )
        load_parser.add_argument("--rm", action="store_true", help="Remove file after uploading")
        load_parser.add_argument("input", nargs=argparse.REMAINDER, help="Input files")

    def handle(self, cmd, *args, **options):
        return getattr(self, "handle_%s" % cmd)(*args, **options)

    def handle_load(self, fields, input, chunk, rm, *args, **kwargs):
        sharder = Sharder(fields, chunk=chunk)
        for fn in input:
            # Read data
            self.print("Reading file %s" % fn)
            if fn.endswith(".gz"):
                with gzip.GzipFile(fn) as f:
                    records = f.read().replace("\r", "").splitlines()
            else:
                with open(fn) as f:
                    records = f.read().replace("\r", "").splitlines()
            sharder.feed(records)
            self.print("    Publishing %d records" % len(records))
            sharder.pub()
            if rm:
                os.unlink(fn)


if __name__ == "__main__":
    Command().run()
