# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Update segment summary
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.inv.models.networksegment import NetworkSegment


def fix():
    for ns in NetworkSegment.objects.all():
        NetworkSegment.update_summary(ns)
