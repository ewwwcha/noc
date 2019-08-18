# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Wait TT
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019, The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging
import datetime

# NOC modules
from noc.fm.models.utils import get_alarm
from noc.fm.models.ttsystem import TTSystem
from noc.core.scheduler.job import Job
from noc.config import config


logger = logging.getLogger(__name__)


def wait_tt(alarm_id):
    logger.info("[%s] Checking escalated TT", alarm_id)
    alarm = get_alarm(alarm_id)
    if alarm is None:
        logger.info("[%s] Missing alarm, skipping", alarm_id)
        return
    if alarm.status == "C":
        logger.info("[%s] Alarm is closed, skipping", alarm_id)
        return
    c_tt_name, c_tt_id = alarm.escalation_tt.split(":")
    cts = TTSystem.get_by_name(c_tt_name)
    if not cts:
        logger.error("Unknown TT system: %s", c_tt_name)
        return
    ti = None
    tts = cts.get_system()
    try:
        ti = tts.get_tt(c_tt_id)
    except tts.TTError as e:
        logger.error("Cannot get TT info: %s", e)
    if ti and ti["resolved"]:
        # Close alarm
        alarm.clear_alarm(
            "Closed by TT %s" % alarm.escalation_tt,
            ts=ti.get("close_ts", datetime.datetime.now()),
            force=True,
        )
    else:
        Job.retry_after(config.escalator.wait_tt_check_interval, msg="Next check")
