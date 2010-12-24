# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Vendor: D-Link
## OS:     DxS
## Compatible:
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
"""
"""
import noc.sa.profiles
from noc.sa.protocols.sae_pb2 import TELNET,SSH

class Profile(noc.sa.profiles.Profile):
    name="DLink.DxS"
    supported_schemes=[TELNET,SSH]
    pattern_username="([Uu]ser ?[Nn]ame|[Ll]ogin):"
    pattern_password="[Pp]ass[Ww]ord:"
    pattern_more="CTRL\+C.+?a All"
    pattern_prompt=r"^\S+?#"
    command_disable_pager="disable clipaging"
    command_more="a"
    command_exit="logout"
    config_volatile=["^%.*?$"]
