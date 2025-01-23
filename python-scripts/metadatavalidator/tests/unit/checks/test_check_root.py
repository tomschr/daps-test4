
from lxml import etree
import pytest

from metadatavalidator.checks import check_root_tag, check_namespace
from metadatavalidator.exceptions import InvalidValueError


def test_check_root_tag(tree):
    assert check_root_tag(tree, {"validator": {"check_root_elements": ["article"]}}) is None


def test_check_check_namespace(tree):
    assert check_namespace(tree, {}) is None


def test_check_root_tag_invalid():
    tree = etree.ElementTree(
        etree.fromstring("""<not_docbook5/>""",
                         parser=etree.XMLParser(encoding="UTF-8"))
    )

    with pytest.raises(InvalidValueError,
                       match="Root tag 'not_docbook5'.*"):
        check_root_tag(tree, {"validator": {"check_root_elements": ["article"]}})


def test_check_check_namespace_invalid():
    tree = etree.ElementTree(
        etree.fromstring("""<not_docbook5/>""",
                         parser=etree.XMLParser(encoding="UTF-8"))
    )

    with pytest.raises(InvalidValueError,
                       match=".*doesn't belong to DocBook 5"
                       ):
        check_namespace(tree, {})