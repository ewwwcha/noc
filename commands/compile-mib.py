# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Compile loaded MIB to the compact JSON representation
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import sys
import os
import gzip
import argparse

# Third-party modules
import ujson
from mongoengine.errors import DoesNotExist

# NOC modules
from noc.core.management.base import BaseCommand
from noc.core.mongo.connection import connect
from noc.fm.models.mib import MIB
from noc.fm.models.mibdata import MIBData


class Command(BaseCommand):
    help = "Compile loaded MIB to compact JSON form"

    def add_arguments(self, parser):
        parser.add_argument("-o", "--output", dest="output", default=""),
        parser.add_argument("-l", "--list", dest="list", default=""),
        parser.add_argument("-b", "--bump", dest="bump", action="store_true", default=False)
        parser.add_argument("args", nargs=argparse.REMAINDER)

    def handle(self, *args, **options):
        job = []  # List of (MIB name, out path)
        mib_list = options.get("list")
        if mib_list:
            with open(mib_list) as f:
                for mlist in f:
                    mlist = mlist.strip()
                    if not mlist:
                        continue
                    m, p = mlist.strip().split(",", 1)
                    job += [(m, p)]
        else:
            if len(args) != 1:
                self.die("Single MIB name required")
            job = [(args[0], options.get("output"))]

        # Compile
        connect()
        for mib_name, path in job:
            try:
                mib = MIB.objects.get(name=mib_name)
            except DoesNotExist:
                self.die("MIB not loaded: '%s'" % mib_name)
            self.compile_mib(mib, path, bump=options.get("bump"))

    def compile_mib(self, mib, out_path, bump=False):
        self.stderr.write("%s -> %s\n" % (mib.name, out_path))
        if out_path:
            d = os.path.dirname(out_path)
            if not os.path.isdir(d):
                os.makedirs(d)
            if os.path.splitext(out_path)[-1] == ".gz":
                out = gzip.GzipFile(out_path, "w")
            else:
                out = open(out_path, "w")
        else:
            out = sys.stdout

        # Prepare MIB data
        mib_data = list(
            sorted(
                [
                    {
                        "oid": dd.oid,
                        "name": dd.name,
                        "description": dd.description,
                        "syntax": dd.syntax,
                    }
                    for dd in MIBData.objects.filter(mib=mib.id)
                ]
                + [
                    {
                        "oid": dd.oid,
                        "name": next((a for a in dd.aliases if a.startswith(mib.name + "::"))),
                        "description": dd.description,
                        "syntax": dd.syntax,
                    }
                    for dd in MIBData.objects.filter(aliases__startswith="%s::" % mib.name)
                ],
                key=lambda x: x["oid"],
            )
        )
        # Prepare MIB
        if mib.last_updated:
            last_updated = mib.last_updated.strftime("%Y-%m-%d")
        else:
            last_updated = "1970-01-01"
        version = mib.version
        if bump:  # Bump to next version
            version += 1
        data = {
            "name": mib.name,
            "description": mib.description,
            "last_updated": last_updated,
            "version": version,
            "depends_on": mib.depends_on,
            "typedefs": mib.typedefs,
            "data": mib_data,
        }
        # Serialize
        out.write(ujson.dumps(data))
        if out_path:
            out.close()


if __name__ == "__main__":
    Command().run()
