from lxml import etree
import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_series,
)
from metadatavalidator.exceptions import InvalidValueError


def test_check_meta_series(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="series">Products &amp; Solutions</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "series"}, "Products & Solutions")
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_series=True,
                                valid_meta_series=["Products & Solutions",
                                                   "Best Practices",
                                                   "Technical References"]))
    assert check_meta_series(tree, config) is None


def test_check_missing_optional_meta_series(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    config = dict(metadata=dict(require_meta_series=False))
    assert check_meta_series(tree, config) is None


def test_check_wrong_meta_series(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="series">Foo</meta>
#     </info>
#     <para/>
# </article>"""
    meta = D("meta", {"name": "series"}, "Foo")
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_series=True,
                                valid_meta_series=["Best Practices",
                                                   "Technical References"]))
    with pytest.raises(InvalidValueError, match="Meta series is invalid"):
        check_meta_series(tree, config)


def test_check_require_meta_series(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
#     <para/>
# </article>"""

    config = dict(
        metadata=dict(
            require_meta_series=True,
            valid_meta_series=["Best Practices", "Technical References"],
        )
    )
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find required meta.*"):
        check_meta_series(tree, config)
