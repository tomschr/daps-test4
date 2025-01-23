from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_description,
)
from metadatavalidator.exceptions import InvalidValueError



def test_check_meta_description(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="description">The SEO description</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "description"}, "The SEO description")
    appendnode(tree, meta)
    assert check_meta_description(tree, {}) is None


def test_check_meta_description_wrong_length(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="description">The SEO description that is too long</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "description"}, "The SEO description that is too long")
    appendnode(tree, meta)

    with pytest.raises(InvalidValueError, match=".*too long.*"):
        check_meta_description(tree, dict(metadata=dict(meta_description_length=10)))


def test_check_required_meta_description(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    with pytest.raises(InvalidValueError, match=".*required.*"):
        check_meta_description(tree, dict(metadata=dict(meta_description_required=True)))


def test_check_optional_meta_description(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    assert check_meta_description(tree,
                                  dict(metadata=dict(meta_description_required=False))) is None
