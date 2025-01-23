import pytest

from _utils import dbtag, D

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks import (
    check_info,
)
from metadatavalidator.util import getinfo, info_or_fail
from metadatavalidator.exceptions import InvalidValueError


def test_getinfo_with_regular_tree(tree):
    info = getinfo(tree)
    assert info is not None
    assert info.tag == dbtag("info")


def test_getinfo_with_assembly_tree(asmtree):
    merge = getinfo(asmtree)
    assert merge is not None
    assert merge.tag == dbtag("merge")


def test_info_or_fail_with_regular_tree(tree):
    info = info_or_fail(tree)
    assert info is not None
    assert info.tag == dbtag("info")


def test_info_or_fail_with_assembly_tree(asmtree):
    merge = info_or_fail(asmtree)
    assert merge is not None
    assert merge.tag == dbtag("merge")


def test_info_or_fail_with_raise_on_missing():
    tree = D("article").getroottree()
    info = info_or_fail(tree, raise_on_missing=False)
    assert info is None


def test_info_or_fail_with_raise_on_missing_and_missing_info():
    tree = D("article").getroottree()
    with pytest.raises(InvalidValueError, match="Couldn't find <info> element."):
        info_or_fail(tree)


def test_check_info(tree):
    assert check_info(tree, {}) is None


def test_check_info_missing():
    tree = D("article").getroottree()
    with pytest.raises(InvalidValueError,
                          match=".*Couldn't find <info> element."):
          check_info(tree, {})
