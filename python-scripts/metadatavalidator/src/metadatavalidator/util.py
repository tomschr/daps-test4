import datetime
import typing as t
from lxml import etree

from .common import (
    DATE_REGEX,
    NAMESPACES,
    NAMESPACES2PREFIX,
    )
from .exceptions import InvalidValueError



def green(text):    # pragma: no cover
    return f"\033[32m{text}\033[0m"

def red(text):    # pragma: no cover
    return f"\033[31m{text}\033[0m"


def getinfo(tree: etree._ElementTree) -> etree._Element|None:
    """Get the <info> element from a DocBook5 XML tree

    :param tree: the XML tree to get the <info> element from
    :return: the <info> element
    """
    # Check if we get all children of <info> element from "normal" root
    # elements orfrom an assembly structure.
    # Regular structures have <info>, but for an assembly we only have
    # <merge> (which can be seen as a "virtual" <info> element).
    a = tree.find("./d:info", namespaces=NAMESPACES)
    b = tree.find("./d:structure/d:merge", namespaces=NAMESPACES)

    if a is not None:
        return a
    if b is not None:
        return b


def info_or_fail(tree: etree._ElementTree, raise_on_missing=True) -> etree._Element:
    """Get the <info> element from a DocBook5 XML tree or raise an error

    :param tree: the XML tree to get the <info> element from
    :param raise_on_missing: whether to raise an error if the <info> element is missing
    :return: the <info> element
    """
    info = getinfo(tree)
    if info is None and raise_on_missing:
        raise InvalidValueError("Couldn't find <info> element.")
    return info


def getfullxpath(element: etree._Element,
                 ns2prefix:dict[str, str]=NAMESPACES2PREFIX) -> str:
    """Return the full XPath including predicates to this element

        :param: the element to get an XPath for
        :return: the full absolute XPath with optional predicates
    """
    tree = element.getroottree()
    root = tree.getroot()

    # Get the basic XPath from the root to the element
    # There are two different cases:
    # 1. Your element belongs to no namespace:
    #    get a regular XPath, no need to add anything
    # 2. Your element belongs to a namespace:
    #    proceed further
    path = tree.getpath(element)
    if "*" not in path:
        return path
    path = path.split("/")

    # Get the "full" XPath, but add the missing root element
    # Looks like ''{http://docbook.org/ns/docbook}info/{http://docbook.org/ns/docbook}revhistory'
    fullpath = "/{}/{}".format(
        etree.QName(root),
        tree.getelementpath(element)
    )
    # Remove some leftovers in case you have just "." from .getelementpath()
    fullpath = fullpath.replace("/.", "")

    # Replace a namespace with a prefix
    for ns, prefix in ns2prefix.items():
        fullpath = fullpath.replace(f'{{{ns}}}', f'{prefix}:')
    fullpath = fullpath.split("/")

    # Check if the two paths have the same length
    # if len(path) != len(fullpath):
    #    raise RuntimeError("two paths differ")

    # Combine element part and predicate
    return "/".join([f"{p2}{p1.replace('*', '')}"
                     for p1, p2 in zip(path, fullpath) ]
    )


def parse_date(date_text: str) -> datetime.date:
    """Attempt to parse a date string into a date object
    Valid formats are YYYY-MM-DD, YYYY-M-D, YYYY-MM, YYYY-M,
    YYYY-MM-D, and YYYY-M-D
    """
    # Attempt to parse the date text into a date object
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            # This will handle all formats
            parsed_date = datetime.datetime.strptime(date_text, fmt)
            return parsed_date.date()
        except ValueError:
            continue

    # If none of the formats matched, raise an error
    raise ValueError(f"Invalid date format: {date_text}")


def validatedate(element: etree._Element):
    """Validate the date text from an element"""
    # First check the formal correctness of the date with regex

    date = validatedatevalue(element.text.strip())
    if date is None:
        path = getfullxpath(element)
        raise InvalidValueError(f"Invalid date format in {element.tag} (XPath={path}).")
    return date


def validatedatevalue(date: str) -> t.Optional[datetime.date]:
    """Validate the date text from an element"""
    # First check the formal correctness of the date with regex
    if not date or not DATE_REGEX.search(date):
        raise InvalidValueError(f"Date is empty or has invalid format: {date}.")

    # Check if the date is valid
    try:
        return parse_date(date.strip())

    except ValueError as e:
        return None
