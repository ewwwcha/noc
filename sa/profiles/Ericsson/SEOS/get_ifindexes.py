# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Ericsson.SEOS.get_ifindexes
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetifindexes import IGetIfindexes
from noc.sa.interfaces.base import InterfaceTypeError
from noc.core.mib import mib


class Script(BaseScript):
    name = "Ericsson.SEOS.get_ifindexes"
    interface = IGetIfindexes
    cache = True
    requires = []

    MAX_GETNEXT_RETIRES = 0

    def get_getnext_retires(self):
        return self.MAX_GETNEXT_RETIRES

    def execute_snmp(self):
        r = {}
        unknown_interfaces = []
        for oid, index in self.snmp.getnext(mib["IF-MIB::ifIndex"], max_retries=self.get_getnext_retires()):
            name = self.snmp.get(mib["IF-MIB::ifName.%s" % index])
            descr = self.snmp.get(mib["IF-MIB::ifDescr.%s" % index])
            try:
                v = self.profile.convert_interface_name("%s/%s" % (name, descr))
            except InterfaceTypeError as e:
                self.logger.debug("Ignoring unknown interface %s: %s", "%s/%s" % (name, descr), e)
                unknown_interfaces += [name]
                continue
            r[v] = index
        if unknown_interfaces:
            self.logger.info("%d unknown interfaces has been ignored", len(unknown_interfaces))
        return r
