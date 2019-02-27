# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# IGetAlarms - interface to get Alarm
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
from __future__ import absolute_import
from dateutil.parser import parse
import datetime
# NOC modules
from noc.core.interface.base import BaseInterface
from .base import (StringParameter, DateTimeParameter, DictListParameter)


class IGetAlarms(BaseInterface):
    """
    * alarm_id - Alarm id on device
    * object_id -- symbolic CPE name if get alarms on controller for cpe
    * type -- "alarm" type for classifier rule, if not classifier rule created "Unknown | Mobile | Alarm"
    * alarm_time - Time to create alarm message on device
    * alarm_name - Short Unique Alarm text
    * message - Full Alarm message
    * vars - Variables for different sorts of alarms
    """
    returns = DictListParameter(attrs={
        "object_id": StringParameter(required=False),
        "alarm_id": StringParameter(),
        "type": StringParameter(default="alarm"),
        "alarm_time": DateTimeParameter(default=parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
        "alarm_name": StringParameter(),
        "message": StringParameter(),
        "vars": StringParameter(required=False),

    })
