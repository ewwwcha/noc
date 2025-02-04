# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Ericsson
# OS:     SEOS
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    """
    For correct polling on snmp it is necessary to enable "snmp extended read" in settings
    """

    name = "Ericsson.SEOS"
    pattern_more = "^---(more)---"
    pattern_unprivileged_prompt = r"^(?:\[(?P<context>\S+)\])?(?P<hostname>\S+)>"
    pattern_prompt = r"^(?:\[(?P<context>\S+)\])?(?P<hostname>\S+)#"
    pattern_syntax_error = r"% Invalid input at|% ERROR Invalid input detected"
    command_disable_pager = "terminal length 0"
    command_super = "enable"
    command_enter_config = "configure"
    command_leave_config = "exit"
    rogue_chars = [re.compile(r"\x08{4,}\S+"), "\r"]

    rx_ifname = re.compile("\S+\s+\d+\/\d+\/\d+")

    def convert_interface_name(self, s):
        """
        >>> Profile().convert_interface_name("LAN    1/1/8")
        '1/1/8-LAN'
        >>> Profile().convert_interface_name("1/1/8-LAN")
        '1/1/8-LAN'
        """
        match = self.rx_ifname.match(s)
        if match:
            iface = s.split()
            return "%s-%s" % (iface[1], iface[0])
        else:
            return s
