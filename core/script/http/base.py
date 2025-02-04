# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# HTTP methods implementation
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import ujson
from six.moves.http_cookies import SimpleCookie

# NOC modules
from noc.core.log import PrefixLoggerAdapter
from noc.core.http.client import fetch_sync
from noc.core.error import NOCError, ERR_HTTP_UNKNOWN
from noc.core.handler import get_handler
from .middleware.base import BaseMiddleware
from .middleware.loader import loader


class HTTPError(NOCError):
    default_code = ERR_HTTP_UNKNOWN


class HTTP(object):
    HTTPError = HTTPError

    def __init__(self, script):
        self.script = script
        if script:  # For testing purposes
            self.logger = PrefixLoggerAdapter(script.logger, "http")
        self.headers = {}
        self.cookies = None
        self.session_started = False
        self.request_id = 1
        self.session_id = None
        self.request_middleware = None
        if self.script:  # For testing purposes
            self.setup_middleware()

    def get_url(self, path):
        address = self.script.credentials["address"]
        port = self.script.credentials.get("http_port")
        if port:
            address += ":%s" % port
        proto = self.script.credentials.get("http_protocol", "http")
        return "%s://%s%s" % (proto, address, path)

    def get(self, path, headers=None, cached=False, json=False, eof_mark=None, use_basic=False):
        """
        Perform HTTP GET request
        :param path: URI
        :param headers: Dict of additional headers
        :param cached: Cache result
        :param json: Decode json if set to True
        :param eof_mark: Waiting eof_mark in stream for end session (perhaps device return length 0)
        :param use_basic: Use basic authentication
        """
        self.ensure_session()
        self.request_id += 1
        self.logger.debug("GET %s", path)
        if cached:
            cache_key = "get_%s" % path
            r = self.script.root.http_cache.get(cache_key)
            if r is not None:
                self.logger.debug("Use cached result")
                return r
        user, password = None, None
        if use_basic:
            user = self.script.credentials.get("user")
            password = self.script.credentials.get("password")
        # Apply GET middleware
        url = self.get_url(path)
        hdr = self._get_effective_headers(headers)
        if self.request_middleware:
            for mw in self.request_middleware:
                url, _, hdr = mw.process_get(url, "", hdr)
        code, headers, result = fetch_sync(
            url,
            headers=hdr,
            request_timeout=60,
            follow_redirects=True,
            allow_proxy=False,
            validate_cert=False,
            eof_mark=eof_mark,
            user=user,
            password=password,
        )
        if not 200 <= code <= 299:
            raise HTTPError(msg="HTTP Error (%s)" % result[:256], code=code)
        self._process_cookies(headers)
        if json:
            try:
                result = ujson.loads(result)
            except ValueError as e:
                raise HTTPError("Failed to decode JSON: %s", e)
        self.logger.debug("Result: %r", result)
        if cached:
            self.script.root.http_cache[cache_key] = result
        return result

    def post(
        self, path, data, headers=None, cached=False, json=False, eof_mark=None, use_basic=False
    ):
        """
        Perform HTTP GET request
        :param path: URI
        :param headers: Dict of additional headers
        :param cached: Cache result
        :param json: Decode json if set to True
        :param eof_mark: Waiting eof_mark in stream for end session (perhaps device return length 0)
        :param use_basic: Use basic authentication
        """
        self.ensure_session()
        self.request_id += 1
        self.logger.debug("POST %s %s", path, data)
        if cached:
            cache_key = "post_%s" % path
            r = self.script.root.http_cache.get(cache_key)
            if r is not None:
                self.logger.debug("Use cached result")
                return r
        user, password = None, None
        if use_basic:
            user = self.script.credentials.get("user")
            password = self.script.credentials.get("password")
        # Apply POST middleware
        url = self.get_url(path)
        hdr = self._get_effective_headers(headers)
        if self.request_middleware:
            for mw in self.request_middleware:
                url, data, hdr = mw.process_post(url, data, hdr)
        code, headers, result = fetch_sync(
            url,
            method="POST",
            body=data,
            headers=hdr,
            request_timeout=60,
            follow_redirects=True,
            allow_proxy=False,
            validate_cert=False,
            eof_mark=eof_mark,
            user=user,
            password=password,
        )
        if not 200 <= code <= 299:
            raise HTTPError(msg="HTTP Error (%s)" % result[:256], code=code)
        self._process_cookies(headers)
        if json:
            try:
                return ujson.loads(result)
            except ValueError as e:
                raise HTTPError(msg="Failed to decode JSON: %s" % e)
        self.logger.debug("Result: %r", result)
        if cached:
            self.script.root.http_cache[cache_key] = result
        return result

    def close(self):
        if self.session_started:
            self.shutdown_session()

    def _process_cookies(self, headers):
        """
        Process and store cookies from response headers
        :param headers:
        :return:
        """
        cdata = headers.get("Set-Cookie")
        if not cdata:
            return
        if not self.cookies:
            self.cookies = SimpleCookie()
        self.cookies.load(cdata)

    def get_cookie(self, name):
        """
        Get cookie name by value
        :param name:
        :return: Morsel object or None
        """
        if not self.cookies:
            return None
        return self.cookies.get(name)

    def _get_effective_headers(self, headers):
        """
        Append session headers when necessary. Apply effective cookies
        :param headers:
        :return:
        """
        if self.headers:
            if headers:
                headers = headers.copy()
            else:
                headers = {}
            headers.update(self.headers)
        elif not headers and self.cookies:
            headers = {}
        if self.cookies:
            headers["Cookie"] = self.cookies.output(header="").lstrip()
        return headers

    def set_header(self, name, value):
        """
        Set HTTP header to be set with all following requests
        :param name:
        :param value:
        :return:
        """
        self.logger.debug("Set header: %s = %s", name, value)
        self.headers[name] = str(value)

    def set_session_id(self, session_id):
        """
        Set session_id to be reused by middleware
        :param session_id:
        :return: None
        """
        if session_id is not None:
            self.session_id = session_id
        else:
            self.session_id = None

    def ensure_session(self):
        if not self.session_started:
            self.session_started = True
            self.setup_session()

    def setup_session(self):
        if self.script.profile.setup_http_session:
            self.logger.debug("Setup http session")
            self.script.profile.setup_http_session(self.script)

    def shutdown_session(self):
        if self.script.profile.shutdown_http_session:
            self.logger.debug("Shutdown http session")
            self.script.profile.shutdown_http_session(self.script)

    def setup_middleware(self):
        mw_list = self.script.profile.get_http_request_middleware(self.script)
        if not mw_list:
            return
        self.request_middleware = []
        for mw_cfg in mw_list:
            if isinstance(mw_cfg, tuple):
                name, cfg = mw_cfg
            else:
                name, cfg = mw_cfg, {}
            if "." in name:
                # Handler
                mw_cls = get_handler(name)
                assert mw_cls
                assert issubclass(mw_cls, BaseMiddleware)
            else:
                # Middleware name
                mw_cls = loader.get_class(name)
            self.request_middleware += [mw_cls(self, **cfg)]
