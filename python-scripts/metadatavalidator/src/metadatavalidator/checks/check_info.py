import asyncio
import datetime
import itertools
import typing as t

from lxml import etree

from ..common import (
    NAMESPACES,
    XML_NS,
)
from ..exceptions import InvalidValueError, MissingAttributeWarning
from ..logging import log
from ..util import (
    info_or_fail,
    getfullxpath,
    validatedate,
    validatedatevalue
)


def check_info(tree: etree._ElementTree, config: dict[t.Any, t.Any]):
    """Checks for an info element"""
    info_or_fail(tree)


def check_info_revhistory(tree: etree._ElementTree, config: dict[t.Any, t.Any]):
    """Checks for an info/revhistory element"""
    info = info_or_fail(tree)

    required = config.get("metadata", {}).get("require_revhistory", False)

    revhistory = info.find("./d:revhistory", namespaces=NAMESPACES)
    if revhistory is None:
        if required:
            raise InvalidValueError(f"Couldn't find a revhistory element in {info.tag}.")
        return None

    xmlid = revhistory.attrib.get(f"{{{XML_NS}}}id")
    if xmlid is None:
        raise InvalidValueError(f"Couldn't find xml:id attribute in revhistory.")

    if not xmlid.startswith("rh"):
        raise InvalidValueError(f"xml:id attribute in revhistory should start with 'rh'.")


def check_info_revhistory_revision(tree: etree._ElementTree,
                                   config: dict[t.Any, t.Any]):
    """Checks for an info/revhistory/revision element"""
    info = info_or_fail(tree)
    revhistory = info.find("./d:revhistory", namespaces=NAMESPACES)

    if revhistory is None:
        # If <info> couldn't be found, we can't check <revhistory>
        return

    revision = revhistory.find("./d:revision", namespaces=NAMESPACES)
    if revision is None:
        raise InvalidValueError(f"Couldn't find a revision element in {revhistory.tag}.")
    xmlid = revision.attrib.get(f"{{{XML_NS}}}id")

    if config.get("metadata", {}).get("require_xmlid_on_revision", True) and xmlid is None:
        xpath = getfullxpath(revision)
        xpath += "/@xml:id"
        raise MissingAttributeWarning(xpath)


def check_info_revhistory_revision_date(tree: etree._ElementTree,
                                        config: dict[t.Any, t.Any]):
    """Checks for an info/revhistory/revision/date element"""
    info = info_or_fail(tree)

    revhistory = info.find("./d:revhistory", namespaces=NAMESPACES)
    if revhistory is None:
        return None

    date = revhistory.find("./d:revision/d:date", namespaces=NAMESPACES)
    if date is None:
        raise InvalidValueError(f"Couldn't find a date element in info/revhistory/revision.")

    validatedate(date)


def check_info_revhistory_revision_order(tree: etree._ElementTree,
                                        config: dict[t.Any, t.Any]):
    """Checks for the right order of info/revhistory/revision elements"""
    info = info_or_fail(tree)
    revhistory = info.find("./d:revhistory", namespaces=NAMESPACES)
    if revhistory is None:
        return
    revisions = revhistory.xpath("./d:revision",
                                  namespaces=NAMESPACES)
    xpath = getfullxpath(revhistory)
    if not revisions:
        return None

    date_elements = [rev.find("./d:date", namespaces=NAMESPACES)
                     for rev in revisions]
    dates = [
        validatedatevalue(d.text)
        for d in date_elements if d is not None
    ]
    converteddates: list[datetime.date] = [d for d in dates if d is not None]

    # First check: check if we have the same number of dates and revisions
    if len(converteddates) != len(revisions):
        raise InvalidValueError(f"Couldn't convert all dates "
                                f"(see position dates={dates.index(None)+1}). "
                                f"Check {xpath}")

    # Second check: we have the same number of dates and revisions, now
    # check if the dates are in descending order
    for first, second in itertools.pairwise(converteddates):
        if first <= second:
            raise InvalidValueError(
                "Dates in revhistory/revision are not in descending order: "
                f"{first} <= {second}."
                )

