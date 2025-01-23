from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_techpartner,
)
from metadatavalidator.exceptions import InvalidValueError


def test_check_meta_techpartner(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="techpartner">
#             <phrase>Acme Inc.</phrase>
#             <phrase>Foo Corp.</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "techpartner"},
             D("phrase", {}, "Acme Inc."),
             D("phrase", {}, "Foo Corp."),
             )
    appendnode(tree, meta)

    assert check_meta_techpartner(tree, {}) is None


def test_check_missing_meta_techpartner(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    config = dict(metadata=dict(require_meta_techpartner=True))
    with pytest.raises(InvalidValueError, match=".*required.*"):
        check_meta_techpartner(tree, config)


def test_check_missing_children_in_meta_techpartner(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="techpartner"/>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "techpartner"})
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_techpartner=True))
    with pytest.raises(InvalidValueError, match=".*Couldn't find any tech partners.*"):
        check_meta_techpartner(tree, config)


def test_check_meta_techpartner_with_nonunique_children(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="techpartner">
#             <phrase>Acme Inc.</phrase>
#             <phrase>Acme Inc.</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "techpartner"},
             D("phrase", "Acme Inc."),
             D("phrase", "Acme Inc."),
             )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_techpartner=True))
    with pytest.raises(InvalidValueError, match=".*Duplicate tech partners.*"):
        check_meta_techpartner(tree, config)
