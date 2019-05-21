# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Migrate InterfaceProfile threshold profiles
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import itertools
# Third-party modules
import bson
import psycopg2
import cachetools
from six.moves.cPickle import loads, dumps, HIGHEST_PROTOCOL
# NOC modules
from noc.core.migration.base import BaseMigration
from noc.lib.nosql import get_db


class Migration(BaseMigration):
    _ac_cache = cachetools.TTLCache(maxsize=5, ttl=60)

    def migrate(self):
        # Convert pickled field ty BYTEA
        self.db.execute("ALTER TABLE sa_managedobjectprofile ALTER metrics TYPE BYTEA USING metrics::bytea")
        #
        current = itertools.count()
        mdb = get_db()
        # Migrate profiles
        tp_coll = mdb["thresholdprofiles"]
        settings = self.db.execute("SELECT id, name, metrics FROM sa_managedobjectprofile")
        for p_id, name, p_metrics in settings:
            if not p_metrics:
                continue
            metrics = loads(str(p_metrics)) or []
            changed = [m for m in metrics if self.has_thresholds(m)]
            if not changed:
                continue
            for n, metric in enumerate(changed):
                tp_id = bson.ObjectId()
                if metric.get("threshold_profile"):
                    # Extend existent threshold profile
                    tp = tp_coll.find_one({"_id": metric["threshold_profile"]})
                    assert tp, "Broken threshold profile"
                    tp["_id"] = tp_id
                else:
                    tp = {"_id": tp_id}
                # Fill profile
                tp["name"] = "op14-%05d-%03d" % (next(current), n)
                tp["description"] = "Migrated for interface profile '%s' metric '%s'" % (name, metric["metric_type"])
                tp["window_type"] = metric.get("window_type")
                tp["window"] = metric.get("window")
                tp["window_function"] = metric.get("window_function")
                tp["window_config"] = metric.get("window_config")
                # Build thresholds
                tp["thresholds"] = []
                if metric.get("high_error", False) or metric.get("high_error", False) == 0:
                    tp["thresholds"] += [
                        {
                            "op": ">=",
                            "value": metric["high_error"],
                            "clear_op": "<",
                            "clear_value": metric["high_error"],
                            "alarm_class": self.get_alarm_class_id("NOC | PM | High Error")
                        }
                    ]
                if metric.get("low_error", False) or metric.get("low_error", False) == 0:
                    tp["thresholds"] += [
                        {
                            "op": "<=",
                            "value": metric["low_error"],
                            "clear_op": ">",
                            "clear_value": metric["low_error"],
                            "alarm_class": self.get_alarm_class_id("NOC | PM | Low Error")
                        }
                    ]
                if metric.get("low_warn", False) or metric.get("low_warn", False) == 0:
                    tp["thresholds"] += [
                        {
                            "op": "<=",
                            "value": metric["low_warn"],
                            "clear_op": ">",
                            "clear_value": metric["low_warn"],
                            "alarm_class": self.get_alarm_class_id("NOC | PM | Low Warning")
                        }
                    ]
                if metric.get("high_warn", False) or metric.get("high_warn", False) == 0:
                    tp["thresholds"] += [
                        {
                            "op": ">=",
                            "value": metric["high_warn"],
                            "clear_op": "<",
                            "clear_value": metric["high_warn"],
                            "alarm_class": self.get_alarm_class_id("NOC | PM | High Warning")
                        }
                    ]
                # Save profile
                tp_coll.insert_one(tp)
                #
                metric["threshold_profile"] = str(tp_id)
            # Store back
            wb_metrics = psycopg2.Binary(dumps(metrics, HIGHEST_PROTOCOL))
            self.db.execute("UPDATE sa_managedobjectprofile SET metrics=%s WHERE id=%s", [wb_metrics, p_id])
