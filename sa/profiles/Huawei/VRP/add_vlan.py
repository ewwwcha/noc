# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Huawei.VRP.add_vlan
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.iaddvlan import IAddVlan


class Script(BaseScript):
    name = "Huawei.VRP.add_vlan"
    interface = IAddVlan

    def execute(self, vlan_id, name, tagged_ports):
        with self.configure():
            self.cli("vlan %d" % vlan_id)
            self.cli("description %s" % name)
            self.cli("quit")
        self.save_config()
        return True
