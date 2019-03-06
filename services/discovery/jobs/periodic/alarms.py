# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Alarms Check
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import time
import datetime
import cachetools
import operator
from threading import Lock
# NOC modules
from noc.core.nsq.pub import nsq_pub
from noc.services.discovery.jobs.base import DiscoveryCheck
from noc.sa.models.managedobject import ManagedObject
from noc.fm.models.activeevent import ActiveEvent

cpe_lock = Lock()


class AlarmsCheck(DiscoveryCheck):
    """
    CPE alarm discovery
    """
    name = "alarms"

    required_script = "get_alarms"
    _cpe_cache = cachetools.TTLCache(maxsize=50, ttl=60)

    def handler(self):
        mos = []
        self.logger.info("Checking Alarm CPEs")
        result = self.object.scripts.get_alarms()  # result get_alarms
        for r in result:
            if "object_id" in r:
                mos += [self.find_cpe(r["object_id"], self.object.id)]
            else:
                mos += [self.object]
        mos_id = list(set(mo.id for mo in mos if mo))
        # Object Events
        object_events = {str(cpe["alarm_id"]): cpe for cpe in result}
        # System Events
        system_events = {str(a.raw_vars["alarm_id"]): a
                         for a in ActiveEvent.objects.filter(managed_object__in=mos_id, source="other",
                                                             raw_vars__alarm_id__exists=True,
                                                             raw_vars__status="Open")}
        # Search object alarms in system events, if object alarms not in system events, create!
        create_objects_events = set(object_events.keys()).difference(set(system_events.keys()))
        # Search system events in object alarms, if system events not in object alarms, close event!
        close_objects_events = set(system_events.keys()).difference(set(object_events.keys()))
        # If not new/old alarms, return.
        if not create_objects_events and not close_objects_events:
            self.logger.debug("No New or Old Events")
            return
        if create_objects_events:
            self.logger.debug("Create event")
            for new_event in create_objects_events:
                if "object_id" in object_events[new_event]:
                    managed_object = self.find_cpe(object_events[new_event]["object_id"], self.object.id)
                    if not managed_object:
                        managed_object = self.object
                        self.logger.warning("No object %s for alarm: \n%s" % (object_events[new_event]["object_id"],
                                                                              object_events[new_event]))
                else:
                    managed_object = self.object
                raw_vars = object_events[new_event]
                raw_vars["status"] = "Open"
                self.raise_event(self.logger, managed_object.id, managed_object.pool.name, raw_vars)
        if close_objects_events:
            self.logger.debug("Close event")
            for close_event in close_objects_events:
                event = system_events[close_event]
                raw_vars = event.raw_vars
                raw_vars["status"] = "Close"
                self.raise_event(self.logger, event.managed_object.id, event.managed_object.pool.name, raw_vars)
                event.mark_as_archived("Close event")
                self.logger.info("Close event %s" % event)

    @cachetools.cachedmethod(operator.attrgetter("_cpe_cache"), lock=lambda _: cpe_lock)
    def find_cpe(self, id, co_id=None):
        mo = ManagedObject.objects.filter(local_cpe_id=id, controller=co_id)[:1]
        if mo:
            return mo[0]
        return None

    @classmethod
    def raise_event(cls, log, mo_id, pool_name, raw_vars):
        d = datetime.datetime.strptime(raw_vars["alarm_time"], '%Y-%m-%dT%H:%M:%S')
        ts = time.mktime(d.timetuple())
        msg = {
            "ts": ts,
            "object": mo_id,
            "source": "other",
            "data": raw_vars
        }
        object_name = raw_vars.get("object_id")
        if object_name:
            log.info("%s: Pub Event: %s", object_name, msg)
        else:
            log.info("Pub Event: %s", msg)
        nsq_pub("events.%s" % pool_name, msg)
