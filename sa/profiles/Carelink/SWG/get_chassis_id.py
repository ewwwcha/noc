# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Carelink.SWG.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):
    name = "Carelink.SWG.get_chassis_id"
    interface = IGetChassisID
    cache = True

    rx_mac = re.compile(r"MAC Address\s+: (?P<mac>\S+)")

    def execute(self):
        match = self.rx_mac.search(self.cli("show system", cached=True))
        mac = match.group("mac")
        return {"first_chassis_mac": mac, "last_chassis_mac": mac}
