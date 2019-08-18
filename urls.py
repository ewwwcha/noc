# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Django URL dispatcher.
# ---------------------------------------------------------------------
# Copyright (C) 2007-2016 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.conf.urls import url
from django.http import HttpResponseServerError
from django.views.i18n import JavaScriptCatalog

# NOC modules
from noc.lib.app.site import site
from noc.core.debug import error_report

#
# Discover all applications
#
site.autodiscover()
#
# Install URL handlers, including django's translations
#
urlpatterns = site.urls + [
    url(r"^jsi18n/$", JavaScriptCatalog.as_view(), name="javascript-catalog")
]


def handler500(request):
    error_report()
    return HttpResponseServerError("Internal Server Error")
