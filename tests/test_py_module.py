# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Test python module loading
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import subprocess
import os
import ast

# Third-party modules
import pytest
import cachetools

ALLOW_XFAIL = {
    "noc.services.login.backends.pam",
    "noc.services.web.apps.kb.parsers.mediawiki",
    "noc.services.classifier.xrulelookup",
    "noc.commands.translation",
    "noc.scripts.build-pop-links",
    "noc.scripts.build-models",
    "noc.scripts.build.compile-handlebars",
    "noc.scripts.check-db",
    "noc.scripts.check-labels",
    "noc.scripts.paste",
    "noc.scripts.migrate-ignored-interfaces",
    "noc.gis.parsers.address.fias",
    "noc.gis.tile",
}


@cachetools.cached(cache={})
def get_files():
    def _get_files():
        try:
            data = subprocess.check_output(["git", "ls-tree", "HEAD", "-r", "--name-only"])
            return data.splitlines()
        except (OSError, subprocess.CalledProcessError):
            # No git, emulate
            data = subprocess.check_output(["find", ".", "-type", "f", "-print"])
            return [p[2:] for p in data.splitlines()]

    return [x for x in _get_files() if not x.startswith("docs")]


@cachetools.cached(cache={})
def get_py_modules_list():
    result = []
    for path in get_files():
        if path.startswith(".") or not path.endswith(".py"):
            continue
        parts = path.split(os.sep)
        if parts[0] == "tests" or path == "setup.py" or "tests" in parts:
            continue
        fn = parts[-1]
        if fn.startswith("."):
            continue
        if fn == "__init__.py":
            # Strip __init__.py
            parts = parts[:-1]
        else:
            # Strip .py
            parts[-1] = fn[:-3]
        result += [".".join(["noc"] + parts)]
    return result


@pytest.mark.parametrize("module", get_py_modules_list())
def test_import(module):
    try:
        m = __import__(module, {}, {}, "*")
        assert m
    except ImportError as e:
        if module in ALLOW_XFAIL:
            pytest.xfail(str(e))
        else:
            pytest.fail(str(e))


@pytest.mark.parametrize("module", get_py_modules_list())
def test_module_empty_docstrings(module):
    try:
        m = __import__(module, {}, {}, "*")
        if m.__doc__ is not None and not m.__doc__.strip():
            # assert m.__doc__.strip(), "Module-level docstring must not be empty"
            pytest.xfail("Module-level docstring must not be empty")
    except ImportError as e:
        if module in ALLOW_XFAIL:
            pytest.xfail(str(e))
        else:
            pytest.fail(str(e))


@pytest.mark.parametrize("path", [f for f in get_files() if f.endswith("__init__.py")])
def test_init(path):
    with open(path) as f:
        data = f.read()
    n = compile(data, path, "exec", ast.PyCF_ONLY_AST)
    assert bool(n.body) or not bool(data), "__init__.py must be empty"
