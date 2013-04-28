# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## Obsolete data cleanup and system maintainance
##----------------------------------------------------------------------
## Copyright (C) 2007-2011 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Python modules
import logging
import os
import subprocess
import datetime
## NOC modules
import noc.lib.periodic
from noc.settings import config


class Task(noc.lib.periodic.Task):
    name = "main.cleanup"
    description = "Obsolete data cleanup and system maintainance"

    def cleanup_expired_sessions(self):
        """
        Delete expired sessions
        """
        from mongoengine.django.sessions import MongoSession

        self.info("Cleaning expired sessions")
        MongoSession.objects.filter(
            expire_date__lt=datetime.datetime.now()).delete()
        self.info("Expired sessions are cleaned")

    def cleanup_mrt(self):
        """
        Remove old map/reduce tasks
        """
        from noc.sa.models import ReduceTask, MapTask
        from noc.lib.db import vacuum

        self.info("Cleanup map/reduce tasks")
        watermark = datetime.datetime.now() - datetime.timedelta(days=1)
        for t in ReduceTask.objects.filter(stop_time__lt=watermark):
            t.delete()
        self.info("Map/Reduce tasks are cleaned")
        self.info("Compacting MRT tables")
        vacuum(ReduceTask._meta.db_table, analyze=True)
        vacuum(MapTask._meta.db_table, analyze=True)
        self.info("MRT Tables are compacted")

    def cleanup_empty_categories(self):
        """
        Cleanup empty categories
        """
        from noc.fm.models import AlarmClass, AlarmClassCategory,\
            EventClass, EventClassCategory, EventClassificationRule,\
            EventClassificationRuleCategory
        
        self.info("Cleaning empty categories")
        for cls, cat_cls in [(AlarmClass, AlarmClassCategory),
                             (EventClass, EventClassCategory),
                             (EventClassificationRule,
                              EventClassificationRuleCategory)]:
            
            for cat in cat_cls.objects.all().order_by("-name"):
                if cls.objects.filter(category=cat.id).count():
                    # There are child items
                    continue
                if cat_cls.objects.filter(parent=cat.id).count():
                    # There are
                    continue
                logging.info("Cleaning %s category: %s" % (cls, cat))
                cat.delete()
        self.info("Empty categories are cleaned")

    def cleanup_failed_script_log(self):
        from noc.sa.models.failedscriptlog import FailedScriptLog
        d = datetime.datetime.now() - datetime.timedelta(days=7)
        self.info("Cleaning failed scripts log")
        FailedScriptLog.objects.filter(timestamp__lte=d).delete()
        self.info("Failed scripts logs are cleaned")

    def execute(self):
        self.cleanup_expired_sessions()
        self.cleanup_mrt()
        self.cleanup_empty_categories()
        self.cleanup_failed_script_log()
        return True
