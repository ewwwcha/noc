# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion
import re


class Script(BaseScript):
    name = "Cisco.NXOS.get_version"
    cache = True
    interface = IGetVersion
    rx_ver = re.compile(
        r"^Cisco Nexus Operating System \(NX-OS\) Software.+?"
        r"Software.+?(?:system|NXOS):\s+version\s+"
        r"(?P<version>\S+).+?Hardware\s+cisco\s+\S+\s+(?P<platform>\S+)",
        re.MULTILINE | re.DOTALL,
    )
    rx_snmp_ver = re.compile(r"^Cisco NX-OS\(tm\) .*?Version (?P<version>[^,]+),", re.IGNORECASE)
    rx_snmp_platform = re.compile(r"^Nexus\s+(?P<platform>\S+).+Chassis$", re.IGNORECASE)
    rx_snmp_platform1 = re.compile(r"^(?P<platform>N9K-C93\d\d\S+)$")

    def execute(self):
        if self.has_snmp():
            try:
                v = self.snmp.get("1.3.6.1.2.1.1.1.0")  # sysDescr.0
                match = self.rx_snmp_ver.search(v)
                version = match.group("version")
                # Get platform via ENTITY-MIB
                platform = None
                # ENTITY-MIB::entPhysicalName
                for oid, v in self.snmp.getnext("1.3.6.1.2.1.47.1.1.1.1.7"):
                    match = self.rx_snmp_platform.match(v)
                    if match:
                        platform = match.group("platform")
                        break
                    match = self.rx_snmp_platform1.match(v)
                    if match:
                        platform = match.group("platform")
                        break
                return {"vendor": "Cisco", "platform": platform, "version": version}
            except self.snmp.TimeOutError:
                pass
        v = self.cli("show version | no-more")
        match = self.rx_ver.search(v)
        return {
            "vendor": "Cisco",
            "platform": match.group("platform"),
            "version": match.group("version"),
        }
