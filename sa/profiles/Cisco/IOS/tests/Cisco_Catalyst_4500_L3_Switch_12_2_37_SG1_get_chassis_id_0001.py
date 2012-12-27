# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_chassis_id test
## Auto-generated by ./noc debug-script at 27.12.2012 09:41:41
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## NOC modules
from noc.lib.test import ScriptTestCase


class Cisco_IOS_get_chassis_id_Test(ScriptTestCase):
    script = "Cisco.IOS.get_chassis_id"
    vendor = "Cisco"
    platform = "Catalyst 4500 L3 Switch"
    version = "12.2(37)SG1"
    input = {}
    result = {'first_chassis_mac': '00:1C:58:2F:44:80',
 'last_chassis_mac': '00:1C:58:2F:44:C0'}
    motd = ' \n\n'
    cli = {
## 'show version'
'show version': """show version
Cisco IOS Software, Catalyst 4500 L3 Switch Software (cat4500-IPBASEK9-M), Version 12.2(37)SG1, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2007 by Cisco Systems, Inc.
Compiled Mon 30-Jul-07 14:00 by prod_rel_team
Image text-base: 0x10000000, data-base: 0x1158DA3C

ROM: 12.2(31r)SG3
Pod Revision 14, Force Revision 31, Tie Revision 32

c4507xxxx uptime is 2 years, 13 weeks, 23 hours, 53 minutes
Uptime for this control processor is 2 years, 13 weeks, 22 hours, 34 minutes
System returned to ROM by power-on
System restarted at 10:11:54 UTC Sun Sep 14 2008
System image file is "bootflash:cat4500-ipbasek9-mz.122-37.SG1.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco WS-C4507R (MPC8540) processor (revision 4) with 524288K bytes of memory.
Processor board ID FOX11210LG6
MPC8540 CPU at 667Mhz, Supervisor II-PLUS-10GE
Last reset from PowerUp
14 Virtual Ethernet interfaces
200 Gigabit Ethernet interfaces
4 Ten Gigabit Ethernet interfaces
511K bytes of non-volatile configuration memory.

Configuration register is 0x2101""", 
'terminal length 0':  'terminal length 0\n', 
## 'show idprom chassis'
'show idprom chassis': """show idprom chassis
Chassis Idprom : 
 Common Block Signature = 0xABAB
 Common Block Version = 1
 Common Block Length = 144
 Common Block Checksum = 4223
 Idprom Size = 256
 Block Count = 3
 FRU Major Type = 0x4001
 FRU Minor Type = 35
 OEM String = Cisco Systems, Inc.
 Product Number = WS-C4507R
 Serial Number = FOX11210LG6
 Part Number = 73-6982-06
 Part Revision = C0
 Manufacturing Deviation String = 0
 Hardware Revision = 5.1
 Manufacturing Bits = 0x0000
 Engineering Bits = 0x0000
 Snmp OID = 0.0.0.0.0.0.0.0
 Power Consumption = 0
 RMA Failure Code = 0 0 0 0
 Chassis Block Signature = 0x4001
 Chassis Block Version = 1
 Chassis Block Length = 22
 Chassis Block Checksum = 511
 Feature Bits = 0x0000000000000000
 MAC Base = 001c.582f.4480
 MAC Count = 64
 Clei Block Signature = 0x4601
 Clei Block Version = 1
 Clei Block Length = 22
 Clei Block Checksum = 1020
 Clei code string = CNMVSS0CRB
 Version ID string = V07""", 
}
    snmp_get = {}
    snmp_getnext = {}
    http_get = {}
