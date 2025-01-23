"""
Checks <meta name="..."> elements in a <info> element of a DocBook5 XML file.

Source: https://confluence.suse.com/x/aQDWNg
"""

import typing as t

from lxml import etree

from ..common import NAMESPACES
from ..exceptions import InvalidValueError
from ..logging import log
from ..util import info_or_fail


def check_meta_title(tree: etree._ElementTree,
                     config: dict[t.Any, t.Any]):
    """Checks for a <meta name="title"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='title']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("meta_title_required", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='title'] element in {root.tag}"
                f" (line {info.sourceline})."
            )
        return

    # the meta[@name='title'] element exists, but must not be empty
    if meta.text is None:
        raise InvalidValueError(
            f"Empty meta[@name='title'] element (line {meta.sourceline})."
        )

    length = config.get("metadata", {}).get("meta_title_length", 55)
    if meta.text is not None and len(meta.text) > length:
        raise InvalidValueError(
            f"Meta title is too long. Max length is {length} characters"
            f" (line {meta.sourceline})."
            )


def check_meta_description(tree: etree._ElementTree,
                           config: dict[t.Any, t.Any]):
    """Checks for a <meta name="description"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='description']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("meta_description_required", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='description'] element in "
                f"{root.tag} (line {info.sourceline})."
            )
        return

    length = config.get("metadata", {}).get("meta_description_length", 150)
    if len(meta.text) > length:
        raise InvalidValueError(
            f"Meta description is too long. Max length is {length} characters."
            f" (line {meta.sourceline})."
            )


def check_meta_series(tree: etree._ElementTree,
                      config: dict[t.Any, t.Any]):
    """Checks for a <meta name="series"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='series']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_series", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='series'] element in {root.tag}"
                f" (line {info.sourceline})."
            )
        return

    valid_series = [x.strip() for x in
                    config.get("metadata", {}).get("valid_meta_series", [])
                    if x]
    if meta.text.strip() not in valid_series:
        raise InvalidValueError(
            f"Meta series is invalid, got {meta.text.strip()!r}. "
            f"Valid series are {valid_series}"
            f" (line {meta.sourceline})."
        )


def check_meta_techpartner(tree: etree._ElementTree,
                           config: dict[t.Any, t.Any]):
    """Checks for a <meta name="techpartner"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='techpartner']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_techpartner", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='techpartner'] element "
                f"in {root.tag}"
                f" (line {info.sourceline})."
            )
        return

    # Do we have children?
    partners = [tag.text.strip() for tag in meta.iterchildren()]
    if not partners:
        raise InvalidValueError(
            f"Couldn't find any tech partners in meta[@name='techpartner'] element "
            f"(line {meta.sourceline})"
        )

    # Are they unique?
    if len(partners) != len(set(partners)):
        raise InvalidValueError(
            f"Duplicate tech partners found in meta[@name='techpartner'] element "
            f"(line {meta.sourceline})."
        )


def check_meta_platform(tree: etree._ElementTree,
                        config: dict[t.Any, t.Any]):
    """Checks for a <meta name="platform"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='platform']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_platform", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='platform'] element "
                f"in {root.tag}"
                f" (line {info.sourceline})."
            )
        return

    if meta.text is None or not meta.text.strip():
        raise InvalidValueError("Empty meta[@name='platform'] element")


def check_meta_architecture(tree: etree._ElementTree,
                            config: dict[t.Any, t.Any]):
    """Checks for a <meta name="architecture"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='architecture']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_architecture",
                                              False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='architecture'] element "
                f"in {root.tag}"
                f" (line {info.sourceline})."
            )
        return

    valid_archs = [
        x.strip() for x in config.get("metadata", {}
                                      ).get("valid_meta_architectures", [])
        if x
    ]

    # Do we have children?
    archs = [tag.text.strip() for tag in meta.iterchildren()]
    if not archs:
        raise InvalidValueError(
            f"Couldn't find any child elements in meta[@name='architecture']"
            f" (line {meta.sourceline})."
        )

    # Are they unique?
    if len(archs) != len(set(archs)):
        raise InvalidValueError(
            f"Duplicate architectures found in meta[@name='architecture']"
            f" (line {meta.sourceline})."
        )

    # Do we have items that don't conform to our predefined list?
    wrong_items = set(archs) - set(valid_archs)
    if wrong_items:
        raise InvalidValueError(
            f"Unknown architecture(s) {wrong_items}. "
            f"Allowed are {valid_archs}"
            f" (line {meta.sourceline})."
        )


def check_meta_category(tree: etree._ElementTree,
                        config: dict[t.Any, t.Any]):
    """Checks for a <meta name="category"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='category']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_category", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='category'] element "
                f"in {root.tag}."
            )
        return

    valid_cats = [
        x.strip() for x in config.get("metadata", {}
                                      ).get("valid_meta_categories", [])
        if x
    ]

    # Do we have children?
    cats = [tag.text.strip() for tag in meta.iterchildren()]
    if not cats:
        raise InvalidValueError(
            f"Couldn't find any child elements in meta[@name='category']"
            f" (line {meta.sourceline})."
        )

    # Are they unique?
    if len(cats) != len(set(cats)):
        raise InvalidValueError(
            f"Duplicate categories found in meta[@name='category']"
            f" (line {meta.sourceline})."
        )

    # Do we have items that don't conform to our predefined list?
    wrong_items = set(cats) - set(valid_cats)
    if wrong_items:
        raise InvalidValueError(
            f"Unknown category(ies) {wrong_items}. "
            f"Allowed are {valid_cats}."
            f" (line {meta.sourceline})."
        )


def check_meta_task(tree: etree._ElementTree,
                    config: dict[t.Any, t.Any]):
    """Checks for a <meta name="task"> element"""
    root = tree.getroot()
    info = info_or_fail(tree)
    meta = info.find("./d:meta[@name='task']", namespaces=NAMESPACES)
    required = config.get("metadata", {}).get("require_meta_task", False)
    if meta is None:
        if required:
            raise InvalidValueError(
                f"Couldn't find required meta[@name='task'] element "
                f"in {root.tag}."
            )
        return

    valid_tasks = [
        x.strip() for x in config.get("metadata", {}
                                      ).get("valid_meta_tasks", [])
        if x
    ]

    # Do we have children?
    tasks = [tag.text.strip() for tag in meta.iterchildren()
             if tag.text is not None]
    if not tasks:
        raise InvalidValueError(
            f"Couldn't find any child elements in meta[@name='task']"
            f" (line {meta.sourceline})."
        )

    # Are they unique?
    if len(tasks) != len(set(tasks)):
        raise InvalidValueError(
            f"Duplicate tasks found in meta[@name='task']"
            f" (line {meta.sourceline})."
        )

    # Do we have items that don't conform to our predefined list?
    wrong_items = set(tasks) - set(valid_tasks)
    if wrong_items:
        raise InvalidValueError(
            f"Unknown task(s) {wrong_items}. "
            f"Allowed are {valid_tasks}"
            f" (line {meta.sourceline})."
        )