# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Missed MIBs Report
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.lib.app.simplereport import SimpleReport, TableColumn
from noc.fm.models.eventclass import EventClass
from noc.fm.models.activeevent import ActiveEvent
from noc.fm.models.mib import MIB
from noc.core.translation import ugettext as _


class ReportMissedMIBs(SimpleReport):
    title = _("Missed MIBs")

    rx_unclassified = re.compile(r"\.\d+$")

    def get_data(self, **kwargs):
        c = EventClass.objects.filter(name="Unknown | SNMP Trap").first()
        # Переделать на agregate Функция считает число OID'ов в переменных аварий
        # и проверяет их на опознанность
        pipeline = [
            {"$match": {"event_class": c.id}},
            {"$project": {"vars": 1}},
            {"$group": {"_id": "$vars.trap_oid", "count": {"$sum": 1}}},
        ]
        oids = ActiveEvent._get_collection().aggregate(pipeline)
        d = [(e["_id"], MIB.get_name(e["_id"]), e["count"]) for e in oids]
        data = [(o, n, cc) for o, n, cc in d if self.rx_unclassified.search(n)]
        return self.from_dataset(
            title=self.title,
            columns=[
                "OID",
                "Name",
                TableColumn("Count", format="integer", align="right", total="sum"),
            ],
            data=data,
        )
