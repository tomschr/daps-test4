from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_title,
)
from metadatavalidator.exceptions import InvalidValueError


def test_check_meta_title(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="title">The SEO title</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "title"}, "The SEO title")
    appendnode(tree, meta)

    assert check_meta_title(tree, {}) is None


def test_check_meta_title_wrong_length(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="title">The SEO title that is too long</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "title"}, "The SEO title that is too long")
    appendnode(tree, meta)

    with pytest.raises(InvalidValueError, match=".*too long.*"):
        check_meta_title(tree, dict(metadata=dict(meta_title_length=10)))


def test_check_required_meta_title(tree):
    with pytest.raises(InvalidValueError, match=".*required.*"):
        check_meta_title(tree, dict(metadata=dict(meta_title_required=True)))


def test_check_optional_meta_title(tree):
    config = dict(metadata=dict(meta_title_required=False))
    assert check_meta_title(tree, config) is None

def test_check_meta_title_empty(tree):
    meta = D("meta", {"name": "title"})
    appendnode(tree, meta)

    with pytest.raises(InvalidValueError,
                       match=r".*Empty meta\[@name='title'\] element.*"):
        check_meta_title(tree, dict(metadata=dict(meta_title_length=10,
                                                  meta_title_required=True)))