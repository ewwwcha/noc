# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## NSN.hiX56xx.get_vlans test
## Auto-generated by ./noc debug-script at 28.02.2012 16:52:00
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class NSN_hiX56xx_get_vlans_Test(ScriptTestCase):
    script = "NSN.hiX56xx.get_vlans"
    vendor = "NSN"
    platform = "hiX5630"
    version = "R2.8"
    input = {}
    result = [{'name': '<noname>', 'vlan_id': 1},
 {'name': '<noname>', 'vlan_id': 21},
 {'name': '<noname>', 'vlan_id': 104},
 {'name': '<noname>', 'vlan_id': 105},
 {'name': '<noname>', 'vlan_id': 106},
 {'name': '<noname>', 'vlan_id': 107},
 {'name': 'PPPoE', 'vlan_id': 393},
 {'name': '<noname>', 'vlan_id': 1612}]
    motd = ''
    cli = {
'terminal no length':  ' terminal no length\n', 
'terminal length 0':  ' terminal length 0\n', 
## 'show vlan properties'
'show vlan properties': """ show vlan properties
---------------------------------------------------------------------------
      | name
      |--------------------------------------------------------------------
 Vlan |  DHCP/   | service   | cross | ip    | multi | mac   | mgmt | x-  
 ID   | PPPoE    | type      | mode  | rout- | cast  | adr   | vlan | lat-
      | provider |           |       | ing   | flood | trans |      | ion 
---------------------------------------------------------------------------
 1    | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | routing mode: default(residential)
 21   | <noname>
      |      0/0   double      off     off     off     off     no     off 
      | routing mode: default(residential)
 104  | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | routing mode: default(residential)
 105  | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | routing mode: default(residential)
 106  | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | routing mode: default(residential)
 107  | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | routing mode: default(residential)
 393  | PPPoE
      |      0/1   double      off     off     off     off     no     off 
      | routing mode: default(residential)
 1612 | <noname>
      |      0/0   stacked     off     off     off     off     no     off 
      | locked by: extern: IGMP (absolute)
      | routing mode: default(residential)""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
