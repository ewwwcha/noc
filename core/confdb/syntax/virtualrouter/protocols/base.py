# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# <describe module here>
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# NOC modules
from ...defs import DEF
from .http.base import HTTP_SYNTAX
from .https.base import HTTPS_SYNTAX
from .igmpsnooping.base import IGMP_SNOOPING_SYNTAX
from .isis.base import ISIS_SYNTAX
from .ldp.base import LDP_SYNTAX
from .ospf.base import OSPF_SYNTAX
from .pim.base import PIM_SYNTAX
from .rsvp.base import RSVP_SYNTAX
from .snmp.base import SNMP_SYNTAX
from .ssh.base import SSH_SYNTAX
from .telnet.base import TELNET_SYNTAX

VR_PROTOCOLS_SYNTAX = DEF(
    "protocols",
    [
        TELNET_SYNTAX,
        SSH_SYNTAX,
        HTTP_SYNTAX,
        HTTPS_SYNTAX,
        SNMP_SYNTAX,
        ISIS_SYNTAX,
        OSPF_SYNTAX,
        LDP_SYNTAX,
        RSVP_SYNTAX,
        PIM_SYNTAX,
        IGMP_SNOOPING_SYNTAX,
    ],
)
