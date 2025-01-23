import typing as t

from lxml import etree

from ..common import DOCBOOK_NS
from ..exceptions import InvalidValueError
from ..logging import log


def check_root_tag(tree: etree._ElementTree, config: dict[t.Any, t.Any]):
    """Checks if root element is in the list of allowed elements
    """
    allowed_root_elements = config.get("validator", {}).get("check_root_elements")
    tag = etree.QName(tree.getroot().tag)
    if tag.localname not in allowed_root_elements:
        raise InvalidValueError(f"Root tag {tag.localname!r} is not allowed. Expected {', '.join(allowed_root_elements)}.")


def check_namespace(tree: etree._ElementTree, config: dict[t.Any, t.Any]):
    """Checks the namespace"""
    tag = etree.QName(tree.getroot().tag)
    if tag.namespace != DOCBOOK_NS:
        raise InvalidValueError(
            f"Root element {tag.localname!r} doesn't belong to DocBook 5."
            )

