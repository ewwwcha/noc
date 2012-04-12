# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Huawei.VRP.get_version test
## Auto-generated by ./noc debug-script at 09.04.2012 18:22:35
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Huawei_VRP_get_version_Test(ScriptTestCase):
    script = "Huawei.VRP.get_version"
    vendor = "Huawei"
    platform = "S9303"
    version = "5.70"
    input = {}
    result = {'attributes': {'image': 'V100R003C00SPC200'},
 'platform': 'Quidway S9303',
 'vendor': 'Huawei',
 'version': '5.70'}
    motd = '\nInfo: The max number of VTY users is 10, and the number\n      of current VTY users on line is 1.\n'
    cli = {
'screen-length 0 temporary':  'screen-length 0 temporary\nInfo: The configuration takes effect on the current user terminal interface only.\n', 
}
    snmp_get = {'1.3.6.1.2.1.1.1.0': 'Quidway S9303\r\nHuawei Versatile Routing Platform Software\r\nVRP (R) Software, Version 5.70 (S9300 V100R003C00SPC200)\r\nCopyright (c) 2003-2010 Huawei Technologies Co., Ltd\r\n'}
    snmp_getnext = {}
    http_get = {}
