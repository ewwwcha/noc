# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Axis.VAPIX.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID


class Script(BaseScript):
    name = "Axis.VAPIX.get_chassis_id"
    cache = True
    interface = IGetChassisID

    def execute(self):
        macs = []
        c = self.profile.get_dict(self)
        for i in range(0, 4):  # for future models
            mac = c.get("root.Network.eth%d.MACAddress" % i)
            if mac is not None:
                macs += [mac]
        return [{
            "first_chassis_mac": mac,
            "last_chassis_mac": mac
        } for mac in sorted(macs)]  # noqa: F812
