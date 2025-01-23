from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_category,
)
from metadatavalidator.exceptions import InvalidValueError


def test_meta_category(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="category">
#             <phrase>Systems Management</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "category"},
             D("phrase", "Systems Management"))
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_category=True,
                                valid_meta_categories=["Systems Management"]))
    assert check_meta_category(tree, config) is None


def test_missing_optional_meta_category(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    config = dict(metadata=dict(require_meta_category=True))
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find required meta.*"):
        check_meta_category(tree, config)


def test_missing_child_meta_category(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="category"/>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "category"})
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_category=True))
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find any child elements in meta.*"):
        check_meta_category(tree, config)


def test_duplicate_child_meta_category(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="category">
#             <phrase>Systems Management</phrase>
#             <phrase>Systems Management</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "category"},
                D("phrase", "Systems Management"),
                D("phrase", "Systems Management"),
                )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_category=True))
    with pytest.raises(InvalidValueError,
                       match=r".*Duplicate categories found in meta.*"):
        check_meta_category(tree, config)


def test_unknown_category_meta_category(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="category">
#             <phrase>Systems Management</phrase>
#             <phrase>Foo</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "category"},
             D("phrase", "Systems Management"),
             D("phrase", "Foo"),
             )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_category=True,
                                valid_meta_categories=["Systems Management"]))
    with pytest.raises(InvalidValueError,
                       match=r".*Unknown category.*"):
        check_meta_category(tree, config)

