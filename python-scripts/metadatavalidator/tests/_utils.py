from lxml import etree
from lxml.builder import ElementMaker
from metadatavalidator.common import NAMESPACES, DOCBOOK_NS, XML_NS


D = ElementMaker(namespace=NAMESPACES["d"], nsmap={None: DOCBOOK_NS})

def dbtag(tag):
    return f"{{{DOCBOOK_NS}}}{tag}"

xmlid = f"{{{XML_NS}}}id"


def appendnode(tree: etree._ElementTree, node: etree._Element):
    """Append the given <meta> element to the <info> element in the tree."""
    root = tree.getroot()
    info = root.find("./d:info", namespaces=NAMESPACES)
    info.append(node)
    return tree
