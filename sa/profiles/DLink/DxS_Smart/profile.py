# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: D-Link
# OS:     DxS_Smart
# Compatible:
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
import re
from noc.core.profile.base import BaseProfile
from noc.core.script.error import NotSupportedError


class Profile(BaseProfile):
    name = "DLink.DxS_Smart"
    pattern_more = [(r"--More--", " "), (r"CTRL\+C.+?(a All)|(r Refresh)", "a")]
    pattern_unprivileged_prompt = r"^\S+:(3|6|user|operator)#"
    pattern_syntax_error = (
        r"(?:% Invalid Command|"
        r"% Invalid input detected at|"
        r"Available commands:|"
        r"Next possible completions:)"
    )
    command_super = "enable admin"
    pattern_prompt = r"(?P<hostname>\S+(:\S+)*)[#>]"
    command_disable_pager = ""
    command_more = " "
    command_exit = "logout"
    command_save_config = "save"
    config_volatile = ["^%.*?$"]
    #
    # Version comparison
    # Version format:
    # <major>.<minor><sep><patch>
    #
    rx_ver = re.compile(r"\d+")

    platforms = {
        "DGS-1210-10P": "1.3.6.1.4.1.171.10.76.12",
        "DGS-1210-20": "1.3.6.1.4.1.171.10.76.14",
        "DGS-1210-28": "1.3.6.1.4.1.171.10.76.15",
        "DGS-1210-28P": "1.3.6.1.4.1.171.10.76.16",
        "DGS-1210-16": "1.3.6.1.4.1.171.10.76.9",
        "DGS-1210-24": "1.3.6.1.4.1.171.10.76.10",
        "DGS-1210-48": "1.3.6.1.4.1.171.10.76.11",
        "DGS-1210-52": "1.3.6.1.4.1.171.10.76.17",
        "DGS-1210-10/C1": "1.3.6.1.4.1.171.10.76.32.1",
        "DGS-1210-10P/C1": "1.3.6.1.4.1.171.10.76.18.1",
        "DGS-1210-20/C1": "1.3.6.1.4.1.171.10.76.19.1",
        "DGS-1210-28/C1": "1.3.6.1.4.1.171.10.76.20.1",
        "DGS-1210-28P/C1": "1.3.6.1.4.1.171.10.76.21.1",
        "DGS-1210-52/C1": "1.3.6.1.4.1.171.10.76.22.1",
        "DGS-1210-52P/C1": "1.3.6.1.4.1.171.10.76.33.1",
        "DGS-1500-20": "1.3.6.1.4.1.171.10.126.1.1",
        "DGS-1500-28": "1.3.6.1.4.1.171.10.126.2.1",
        "DGS-1500-28P": "1.3.6.1.4.1.171.10.126.3.1",
        "DGS-1500-52": "1.3.6.1.4.1.171.10.126.4.1",
    }

    def cmp_version(self, x, y):
        a = [int(z) for z in self.rx_ver.findall(x)]
        b = [int(z) for z in self.rx_ver.findall(y)]
        return (a > b) - (a < b)

    def convert_interface_name(self, s):
        if s.startswith("Slot0/"):
            return s[6:]
        else:
            return s

    def get_pmib(self, v):
        if v["platform"].startswith("DES-1210-52"):
            if v["version"].startswith("1") or v["version"].startswith("2"):
                return "1.3.6.1.4.1.171.10.75.7"
            elif v["version"].startswith("4"):
                return "1.3.6.1.4.1.171.10.75.20.1"
            else:
                return "1.3.6.1.4.1.171.10.75.17"
        if v["platform"].startswith("DES-1210-48"):
            return "1.3.6.1.4.1.171.10.76.11"
        if v["platform"].startswith("DES-1210-08P"):
            if v["version"].startswith("1") or v["version"].startswith("2"):
                return "1.3.6.1.4.1.171.10.75.13"
            else:
                return "1.3.6.1.4.1.171.10.75.14"
        if v["platform"].startswith("DES-1210-28P"):
            if v["version"].startswith("2") or v["version"].startswith("3"):
                return "1.3.6.1.4.1.171.10.75.6"
            else:
                return "1.3.6.1.4.1.171.10.75.19.1"
        if v["platform"].startswith("DES-1210-28"):
            if v["version"].startswith("1") or v["version"].startswith("2"):
                return "1.3.6.1.4.1.171.10.75.5"
            else:
                return "1.3.6.1.4.1.171.10.75.15"
        if v["platform"].startswith("DES-1210"):
            return "1.3.6.1.4.1.171.10.75.7"
        r = self.platforms.get(v["platform"])
        if r:
            return r
        else:
            raise NotSupportedError()

    rx_port = re.compile(
        r"^(?P<port>\d+)\s+"
        r"(?P<admin_state>Enabled|Disabled)\s+"
        r"(?P<admin_speed>Auto|10M|100M|1000M|10G)/"
        r"((?P<admin_duplex>Half|Full)/)?"
        r"(?P<admin_flowctrl>Enabled|Disabled)\s+"
        r"(?P<status>LinkDown|Link\sDown|Err\-Disabled|Empty)?"
        r"((?P<speed>10M|100M|1000M|10G)/"
        r"(?P<duplex>Half|Full)/(?P<flowctrl>None|Disabled|802.3x))?\s+"
        r"(\n\s+(?P<mdix>Auto|MDI|MDIX|\-)\s*)?",
        re.MULTILINE,
    )

    rx_descr = re.compile(r"^\s+(?P<port>\d+)\s(?P<descr>.+)\n", re.MULTILINE)

    def get_ports(self, script, interface=None):
        descr = []
        try:
            c = script.cli("show ports description", cached=True)
            for match in self.rx_descr.finditer(c):
                descr += [{"port": match.group("port"), "descr": match.group("descr").strip()}]
        except script.CLISyntaxError:
            pass
        objects = []
        try:
            if interface is not None:
                c = script.cli(("show ports %s" % interface), cached=True)
            else:
                c = script.cli("show ports", cached=True)
        except script.CLISyntaxError:
            raise script.NotSupportedError()
        for match in self.rx_port.finditer(c):
            objects += [
                {
                    "port": match.group("port"),
                    "admin_state": match.group("admin_state") == "Enabled",
                    "admin_speed": match.group("admin_speed"),
                    "admin_duplex": match.group("admin_duplex"),
                    "admin_flowctrl": match.group("admin_flowctrl"),
                    "status": match.group("status") is None,
                    "speed": match.group("speed"),
                    "duplex": match.group("duplex"),
                    "flowctrl": match.group("flowctrl"),
                    "mdix": match.group("mdix"),
                }
            ]
        prev_port = None
        ports = []
        for i in objects:
            for d in descr:
                if int(i["port"]) == int(d["port"]):
                    i["descr"] = d["descr"]
            if prev_port and (prev_port == i["port"]):
                if i["status"] is True:
                    k = 0
                    for j in ports:
                        if j["port"] == i["port"]:
                            ports[k] = i
                            break
                        k = k + 1
            else:

                ports += [i]
            prev_port = i["port"]
        return ports

    rx_vlan = re.compile(
        r"VID\s+:\s+(?P<vlan_id>\d+)\s+"
        r"VLAN Name\s+:\s+(?P<vlan_name>\S+)\s*\n"
        r"VLAN Type\s+:\s+(?P<vlan_type>\S+)\s*.+?"
        r"^(Current Tagged P|Tagged p)orts\s+:\s*(?P<tagged_ports>\S*?)\s*\n"
        r"^(Current Untagged P|Untagged p)orts\s*:\s*"
        r"(?P<untagged_ports>\S*?)\s*\n",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    rx_vlan1 = re.compile(
        r"VID\s+:\s+(?P<vlan_id>\d+)\s+"
        r"VLAN Name\s+:\s*(?P<vlan_name>\S*)\s*\n"
        r"VLAN Type\s+:\s+(?P<vlan_type>\S+)\s*.+?"
        r"^Member Ports\s+:\s*(?P<member_ports>\S*?)\s*\n"
        r"(Static ports\s+:\s*\S+\s*\n)?"
        r"^(Current )?Untagged ports\s*:\s*(?P<untagged_ports>\S*?)\s*\n",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    def get_vlans(self, script):
        vlans = []
        c = script.cli("show vlan", cached=True)
        for match in self.rx_vlan.finditer(c):
            tagged_ports = script.expand_interface_range(match.group("tagged_ports"))
            untagged_ports = script.expand_interface_range(match.group("untagged_ports"))
            vlans += [
                {
                    "vlan_id": int(match.group("vlan_id")),
                    "vlan_name": match.group("vlan_name"),
                    "vlan_type": match.group("vlan_type"),
                    "tagged_ports": tagged_ports,
                    "untagged_ports": untagged_ports,
                }
            ]
        if vlans == []:
            for match in self.rx_vlan1.finditer(c):
                tagged_ports = []
                member_ports = script.expand_interface_range(match.group("member_ports"))
                untagged_ports = script.expand_interface_range(match.group("untagged_ports"))
                for port in member_ports:
                    if port not in untagged_ports:
                        tagged_ports += [port]
                vlans += [
                    {
                        "vlan_id": int(match.group("vlan_id")),
                        "vlan_name": match.group("vlan_name"),
                        "vlan_type": match.group("vlan_type"),
                        "tagged_ports": tagged_ports,
                        "untagged_ports": untagged_ports,
                    }
                ]
        return vlans


# DES-1210-series
def DES1210(v):
    return v["platform"].startswith("DES-1210")


# DGS-1210-series
def DGS1210(v):
    return v["platform"].startswith("DGS-1210")


# DGS-1500-series
def DGS1500(v):
    return v["platform"].startswith("DGS-1500")
