# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Default workflow
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import bson
# NOC modules
from noc.core.migration.base import BaseMigration


class Migration(BaseMigration):
    def migrate(self):
        db = self.mongo_db
        # Workflow
        db["workflows"].insert_many(
            [
                {
                    "_id": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Default Resource",
                    "is_active": True,
                    "bi_id": 1099501303790147280,
                    "description": "Default resource workflow with external provisioning"
                }, {
                    "_id": bson.ObjectId("5a1d078e1bb627000151a17d"),
                    "name": "Default",
                    "is_active": True,
                    "bi_id": 4397582378950796294,
                    "description": "Default workflow with Ready state"
                }
            ]
        )
        # State
        db["states"].insert_many(
            [
                {
                    "_id": bson.ObjectId("5a17f61b1bb6270001bd0328"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Free",
                    "is_default": True,
                    "is_productive": False,
                    "update_last_seen": False,
                    "ttl": 0,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 5784899502721162850,
                    "description": "Resource is free and can be used"
                }, {
                    "_id": bson.ObjectId("5a17f6c51bb6270001bd0333"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Reserved",
                    "is_default": False,
                    "is_productive": False,
                    "update_last_seen": False,
                    "ttl": 604800,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 346135885535479406,
                    "description": "Resource is temporary reserved/booked. \
                                    It must be approved explicitly during TTL to became used"
                }, {
                    "_id": bson.ObjectId("5a17f7391bb6270001bd033e"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Cooldown",
                    "is_default": False,
                    "is_productive": False,
                    "update_last_seen": False,
                    "ttl": 2592000,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 5541827829820576149,
                    "description": "Cooldown stage for released resources to prevent reuse collisions"
                }, {
                    "_id": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Ready",
                    "is_default": False,
                    "is_productive": True,
                    "update_last_seen": False,
                    "ttl": 604800,
                    "update_expired": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 6326503631568495692,
                    "description": "Resource is in productive usage"
                }, {
                    "_id": bson.ObjectId("5a17f7d21bb6270001bd034f"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Approved",
                    "is_default": False,
                    "is_productive": False,
                    "update_last_seen": False,
                    "ttl": 0,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 6239532707574720775,
                    "description": "Resource reservation is approved. \
                                    Resource will became ready when it will be discovered"
                }, {
                    "_id": bson.ObjectId("5a17f7fc1bb6270001bd0359"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "name": "Suspended",
                    "is_default": False,
                    "is_productive": False,
                    "update_last_seen": False,
                    "ttl": 0,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 8871888520366972039,
                    "description": "Resource is temporary suspended/blocked for organisational reasons"
                }, {
                    "_id": bson.ObjectId("5a1d07b41bb627000151a18b"),
                    "workflow": bson.ObjectId("5a1d078e1bb627000151a17d"),
                    "name": "Ready",
                    "is_default": True,
                    "is_productive": True,
                    "update_last_seen": True,
                    "ttl": 0,
                    "update_expired": False,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 6481686024283854615,
                    "description": "Resource is in productive usage"
                }
            ]
        )
        # Transitions
        db["transitions"].insert_many(
            [
                {
                    "_id": bson.ObjectId("5a1813e41bb6270001c70309"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f61b1bb6270001bd0328"),
                    "to_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "is_active": True,
                    "label": "Seen",
                    "event": "seen",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 8800448533721856912
                }, {
                    "_id": bson.ObjectId("5a18140b1bb6270001c7031c"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f61b1bb6270001bd0328"),
                    "to_state": bson.ObjectId("5a17f6c51bb6270001bd0333"),
                    "is_active": True,
                    "label": "Reserve",
                    "event": "reserve",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 7126984897086158544
                }, {
                    "_id": bson.ObjectId("5a18146a1bb6270001c70332"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f6c51bb6270001bd0333"),
                    "to_state": bson.ObjectId("5a17f61b1bb6270001bd0328"),
                    "is_active": True,
                    "label": "Expired",
                    "event": "expired",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 6910421850576189953
                }, {
                    "_id": bson.ObjectId("5a18152d1bb6270001c70352"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f6c51bb6270001bd0333"),
                    "to_state": bson.ObjectId("5a17f7d21bb6270001bd034f"),
                    "is_active": True,
                    "label": "Approve",
                    "event": "approve",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 1894890040029769162
                }, {
                    "_id": bson.ObjectId("5a1815701bb6270001c70373"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f7d21bb6270001bd034f"),
                    "to_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "is_active": True,
                    "label": "Seen",
                    "event": "seen",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 2205967151884564606
                }, {
                    "_id": bson.ObjectId("5a18161e1bb6270001028cd0"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "to_state": bson.ObjectId("5a17f7fc1bb6270001bd0359"),
                    "is_active": True,
                    "label": "Suspend",
                    "event": "suspend",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 1854285483372474455
                }, {
                    "_id": bson.ObjectId("5a1816591bb6270001028cf6"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f7fc1bb6270001bd0359"),
                    "to_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "is_active": True,
                    "label": "Resume",
                    "event": "resume",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 81389710212083104
                }, {
                    "_id": bson.ObjectId("5a1816c81bb6270001028d45"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "to_state": bson.ObjectId("5a17f7391bb6270001bd033e"),
                    "is_active": True,
                    "label": "Expired",
                    "event": "expired",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 2244054006097306867
                }, {
                    "_id": bson.ObjectId("5a1816dd1bb6270001028d5f"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f7391bb6270001bd033e"),
                    "to_state": bson.ObjectId("5a17f78d1bb6270001bd0346"),
                    "is_active": True,
                    "label": "Seen",
                    "event": "seen",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 2585664142032130717
                }, {
                    "_id": bson.ObjectId("5a1817071bb6270001028d7e"),
                    "workflow": bson.ObjectId("5a01d980b6f529000100d37a"),
                    "from_state": bson.ObjectId("5a17f7391bb6270001bd033e"),
                    "to_state": bson.ObjectId("5a17f61b1bb6270001bd0328"),
                    "is_active": True,
                    "label": "Expired",
                    "event": "expired",
                    "enable_manual": True,
                    "on_enter_handlers": [],
                    "on_leave_handlers": [],
                    "bi_id": 8194239664781898089
                }
            ]
        )

