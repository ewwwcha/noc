# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# as, asset, peer tags
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.model.fields import AutoCompleteTagsField
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    TAG_MODELS = ["peer_as", "peer_asset", "peer_peer"]

    def migrate(self):
        for m in self.TAG_MODELS:
            db.add_column(m, "tags", AutoCompleteTagsField("Tags", null=True, blank=True))
