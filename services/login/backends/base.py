# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Authentication Backends
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import os
import logging
from threading import Lock
import operator
import inspect
# Third-party modules
import cachetools
from noc.config import config

id_lock = Lock()


class BaseAuthBackend(object):
    class LoginError(Exception):
        pass

    _methods = {}

    def __init__(self, service):
        self.service = service
        self.logger = logging.getLogger("auth")

    def authenticate(self, **kwargs):
        """
        Authenticate user using given credentials.
        Raise LoginError when failed
        """
        raise self.LoginError()

    def change_credentials(self, **kwargs):
        """
        Change credentials.
        Raise LoginError when failed
        """
        raise NotImplementedError

    def ensure_user(self, username, is_active=True,
                    first_name=None, last_name=None, email=None,
                    **kwargs):
        from noc.main.models.user import User

        changed = False
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            self.logger.info("Creating local user %s", username)
            u = User(
                username=username,
                is_active=is_active
            )
            u.set_unusable_password()
            changed = True
        for k, v in [
            ("is_active", is_active),
            ("first_name", first_name),
            ("last_name", last_name),
            ("email", email)
        ]:
            cv = getattr(u, k)
            if cv != v and v is not None:
                self.logger.info(
                    "Changing user %s %s: %s -> %s",
                    username, k, cv, v
                )
                setattr(u, k, v)
                changed = True
        # Check changes
        if changed:
            u.save()
        return u

    def _user_in_group(self, user, group):
        return user.groups.filter(id=group.id).exists()

    def ensure_group(self, user, group):
        if not self._user_in_group(user, group):
            self.logger.info("Adding user %s to group %s",
                             user.username, group.name)
            user.groups.add(group)

    def deny_group(self, user, group):
        if self._user_in_group(user, group):
            self.logger.info("Removing user %s from group %s",
                             user.username, group.name)
            user.groups.remove(group)

    @classmethod
    @cachetools.cachedmethod(operator.attrgetter("_methods"), lock=lambda _: id_lock)
    def get_backend(cls, name):
        """
        Look for custom auth methods in custom and load it.
        First check if custom method with same name exists then use bundled one.
        :param name: param name
        :return: found auth method
        """
        m = None
        import logging
        logger = logging.getLogger(__name__)
        for p in config.get_customized_paths(""):
            if p:
                mm = "%s.services.login.backends.%s" % (os.path.basename(os.path.dirname(p)), name)
            else:
                mm = "noc.services.login.backends.%s" % name
            try:
                m = __import__(mm, {}, {}, "*")
                logger.debug("Successfuly imported %s", m)
            except ImportError as e:
                logger.debug("There was an error importing %s with %s %s", e, m, mm)
        if m is None:
            return None
        for a in dir(m):
            o = getattr(m, a)
            if (
                inspect.isclass(o) and
                issubclass(o, BaseAuthBackend) and
                o.__module__ == m.__name__
            ):
                return o
        return None
