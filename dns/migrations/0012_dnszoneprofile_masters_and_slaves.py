# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnszoneprofile masters and slaves
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from south.db import db
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        # Mock Models
        DNSZoneProfile = db.mock_model(
            model_name='DNSZoneProfile',
            db_table='dns_dnszoneprofile',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        DNSServer = db.mock_model(
            model_name='DNSServer',
            db_table='dns_dnsserver',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # M2M field 'DNSZoneProfile.masters'
        db.create_table(
            'dns_dnszoneprofile_masters', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('dnszoneprofile', models.ForeignKey(DNSZoneProfile, null=False)),
                ('dnsserver', models.ForeignKey(DNSServer, null=False))
            )
        )
        # Mock Models
        DNSZoneProfile = db.mock_model(
            model_name='DNSZoneProfile',
            db_table='dns_dnszoneprofile',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )
        DNSServer = db.mock_model(
            model_name='DNSServer',
            db_table='dns_dnsserver',
            db_tablespace='',
            pk_field_name='id',
            pk_field_type=models.AutoField
        )

        # M2M field 'DNSZoneProfile.slaves'
        db.create_table(
            'dns_dnszoneprofile_slaves', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('dnszoneprofile', models.ForeignKey(DNSZoneProfile, null=False)),
                ('dnsserver', models.ForeignKey(DNSServer, null=False))
            )
        )
        db.execute(
            """INSERT INTO dns_dnszoneprofile_masters(dnszoneprofile_id,dnsserver_id)
               SELECT dnszoneprofile_id,dnsserver_id
               FROM dns_dnszoneprofile_ns_servers"""
        )
        db.delete_table('dns_dnszoneprofile_ns_servers')
