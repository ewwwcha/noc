# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Eltex.WOP.get_metrics
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import division
import six
from collections import defaultdict

# NOC modules
from noc.sa.profiles.Generic.get_metrics import Script as GetMetricsScript, metrics
from noc.core.validators import is_ipv4


class Script(GetMetricsScript):
    name = "Eltex.WOP.get_metrics"
    scale_x8 = {"Interface | Load | In", "Interface | Load | Out"}  # Scale 8 metric type

    @metrics(["CPU | Usage"], volatile=False, access="C")  # CLI version
    def get_cpu_metrics(self, metrics):
        c = self.cli("get monitoring cpu-usage")
        cpu = c.strip()
        self.set_metric(id=("CPU | Usage", None), value=round(float(cpu) + 0.5))

    @metrics(["Memory | Usage"], volatile=False, access="C")  # CLI version
    def get_memory_metrics(self, metrics):
        c = self.cli("get monitoring memory-usage")
        memory = c.strip()
        self.set_metric(id=("Memory | Usage", None), value=memory)

    @metrics(["Environment | Temperature"], volatile=False, access="C")  # CLI version
    def get_temperature_metrics(self, metrics):
        c = self.cli("get monitoring temperature")
        temperature = c.strip()
        self.set_metric(id=("Environment | Temperature", None), value=temperature)

    @metrics(["Check | Result", "Check | RTT"], volatile=False, access="C")  # CLI version
    def get_avail_metrics(self, metrics):
        if not self.credentials["path"]:
            return
        check_id = 999
        check_rtt = 998
        for m in metrics:
            if m.metric == "Check | Result":
                check_id = m.id
            if m.metric == "Check | RTT":
                check_rtt = m.id
        for ip in self.credentials["path"].split(","):
            if is_ipv4(ip.strip()):
                result = self.scripts.ping(address=ip)
                self.set_metric(
                    id=check_id,
                    metric="Check | Result",
                    path=("ping", ip),
                    value=bool(result["success"]),
                    multi=True,
                )
                if result["success"] and check_rtt != 998:
                    self.set_metric(
                        id=check_rtt,
                        metric="Check | RTT",
                        path=("ping", ip),
                        value=bool(result["success"]),
                    )

    def get_beacon_iface(self, ifaces):
        """
        Beacon iface. Add Status and mapping for SSID <-> Radio interface
        :param ifaces:
        :return:
        """
        for s in ifaces:
            if "bss" not in s:
                continue
            v = self.cli("get bss %s detail" % s["bss"])
            for block in v.split("\n\n"):
                data = dict(
                    line.split(None, 1)
                    for line in block.splitlines()
                    if len(line.split(None, 1)) == 2
                )
                if "status" not in data:
                    continue
                s["status"] = data["status"]
                s["radio"] = data["radio"]

    @metrics(
        [
            "Interface | Load | In",
            "Interface | Load | Out",
            "Interface | Packets | In",
            "Interface | Packets | Out",
            "Interface | Errors | In",
            "Interface | Errors | Out",
        ],
        has_capability="DB | Interfaces",
        volatile=False,
        access="C",  # CLI version
    )
    def get_interface_metrics(self, metrics):
        ifaces = []
        radio_metrics = self.get_radio_metrics(metrics)
        iface_metric_map = {
            "rx-bytes": "Interface | Load | In",
            "tx-bytes": "Interface | Load | Out",
            "rx-packets": "Interface | Packets | In",
            "tx-packets": "Interface | Packets | Out",
            "rx-errors": "Interface | Errors | In",
            "tx-errors": "Interface | Errors | Out",
        }
        c = self.cli("get interface all detail")
        for block in c.split("\n\n"):
            ifaces += [
                dict(
                    line.split(None, 1)
                    for line in block.splitlines()
                    if len(line.split(None, 1)) == 2
                )
            ]
        self.get_beacon_iface(ifaces)
        for data in ifaces:
            if data.get("status", "up") == "down":
                # Skip if interface is down
                continue
            if "ssid" in data:
                ssid = data["ssid"].strip().replace(" ", "").replace("Managed", "")
                if ssid.startswith("2a2d"):
                    # 2a2d - hex string
                    ssid = ssid.decode("hex")
                iface = "%s.%s" % (data["name"], ssid)
            else:
                iface = data["name"]
            for field, metric in six.iteritems(iface_metric_map):
                if data.get(field) is not None:
                    self.set_metric(
                        id=(metric, ["", "", "", iface]),
                        value=data[field],
                        type="counter",
                        scale=8 if metric in self.scale_x8 else 1,
                    )
            # LifeHack. Set Radio interface metrics to SSID
            if "radio" in data and data["radio"] in radio_metrics:
                self.set_metric(
                    id=("Radio | TxPower", ["", "", "", iface]),
                    value=radio_metrics[data["radio"]]["tx-power"],
                )

    @metrics(
        ["Radio | TxPower", "Radio | Quality"],
        has_capability="DB | Interfaces",
        volatile=True,
        access="C",  # CLI version
    )
    def get_radio_metrics(self, metrics):
        r_metrics = defaultdict(dict)
        w = self.cli("get radio all detail")
        for block in w.split("\n\n"):
            data = dict(
                line.split(None, 1) for line in block.splitlines() if len(line.split(None, 1)) == 2
            )
            if not data:
                continue
            iface = data["name"].strip()
            if data.get("tx-power-dbm") is not None:
                self.set_metric(
                    id=("Radio | TxPower", ["", "", "", iface]),
                    # Max TxPower 27dBm, convert % -> dBm
                    value=int(data["tx-power-dbm"].strip()),
                )
                r_metrics[iface]["tx-power"] = int(data["tx-power-dbm"].strip())
        return r_metrics
