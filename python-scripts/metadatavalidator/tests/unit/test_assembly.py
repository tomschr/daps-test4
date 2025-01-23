from lxml import etree
import pytest

from _utils import dbtag

from metadatavalidator.common import NAMESPACES
from metadatavalidator.util import getinfo


def test_assembly_for_info(asmtree):
    merge = getinfo(asmtree)
    assert merge is not None
    assert merge.tag == dbtag("merge")


