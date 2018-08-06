# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# test BI dictionaries
# ----------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest
# NOC modules
from noc.core.clickhouse.dictionary import Dictionary


@pytest.fixture(params=list(Dictionary.iter_cls()))
def dictionary(request):
    return request.param


@pytest.mark.dependency(name="test_dictionary_cls")
def test_cls(dictionary):
    assert Dictionary.get_dictionary_class(dictionary)


@pytest.mark.dependency(depends=["test_dictionary_cls"])
def test_config(dictionary):
    d = Dictionary.get_dictionary_class(dictionary)
    # @todo: Check result
    assert d.get_config()
