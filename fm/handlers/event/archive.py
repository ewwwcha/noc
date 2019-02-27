# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Mark Archive Event when close
#  Rules handlers
# ----------------------------------------------------------------------
#  Copyright (C) 2007-2019 The NOC Project
#  See LICENSE for details
# ----------------------------------------------------------------------


def handler(event):
    event.mark_as_archived("Close event")
