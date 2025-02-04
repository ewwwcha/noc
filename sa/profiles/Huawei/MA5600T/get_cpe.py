# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Huawei.MA5600T.get_cpe
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
import six

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetcpe import IGetCPE
from noc.core.text import parse_table_header
from noc.core.text import parse_kv
from noc.core.mib import mib


class Script(BaseScript):
    name = "Huawei.MA5600T.get_cpe"
    interface = IGetCPE

    cache = True

    splitter = re.compile("\s*-+\n")

    status_map = {"online": "active", "offline": "inactive"}  # associated  # disassociating
    INACTIVE_STATE = {"initial"}

    detail_map = {
        "ont distance(m)": "ont_distance",
        "ont ip 0 address/mask": "ont_address",
        "last down cause": "down_cause",
    }

    def execute_cli(self, **kwargs):
        r = {}
        # v = self.cli("display ont info 0 all")
        for c in ("display ont info 0 all", "display ont version 0 all"):
            v = self.cli(c)
            for table in v.split("\n\n"):
                tables_data = []
                parts = self.splitter.split(table)
                parts = parts[1:]
                while len(parts) > 2:
                    header, body = parts[:2]
                    parts = parts[2:]
                    header = header.splitlines()
                    if len(header[0]) - len(header[0].lstrip()) - 2:
                        # pylint: disable=line-too-long
                        # Align first line by two whitespace if header:
                        # '  -----------------------------------------------------------------------------',
                        # '                                       F/S/P   ONT         SN         Control     Run      Config   Match    Protect',
                        # '          ID                     flag        state    state    state    side',
                        # '  -----------------------------------------------------------------------------'
                        header[0] = header[0][len(header[0]) - len(str.lstrip(header[0])) - 2 :]
                    head = parse_table_header(header)
                    del head[2]  # remove empty header
                    tables_data += self.profile.parse_table1(body, head)
                else:
                    pass
                    # summary = parts
                for t in tables_data:
                    if "Config state" in t and t["Config state"][0] in self.INACTIVE_STATE:
                        continue
                    if "ONT-ID" in t:
                        ont_id = "%s/%s" % (t["F/S/P"][0].replace(" ", ""), t["ONT-ID"][0])
                        if ont_id in r:
                            r[ont_id]["description"] = t["Description"][0]
                        continue
                    if "F/S/P/ONT-ID" in t:
                        ont_id = t["F/S/P/ONT-ID"][0].replace(" ", "")
                        if ont_id in r:
                            r[ont_id].update(
                                {
                                    "vendor": t["Vendor ID"][0],
                                    "model": t["ONT"][0] + t["Model"][0] if t["Model"] else "",
                                    "version": t["Software Version"][0]
                                    if t["Software Version"]
                                    else "",
                                }
                            )
                        continue
                    status = "other"
                    if "ONT ID" in t:
                        ont_id, serial = t["ONT ID"][0].split()
                        status = self.status_map[t["Run state"][0]]
                    elif "ONT" in t:
                        #  -----------------------------------------------------------------------------
                        #  F/S/P   ONT         SN         Control     Run      Config   Match    Protect
                        #                       ID                     flag        state    state    state    side
                        #  -----------------------------------------------------------------------------
                        #
                        self.logger.warning("Shift header row. %s" % header)
                        ont_id, serial = t["ONT"][0].split()
                        status = self.status_map[t["Run ID"][0]]
                    # else:
                    #    self.logger.warning("Unknown ID")
                    #    continue
                    ont_id = "%s/%s" % (t["F/S/P"][0].replace(" ", ""), ont_id)
                    r[ont_id] = {
                        "interface": t["F/S/P"][0].replace(" ", ""),
                        "status": status,
                        "id": ont_id,
                        "global_id": serial + t["SN"][0],
                        "type": "ont",
                        "serial": serial + t["SN"][0],
                        "description": "",
                        "location": "",
                    }
        for ont_id in r:
            # if r[ont_id]["status"] != "active":
            #     continue
            v = self.cli("display ont info %s %s %s %s" % tuple(ont_id.split("/")))
            parts = self.splitter.split(v)
            parse_result = parse_kv(self.detail_map, parts[1])
            try:
                r[ont_id]["distance"] = float(parse_result.get("ont_distance", 0))
            except ValueError:
                pass
            address = parse_result.get("ont_address", "")
            if address:
                r[ont_id]["ip"] = parse_result.get("ont_address", "").split("/")[0]
        return list(six.itervalues(r))

    def execute_snmp(self, **kwargs):
        r = {}
        names = {
            x: y for y, x in six.iteritems(self.scripts.get_ifindexes(name_oid="IF-MIB::ifName"))
        }
        for ont_index, ont_serial, ont_descr in self.snmp.get_tables(
            [
                mib["HUAWEI-XPON-MIB::hwGponDeviceOntSn"],
                mib["HUAWEI-XPON-MIB::hwGponDeviceOntDespt"],
            ],
            bulk=False,
        ):
            ifindex, ont_id = ont_index.split(".")
            ont_id = "%s/%s" % (names[int(ifindex)], ont_id)
            r[ont_index] = {
                "interface": names[int(ifindex)],
                "status": "inactive",
                "id": ont_id,
                "global_id": ont_serial.encode("hex").upper(),
                "type": "ont",
                "serial": ont_serial.encode("hex").upper(),
                "description": ont_descr,
                "location": "",
            }
        for ont_index, ont_status in self.snmp.get_tables(
            [mib["HUAWEI-XPON-MIB::hwGponDeviceOntControlRunStatus"]]
        ):
            r[ont_index]["status"] = "active" if ont_status == 1 else "inactive"
        for ont_index, ont_version, ont_vendor, ont_model in self.snmp.get_tables(
            [
                mib["HUAWEI-XPON-MIB::hwGponDeviceOntVersion"],
                mib["HUAWEI-XPON-MIB::hwGponDeviceOntVendorId"],
                mib["HUAWEI-XPON-MIB::hwGponDeviceOntProductId"],
            ],
            bulk=False,
        ):
            if ont_version != -1:
                r[ont_index]["version"] = ont_version
            if ont_model != -1:
                r[ont_index]["model"] = ont_model
            if ont_vendor != -1:
                r[ont_index]["vendor"] = ont_vendor
        for ont_index, ont_distance in self.snmp.get_tables(
            [mib["HUAWEI-XPON-MIB::hwGponDeviceOntControlRanging"]], bulk=False
        ):
            if ont_distance != -1:
                r[ont_index]["distance"] = ont_distance

        return six.itervalues(r)
