# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Checkpoint model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
# Third-party modules
import six
from django.db import models
# NOC modules
from noc.core.model.base import NOCModel
from noc.aaa.models.user import User


@six.python_2_unicode_compatible
class Checkpoint(NOCModel):
    """
    Checkpoint is a marked moment in time
    """
    class Meta(object):
        app_label = "main"
        db_table = "main_checkpoint"
        verbose_name = "Checkpoint"
        verbose_name_plural = "Checkpoints"

    timestamp = models.DateTimeField("Timestamp")
    user = models.ForeignKey(User, verbose_name="User", blank=True, null=True, on_delete=models.CASCADE)
    comment = models.CharField("Comment", max_length=256)
    private = models.BooleanField("Private", default=False)

    def __str__(self):
        if self.user:
            return u"%s[%s]: %s" % (self.timestamp, self.user.username,
                                    self.comment)

    @classmethod
    def set_checkpoint(cls, comment, user=None, timestamp=None, private=True):
        if not timestamp:
            timestamp = datetime.datetime.now()
        cp = Checkpoint(timestamp=timestamp, user=user, comment=comment,
                        private=private)
        cp.save()
        return cp
