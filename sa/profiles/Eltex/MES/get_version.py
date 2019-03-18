# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.MES.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion
from noc.core.mib import mib


class Script(BaseScript):
    name = "Eltex.MES.get_version"
    interface = IGetVersion
    cache = True

    rx_version1 = re.compile(
        r"^SW version+\s+(?P<version>\S+)", re.MULTILINE)
    rx_version2 = re.compile(
        r"^Active-image: \S+\s*\n"
        r"^\s+Version: (?P<version>\S+)", re.MULTILINE)
    rx_bootprom = re.compile(
        r"^Boot version+\s+(?P<bootprom>\S+)", re.MULTILINE)
    rx_hardware = re.compile(
        r"^HW version+\s+(?P<hardware>\S+)$", re.MULTILINE)
    rx_serial1 = re.compile(
        r"^Serial number :\s+(?P<serial>\S+)$", re.MULTILINE)
    rx_serial2 = re.compile(
        r"^\s+1\s+(?P<serial>\S+)\s*\n", re.MULTILINE)
    rx_serial3 = re.compile(
        r"^\s+1\s+(?P<mac>\S+)\s+(?P<hardware>\S+)\s+(?P<serial>\S+)\s*\n",
        re.MULTILINE)
    rx_platform = re.compile(
        r"^System Object ID:\s+(?P<platform>\S+)$", re.MULTILINE)

    platforms = {
        "24": "MES-3124",
        "26": "MES-5148",
        "30": "MES-3124F",
        "35": "MES-3108",
        "36": "MES-3108F",
        "38": "MES-3116",
        "39": "MES-3116F",
        "40": "MES-3224",
        "41": "MES-3224F",
        "42": "MES-1024",
        "43": "MES-2124",
        "52": "MES-1124",
        "54": "MES-5248",
        "59": "MES-2124P",
        "74": "MES-5324",
        "75": "MES-2124F",
        "76": "MES-2324",
        "78": "MES-2324FB",
        "81": "MES-3324F",
        "88": "MES-2308",
        "89": "MES-2308P",
        "92": "MES-2324P"
    }

    def execute_snmp(self, **kwargs):
        try:
            platform = self.snmp.get(mib["SNMPv2-MIB::sysObjectID.0"], cached=True)
            platform = platform.split('.')[8]
            platform = self.platforms.get(platform.split(')')[0])
            version = self.snmp.get("1.3.6.1.2.1.47.1.1.1.1.10.67108992",
                                    cached=True)
            bootprom = self.snmp.get("1.3.6.1.2.1.47.1.1.1.1.9.67108992",
                                     cached=True)
            hardware = self.snmp.get("1.3.6.1.2.1.47.1.1.1.1.8.67108992",
                                     cached=True)
            serial = self.snmp.get("1.3.6.1.2.1.47.1.1.1.1.11.67108992",
                                   cached=True)
            return {
                "vendor": "Eltex",
                "platform": platform,
                "version": version,
                "attributes": {
                    "Boot PROM": bootprom,
                    "HW version": hardware,
                    "Serial Number": serial
                }
            }
        except self.snmp.TimeOutError:
            raise self.UnexpectedResultError

    def execute_cli(self, **kwargs):
        if self.has_capability("Stack | Members"):
            plat = self.cli("show system unit 1", cached=True)
            ver = self.cli("show version unit 1", cached=True)
            ser = self.cli("show system id unit 1", cached=True)
        else:
            plat = self.cli("show system", cached=True)
            ver = self.cli("show version", cached=True)
            ser = self.cli("show system id", cached=True)

        match = self.rx_platform.search(plat)
        platform = match.group("platform")
        platform = platform.split(".")[8]
        platform = self.platforms.get(platform)

        match = self.rx_version1.search(ver)
        if match:
            version = self.rx_version1.search(ver)
            bootprom = self.rx_bootprom.search(ver)
            hardware = self.rx_hardware.search(ver)
        else:
            version = self.rx_version2.search(ver)
            bootprom = None
            hardware = None

        match = self.rx_serial1.search(ser)
        match2 = self.rx_serial3.search(ser)
        if match:
            serial = self.rx_serial1.search(ser)
        elif match2:
            # Unit    MAC address    Hardware version Serial number
            # ---- ----------------- ---------------- -------------
            # 1   xx:xx:xx:xx:xx:xx     02.01.02      ESXXXXXXX
            serial = self.rx_serial3.search(ser)
        else:
            serial = self.rx_serial2.search(ser)

        res = {
            "vendor": "Eltex",
            "platform": platform,
            "version": version.group("version"),
            "attributes": {}}

        if serial:
            res["attributes"]["Serial Number"] = serial.group("serial")
        if bootprom:
            res["attributes"]["Boot PROM"] = bootprom.group("bootprom")
        if hardware:
            res["attributes"]["HW version"] = hardware.group("hardware")
        return res
