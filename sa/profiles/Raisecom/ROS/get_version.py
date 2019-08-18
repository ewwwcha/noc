# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Raisecom.ROS.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Raisecom.ROS.get_version"
    interface = IGetVersion
    cache = True

    def execute_cli(self):
        v = self.profile.get_version(self)
        return {
            "vendor": v.get("vendor", "Raisecom"),
            "platform": v["platform"],
            "version": v["version"],
            "attributes": {
                "Serial Number": v["serial"],
                "Boot PROM": v["bootstrap"],
                "HW version": v["hw_rev"],
            },
        }
