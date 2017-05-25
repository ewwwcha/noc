# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# MAC Check
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import time
# NOC modules
from noc.services.discovery.jobs.base import DiscoveryCheck
from noc.core.perf import metrics
from noc.core.mac import MAC


class MACCheck(DiscoveryCheck):
    """
    MAC discovery
    """
    name = "mac"
    required_script = "get_mac_address_table"

    METRIC_FIELDS = "mac.date.ts.managed_object.mac" \
                    ".interface.interface_profile.segment.vlan.is_uni"

    def handler(self):
        now = time.localtime()
        date = now.stftime("%Y-%m-%d", now)
        ts = now.stftime("%Y-%m-%d %H:%M:%S")
        mo_id = self.object.get_bi_id()
        seg_id = self.object.segment.get_bi_id()
        unknown_interfaces = set()
        disabled_by_profile = set()
        total_macs = 0
        processed_macs = 0
        data = []
        # Collect and process MACs
        result = self.object.scripts.get_mac_address_table()
        for v in result:
            total_macs += 1
            if v["type"] != "D" or not v["interfaces"]:
                continue
            ifname = v["interfaces"][0]
            iface = self.get_interface_by_name(ifname)
            if not iface:
                unknown_interfaces.add(ifname)
                continue  # Interface not found
            if not iface.profile or not iface.profile.mac_discovery:
                disabled_by_profile.add(ifname)
                continue  # MAC discovery disabled on interface
            data += ["\t".join((
                date,  # date
                ts,  # ts
                mo_id,  # managed_object
                int(MAC(v["mac"])),  # mac
                ifname,  # interface
                iface.profile.get_bi_id(),  # interface_profile
                seg_id,  # segment
                v.get("vlan_id", 0),  # vlan
                iface.profile.is_uni  # is_uni
            ))]
            processed_macs += 1
        if unknown_interfaces:
            self.logger.info("Ignoring unknown interfaces: %s",
                             ", ".join(unknown_interfaces))
        if disabled_by_profile:
            self.logger.info("MAC collection disabled on interfaces:",
                             ", ".join(disabled_by_profile))
        metrics["discovery_mac_total_macs"] += total_macs
        metrics["discovery_mac_processed_macs"] += processed_macs
        metrics["discovery_mac_ignored_macs"] += total_macs - processed_macs
        if data:
            self.logger.info("%d MAC addresses are collected. Sending",
                             processed_macs)
            self.service.register_ch_metrics(
                self.METRIC_FIELDS,
                data
            )
        else:
            self.logger.info("No MAC addresses collected")
