# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Local user
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# Third-party modules
import six

# NOC modules
from .base import BaseFact


@six.python_2_unicode_compatible
class User(BaseFact):
    ATTRS = ["name", "level", "[groups]"]
    ID = ["name"]

    def __init__(self, name=None, level=None, groups=None):
        super(User, self).__init__()
        self.name = name
        self.level = level
        self.groups = groups

    def __str__(self):
        return "User %s" % self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value or None

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = value or []
