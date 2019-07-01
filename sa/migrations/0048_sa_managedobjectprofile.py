# ----------------------------------------------------------------------
# sa managedobjectprofile
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    depends_on = [("main", "0027_style")]

    def migrate(self):
        Style = self.db.mock_model(
            model_name="Style",
            db_table="main_style"
        )
        self.db.create_table(
            'sa_managedobjectprofile',
            (
                ('id', models.AutoField(primary_key=True)),
                ('name', models.CharField("Name", max_length=64, unique=True)),
                ('description', models.TextField("Description", blank=True, null=True)),
                ('style', models.ForeignKey(Style, verbose_name="Style", blank=True, null=True, on_delete=models.CASCADE)),
                # Name restrictions
                # Regular expression to check name format
                ('name_template', models.CharField("Name template", max_length=256, blank=True, null=True)),
                # @todo: Name validation function
                # FM settings
                ('enable_ping', models.BooleanField("Enable ping check", default=True)),
                # Host down alarm severity
                # Default impact is MAJOR/4000
                ('down_severity', models.IntegerField("Down severity", default=4000)),
                # Config polling
                ('enable_config_polling', models.BooleanField("Enable config polling", default=True)),
                ('config_polling_min_interval', models.IntegerField("Min. config polling interval", default=600)),
                ('config_polling_max_interval', models.IntegerField("Max. config polling interval", default=86400)),
                # Discovery settings
                # Version inventory
                ('enable_version_inventory', models.BooleanField("Enable version inventory", default=True)),
                ('version_inventory_min_interval', models.IntegerField("Min. version inventory interval", default=600)),
                (
                    'version_inventory_max_interval',
                    models.IntegerField("Max. version inventory interval", default=86400)
                ),
                # Interface discovery
                ('enable_interface_discovery', models.BooleanField("Enable interface discovery", default=True)),
                (
                    'interface_discovery_min_interval',
                    models.IntegerField("Min. interface discovery interval", default=600)
                ),
                (
                    'interface_discovery_max_interval',
                    models.IntegerField("Max. interface discovery interval", default=86400)
                ),
                # IP discovery
                ('enable_ip_discovery', models.BooleanField("Enable IP discovery", default=True)),
                ('ip_discovery_min_interval', models.IntegerField("Min. IP discovery interval", default=600)),
                ('ip_discovery_max_interval', models.IntegerField("Max. IP discovery interval", default=86400)),
                # Prefix discovery
                ('enable_prefix_discovery', models.BooleanField("Enable prefix discovery", default=True)),
                ('prefix_discovery_min_interval', models.IntegerField("Min. prefix discovery interval", default=600)),
                ('prefix_discovery_max_interval', models.IntegerField("Max. prefix discovery interval", default=86400)),
                # MAC discovery
                ('enable_mac_discovery', models.BooleanField("Enable MAC discovery", default=True)),
                ('mac_discovery_min_interval', models.IntegerField("Min. MAC discovery interval", default=600)),
                ('mac_discovery_max_interval', models.IntegerField("Max. MAC discovery interval", default=86400))
            )
        )
