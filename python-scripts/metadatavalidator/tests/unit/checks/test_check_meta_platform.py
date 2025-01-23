from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_platform,
)
from metadatavalidator.exceptions import InvalidValueError


def test_check_meta_platform(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="platform">Foo</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "platform"}, "Foo")
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_platform=True))
    assert check_meta_platform(tree, config) is None


def test_check_missing_meta_platform(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""
#     tree = etree.ElementTree(etree.fromstring(xmlcontent, parser=xmlparser))

    config = dict(metadata=dict(require_meta_platform=True))
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find required meta.*"):
        check_meta_platform(tree, config)


def test_check_empty_meta_platform(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="platform"/>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "platform"})
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_platform=True))
    with pytest.raises(InvalidValueError, match=r".*Empty meta.*"):
        check_meta_platform(tree, config)
