from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_architecture,
    check_meta_category,
    check_meta_task,
)
from metadatavalidator.exceptions import InvalidValueError


def test_check_meta_architecture(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="architecture">
#           <phrase>x86_64</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "architecture"}, D("phrase", "x86_64"))
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_architecture=True,
                                valid_meta_architectures=["x86_64", "POWER"]))
    assert check_meta_architecture(tree, config) is None


def test_check_missing_optional_meta_architecture(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    config = dict(metadata=dict(require_meta_architecture=True))
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find required meta.*"):
        check_meta_architecture(tree, config)


def test_check_missing_child_meta_architecture(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="architecture"/>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "architecture"})
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_architecture=True))
    with pytest.raises(
        InvalidValueError,
        match=r".*Couldn't find any child elements in meta.*"
    ):
        check_meta_architecture(tree, config)


def test_check_duplicate_child_meta_architecture(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="architecture">
#           <phrase>x86_64</phrase>
#           <phrase>x86_64</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "architecture"},
                D("phrase", "x86_64"),
                D("phrase", "x86_64"),
                )
    appendnode(tree, meta)

    config = dict(metadata=dict(
        require_meta_architecture=True,
        valid_meta_architectures=["x86_64", "POWER"]))
    with pytest.raises(
        InvalidValueError, match=r".*Duplicate architectures found in meta.*"
    ):
        check_meta_architecture(tree, config)


def test_check_unknown_child_meta_architecture(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="architecture">
#           <phrase>x86_64</phrase>
#           <phrase>foo</phrase>
#         </meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "architecture"},
            D("phrase", "x86_64"),
            D("phrase", "foo"),
            )
    appendnode(tree, meta)

    config = dict(
        metadata=dict(
            require_meta_architecture=True,
            valid_meta_architectures=["x86_64", "POWER"],
        )
    )
    with pytest.raises(InvalidValueError,
                       match=r".*Unknown architecture.*"):
        check_meta_architecture(tree, config)
