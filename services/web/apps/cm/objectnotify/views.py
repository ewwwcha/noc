# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ObjectNotify Manager
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
# from django.contrib import admin
# NOC modules
from noc.lib.app.extmodelapplication import ExtModelApplication
from noc.cm.models.objectnotify import ObjectNotify
from noc.core.translation import ugettext as _


# class ObjectNotifyAdmin(admin.ModelAdmin):
#     list_display = ["type", "administrative_domain", "notify_immediately", "notify_delayed", "notification_group"]
#     list_filter = ["type", "administrative_domain", "notification_group"]


class ObjectNotifyApplication(ExtModelApplication):

    title = _("Object Notifies")
    menu = [_("Setup"), _("Object Notifies")]
    glyph = "flag-o"
    model = ObjectNotify
    # model_admin = ObjectNotifyAdmin
