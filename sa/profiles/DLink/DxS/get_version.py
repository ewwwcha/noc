# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DLink.DxS.get_version
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
import noc.sa.script
from noc.sa.interfaces import IGetVersion
import re

class Script(noc.sa.script.Script):
    name="DLink.DxS.get_version"
    cache=True
    implements=[IGetVersion]
    rx_ver=re.compile(r"Device Type\s+:\s+(?P<platform>\S+).+Firmware Version\s+:\s+(?:Build\s+)?(?P<version>\S+)",re.MULTILINE|re.DOTALL)
    def execute(self):
        data=self.cli("show switch")
        match=self.re_search(self.rx_ver, data)
        return {
            "vendor"    : "DLink",
            "platform"  : match.group("platform"),
            "version"   : match.group("version"),
        }
