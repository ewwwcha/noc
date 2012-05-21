# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Huawei.VRP.get_portchannel test
## Auto-generated by ./noc debug-script at 21.05.2012 10:15:49
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Huawei_VRP_get_portchannel_Test(ScriptTestCase):
    script = "Huawei.VRP.get_portchannel"
    vendor = "Huawei"
    platform = "S2326TP-SI"
    version = "5.30"
    input = {}
    result = []
    motd = ''
    cli = {
'screen-length 0 temporary':  "screen-length 0 temporary\n                ^\nError:Unrecognized command found at '^' position.\n", 
## 'display version'
'display version': """display version
Huawei Versatile Routing Platform Software
VRP (R) Software, Version 5.30 (S2300 V100R003C00SPC200)
Copyright (C) 2008-2009 Huawei Technologies Co., Ltd.
Quidway S2326TP-SI uptime is 203 days, 23 hours, 12 minutes


[Unit 0] EFFED uptime is 203 days, 23 hours, 12 minutes
Startup time :2008/01/01 00:00:25
64M bytes DDR Memory
16M bytes FLASH
Pcb      Version : CX22EFFED REV C
Basic  BOOTROM  Version :  128 Compiled at Aug 19 2009, 20:20:35
Software Version : VRP (R) Software, Version 5.30 (S2300 V100R003C00SPC200)""", 
'display eth-trunk':  'display eth-trunk\nError: No valid trunk in the system.\n\n', 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
