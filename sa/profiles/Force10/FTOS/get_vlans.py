# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Force10.FTOS.get_vlans
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetvlans import IGetVlans
from noc.core.text import parse_table


class Script(BaseScript):
    name = "Force10.FTOS.get_vlans"
    interface = IGetVlans

    def execute(self):
        if self.has_snmp():
            try:
                oids = {}
                # Get OID -> VLAN ID mapping
                for oid, v in self.snmp.getnext(
                    "1.3.6.1.2.1.17.7.1.4.2.1.3", bulk=True
                ):  # dot1qVlanFdbId
                    oids[oid.split(".")[-1]] = v
                # Get VLAN names
                result = []
                for oid, v in self.snmp.getnext(
                    "1.3.6.1.2.1.17.7.1.4.3.1.1", bulk=True
                ):  # dot1qVlanStaticName
                    o = oid.split(".")[-1]
                    result += [{"vlan_id": int(oids[o]), "name": v.strip()}]
                return sorted(result, lambda x, y: cmp(x["vlan_id"], y["vlan_id"]))
            except self.snmp.TimeOutError:
                # SNMP failed, continue with CLI
                pass
        return [{"vlan_id": x[0], "name": x[1]} for x in parse_table(self.cli("show vlan brief"))]
