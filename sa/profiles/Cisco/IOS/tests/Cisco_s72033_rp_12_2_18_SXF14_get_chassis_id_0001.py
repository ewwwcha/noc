# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Cisco.IOS.get_chassis_id test
## Auto-generated by manage.py debug-script at 2010-12-15 13:06:30
##----------------------------------------------------------------------
## Copyright (C) 2007-2010 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from noc.lib.test import ScriptTestCase
class Cisco_IOS_get_chassis_id_Test(ScriptTestCase):
    script="Cisco.IOS.get_chassis_id"
    vendor="Cisco"
    platform='s72033_rp'
    version='12.2(18)SXF14'
    input={}
    result='00:14:1B:33:1C:C0'
    motd=' \n\n'
    cli={
'show catalyst6000 chassis-mac-addresses':  'show catalyst6000 chassis-mac-addresses\n  chassis MAC addresses: 64 addresses from 0014.1b33.1cc0 to 0014.1b33.1cff\n',
## 'show version'
'show version': """show version
Cisco Internetwork Operating System Software 
IOS (tm) s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF14, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2008 by cisco Systems, Inc.
Compiled Thu 08-May-08 01:44 by kellythw
Image text-base: 0x40101040, data-base: 0x42DD1530

ROM: System Bootstrap, Version 12.2(17r)S2, RELEASE SOFTWARE (fc1)
BOOTLDR: s72033_rp Software (s72033_rp-ADVENTERPRISEK9_WAN-M), Version 12.2(18)SXF14, RELEASE SOFTWARE (fc1)

c6513xxx uptime is 2 years, 13 weeks, 20 hours, 7 minutes
Time since c6513eu1 switched to active is 2 years, 13 weeks, 20 hours, 12 minutes
System returned to ROM by  power cycle at 14:50:21 GMT Sun Sep 14 2008 (SP by power on)
System restarted at 14:53:25 GMT Sun Sep 14 2008
System image file is "disk0:s72033-adventerprisek9_wan-mz.122-18.SXF14.bin"


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

cisco WS-C6513 (R7000) processor (revision 1.0) with 458720K/65536K bytes of memory.
Processor board ID SAL09211PQ3
SR71000 CPU at 600Mhz, Implementation 0x504, Rev 1.2, 512KB L2 Cache
Last reset from power-on
SuperLAT software (copyright 1990 by Meridian Technology Corp).
X.25 software, Version 3.0.0.
Bridging software.
TN3270 Emulation software.
64 Virtual Ethernet/IEEE 802.3 interfaces
68 Gigabit Ethernet/IEEE 802.3 interfaces
8 Ten Gigabit Ethernet/IEEE 802.3 interfaces
1917K bytes of non-volatile configuration memory.
8192K bytes of packet buffer memory.

65536K bytes of Flash internal SIMM (Sector size 512K).
Configuration register is 0x2102
""",
'terminal length 0':  'terminal length 0\n',
}
    snmp_get={}
    snmp_getnext={}
