# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# KBEntryPreviewLog
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db import models
# NOC modules
from noc.core.model.base import NOCModel
from noc.aaa.models.user import User
from noc.kb.models.kbentry import KBEntry


class KBEntryPreviewLog(NOCModel):
    """
    Preview Log
    """
    class Meta(object):
        verbose_name = "KB Entry Preview Log"
        verbose_name_plural = "KB Entry Preview Log"
        app_label = "kb"
        db_table = "kb_kbentrypreviewlog"

    kb_entry = models.ForeignKey(KBEntry, verbose_name="KB Entry", on_delete=models.CASCADE)
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
