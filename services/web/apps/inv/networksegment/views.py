# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# inv.networksegment application
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Third-party modules
from django.db.models import Count

# NOC modules
from noc.lib.app.extdocapplication import ExtDocApplication, view
from noc.inv.models.networksegment import NetworkSegment
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.useraccess import UserAccess
from noc.core.translation import ugettext as _


class NetworkSegmentApplication(ExtDocApplication):
    """
    NetworkSegment application
    """

    title = _("Network Segment")
    menu = [_("Setup"), _("Network Segments")]
    model = NetworkSegment
    query_fields = ["name__icontains", "description__icontains"]

    def field_row_class(self, o):
        return o.profile.style.css_class_name if o.profile.style else ""

    def queryset(self, request, query=None):
        qs = super(NetworkSegmentApplication, self).queryset(request, query)
        if not request.user.is_superuser:
            qs = qs.filter(adm_domains__in=UserAccess.get_domains(request.user))
        return qs

    def instance_to_lookup(self, o, fields=None):
        return {"id": str(o.id), "label": unicode(o), "has_children": o.has_children}

    def bulk_field_count(self, data):
        segments = [d["id"] for d in data]
        counts = dict(
            ManagedObject.objects.filter(segment__in=segments)
            .values("segment")
            .annotate(cnt=Count("segment"))
            .values_list("segment", "cnt")
        )
        for row in data:
            row["count"] = counts.get(row["id"], 0)
        return data

    @view("^(?P<id>[0-9a-f]{24})/get_path/$", access="read", api=True)
    def api_get_path(self, request, id):
        o = self.get_object_or_404(NetworkSegment, id=id)
        path = [NetworkSegment.get_by_id(ns) for ns in o.get_path()]
        return {
            "data": [
                {"level": level + 1, "id": str(p.id), "label": unicode(p.name)}
                for level, p in enumerate(path)
            ]
        }

    @view("^(?P<id>[0-9a-f]{24})/effective_settings/$", access="read", api=True)
    def api_effective_settings(self, request, id):
        o = self.get_object_or_404(NetworkSegment, id=id)
        return o.effective_settings
