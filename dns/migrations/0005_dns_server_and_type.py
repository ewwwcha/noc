# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# dnsserver and type
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

        # Model 'DNSServer'
        db.create_table(
            'dns_dnsserver', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField("Name", max_length=64, unique=True)),
                ('description', models.CharField("Description", max_length=128, blank=True, null=True)),
                ('location', models.CharField("Location", max_length=128, blank=True, null=True))
            )
        )
        # M2M field 'DNSZoneProfile.ns_servers'
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
        db.create_table(
            'dns_dnszoneprofile_ns_servers', (
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
                ('dnszoneprofile', models.ForeignKey(DNSZoneProfile, null=False)),
                ('dnsserver', models.ForeignKey(DNSServer, null=False))
            )
        )
