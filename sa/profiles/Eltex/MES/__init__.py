# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Eltex
# OS:     MES
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re
# NOC modules
from noc.core.profile.base import BaseProfile
from noc.sa.interfaces.base import InterfaceTypeError
from noc.lib.validators import is_int


class Profile(BaseProfile):
    name = "Eltex.MES"
    pattern_more = [
        (r"^More: <space>,  Quit: q, One line: <return>$", " "),
        (r"\[Yes/press any key for no\]", "Y"),
        (r"<return>, Quit: q or <ctrl>", " "),
        (r"q or <ctrl>+z", " "),
        (r"Overwrite file \[startup-config\].... \(Y\/N\)", "Y"),
        (r"Would you like to continue \? \(Y\/N\)\[N\]", "Y")
    ]
    pattern_unprivileged_prompt = r"^(?P<hostname>\S+)>\s*"
    pattern_syntax_error = \
        r"^% (Unrecognized command|Incomplete command|" \
        r"Wrong number of parameters or invalid range, size or " \
        r"characters entered)$"
    command_disable_pager = "terminal datadump"
    command_super = "enable"
    command_enter_config = "configure"
    command_leave_config = "end"
    command_save_config = "copy running-config startup-config"
    pattern_prompt = \
        r"^(?P<hostname>[A-Za-z0-9-_ \:\.\*\'\,\(\)\/]+)?" \
        r"(?:\(config[^\)]*\))?#"
    # to one SNMP GET request
    snmp_metrics_get_chunk = 10
    config_tokenizer = "indent"
    config_tokenizer_settings = {
        "line_comment": "!",
        "end_of_context": "exit"
    }
    config_normalizer = "MESNormalizer"
    confdb_defaults = [
        ("hints", "interfaces", "defaults", "admin-status", True),
        ("hints", "protocols", "lldp", "status", True),
        ("hints", "protocols", "spanning-tree", "status", False),
        ("hints", "protocols", "spanning-tree", "priority", "32768"),
        ("hints", "protocols", "loop-detect", "status", False)
    ]

    INTERFACE_TYPES = {
        "as": "physical",    # Async
        "at": "physical",    # ATM
        "bv": "aggregated",  # BVI
        "bu": "aggregated",  # Bundle
        # "C": "physical",     # @todo: fix
        "ca": "physical",    # Cable
        "cd": "physical",    # CDMA Ix
        "ce": "physical",    # Cellular
        "et": "physical",    # Ethernet
        "fa": "physical",    # FastEthernet
        "gi": "physical",    # GigabitEthernet
        "gr": "physical",    # Group-Async
        "lo": "loopback",    # Loopback
        "oo": "management",  # oob
        "mf": "aggregated",  # Multilink Frame Relay
        "mu": "aggregated",  # Multilink-group interface
        "po": "aggregated",  # Port-channel/Portgroup
        # "R": "aggregated",   # @todo: fix
        "sr": "physical",    # Spatial Reuse Protocol
        "se": "physical",    # Serial
        "st": "management",  # Stack-port
        "te": "physical",    # TenGigabitEthernet
        "fo": "physical",    # FortyGigabitEthernet
        "tu": "tunnel",      # Tunnel
        "vl": "SVI",         # VLAN, found on C3500XL
        "xt": "SVI"          # Extended Tag ATM
    }

    @classmethod
    def get_interface_type(cls, name):
        return cls.INTERFACE_TYPES.get((name[:2]).lower())

    # Eltex-like translation
    rx_eltex_interface_name = re.compile(
        r"^(?P<type>[a-z]{2})[a-z\-]*\s*"
        r"(?P<number>\d+(/\d+(/\d+)?)?(\.\d+(/\d+)*(\.\d+)?)?(:\d+(\.\d+)*)?(/[a-z]+\d+(\.\d+)?)?(A|B)?)?",
        re.IGNORECASE
    )

    def convert_interface_name(self, s):
        """
        >>> Profile().convert_interface_name_cisco("gi1/0/1")
        'Gi 1/0/1'
        >>> Profile().convert_interface_name_cisco("gi1/0/1?")
        'Gi 1/0/1'
        """
        match = self.rx_eltex_interface_name.match(str(s))
        if is_int(s):
            return "Vl %s" % s
        elif s in ["oob", "stack-port"]:
            return s
        elif match:
            return "%s %s" % (match.group("type").capitalize(),
                              match.group("number"))
        else:
            raise InterfaceTypeError("Invalid interface '%s'" % s)
