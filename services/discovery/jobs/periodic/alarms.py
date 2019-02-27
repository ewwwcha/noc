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
# NOC modules
from noc.core.nsq.pub import nsq_pub
from noc.services.discovery.jobs.base import DiscoveryCheck
from noc.sa.models.managedobject import ManagedObject
from noc.fm.models.activeevent import ActiveEvent


class AlarmsCheck(DiscoveryCheck):
    """
    CPE alarm discovery
    """
    name = "alarms"

    required_script = "get_alarms"

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
        # Controller Alarm
        objcet_alarms = {str(cpe["alarm_id"]): cpe for cpe in result}
        # System Events
        system_alarms = {str(a.raw_vars["alarm_id"]): a for a in ActiveEvent.objects.filter(managed_object__in=mos_id,
                                                                                            source="other",
                                                                                            raw_vars__alarm_id__exists=True,
                                                                                            raw_vars__status="Open")}
        # Search objcet alarms in system events, if objcet alarms not in system events, create!
        create_objcet_alarms = set(objcet_alarms.keys()).difference(set(system_alarms.keys()))
        # Search system events in objcet alarms, if system events not in objcet alarms, close event!
        close_objects_event = set(system_alarms.keys()).difference(set(objcet_alarms.keys()))
        # If not new/old alarms, return.
        if len(create_objcet_alarms) == 0 and len(close_objects_event) == 0:
            self.logger.debug("No New or Old Alarms")
            return
        if len(create_objcet_alarms) != 0:
            for new_event in create_objcet_alarms:
                if "object_id" in objcet_alarms[new_event]:
                    managed_object = self.find_cpe(objcet_alarms[new_event]["object_id"], self.object.id)
                    if not managed_object:
                        managed_object = self.object
                        self.logger.warning("No object %s for alarm: \n%s" % (objcet_alarms[new_event]["object_id"],
                                                                              objcet_alarms[new_event]))
                else:
                    managed_object = self.object
                raw_vars = objcet_alarms[new_event]
                raw_vars["status"] = "Open"
                self.raise_event(self.logger, managed_object.id, managed_object.pool.name, raw_vars)
        if len(close_objects_event) != 0:
            for close_event in close_objects_event:
                event = system_alarms[close_event]
                raw_vars = event.raw_vars
                raw_vars["status"] = "Close"
                self.raise_event(self.logger, event.managed_object.id, event.managed_object.pool.name, raw_vars)
                event.mark_as_archived("Close event")
                self.logger.info("Close event %s" % event)

    @classmethod
    def find_cpe(cls, name, co_id=None):
        try:
            return ManagedObject.objects.get(name=name, controller=co_id)
        except ManagedObject.DoesNotExist:
            return None

    @classmethod
    def raise_event(self, log, mo_id, pool_name, raw_vars):
        d = datetime.datetime.strptime(raw_vars["alarm_time"], '%Y-%m-%dT%H:%M:%S')
        ts = time.mktime(d.timetuple())
        msg = {
            "ts": ts,
            "object": mo_id,
            "source": "other",
            "data": raw_vars
        }
        log.info("Pub Event: %s", msg)
        nsq_pub("events.%s" % pool_name, msg)
