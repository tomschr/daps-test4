import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks import (
    check_info_revhistory,
    check_info_revhistory_revision,
    check_info_revhistory_revision_date,
    check_info_revhistory_revision_order,
)

from metadatavalidator.exceptions import InvalidValueError, MissingAttributeWarning


def test_check_info_revhistory_missing(tree):
    with pytest.raises(InvalidValueError,
                       match="Couldn't find a revhistory element"):
        check_info_revhistory(tree, {"metadata": {"require_revhistory": True}})


def test_check_info_revhistory(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh"></revhistory>
#     </info>
#     <para/>
# </article>"""
#     tree = ET.ElementTree(
#         ET.fromstring(xmlcontent, parser=xmlparser)
#     )
    revhistory = D("revhistory", {xmlid: "rh"})
    appendnode(tree, revhistory)

    assert check_info_revhistory(tree, {}) is None


def test_check_info_revhistory_without_info(tree):
    info = tree.find("./d:info", namespaces=NAMESPACES)
    info.getparent().remove(info)
    with pytest.raises(InvalidValueError,
                       match="Couldn't find <info> element."):
        check_info_revhistory(tree, {})


def test_check_info_revhistory_xmlid(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh1"></revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", {xmlid: "rh1"})
    appendnode(tree, revhistory)

    assert check_info_revhistory(tree, {}) is None


def test_info_revhistory_missing_xmlid(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory/>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory")
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match="Couldn't find xml:id attribute"):
        check_info_revhistory(tree, {})


def test_check_info_revhistory_xmlid_with_wrong_value(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="wrong_id"></revhistory>
#     </info>
#     <para/>
# </article>"""
    appendnode(tree, D("revhistory", {xmlid: "wrong_id"}))

    with pytest.raises(InvalidValueError,
                       match="should start with 'rh'"):
        check_info_revhistory(tree, {})


def test_check_info_revhistory_revision(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory>
#           <revision xml:id="rh">
#             <date>2021-01-01</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory",
                   D("revision", {xmlid: "rh"},
                     D("date", "2021")
                     )
                   )
    appendnode(tree, revhistory)

    assert check_info_revhistory_revision(tree, {}) is None


def test_check_info_revhistory_revision_missing_xmlid(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory>
#           <revision>
#             <date>2021-01-01</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory",
                    D("revision",
                      D("date", "2021-01-01")
                      )
                    )
    appendnode(tree, revhistory)

    with pytest.raises(MissingAttributeWarning,
                       match="Missing recommended attribute in"):
        check_info_revhistory_revision(
            tree,
            {"metadata": {"require_xmlid_on_revision": True}})


def test_check_info_revhistory_revision_missing(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory/>
#     </info>
#     <para/>
# </article>"""
    appendnode(tree, D("revhistory"))

    with pytest.raises(InvalidValueError,
                       match=".*Couldn't find any revision element.*"):
        check_info_revhistory_revision(
            tree,
            {"metadata": {"require_xmlid_on_revision": True}}
        )


def test_check_info_revhistory_revision_date(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory>
#           <revision>
#             <date>2021-01-01</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory",
                   D("revision",
                     D("date", "2021-01-01")
                    )
                   )
    appendnode(tree, revhistory)

    assert check_info_revhistory_revision_date(tree, {}) is None


def test_check_info_revhistory_revision_date_missing(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory>
#           <revision/>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", D("revision"))
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match="Couldn't find a date element"):
        check_info_revhistory_revision_date(tree, {})


def test_check_info_revhistory_revision_date_invalid_format(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh">
#           <revision>
#             <date>January 2024</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", D("revision", D("date", "January 2024")))
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match=".*ate is empty or has invalid format.*"):
        check_info_revhistory_revision_date(tree, {})


def test_check_info_revhistory_revision_date_invalid_value(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh">
#           <revision>
#             <date>2024-13</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", {xmlid: "rh"},
                   D("revision", D("date", "2024-13")))
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match="Invalid value in metadata"
                       ):
        check_info_revhistory_revision_date(tree, {})


def test_check_info_revhistory_revision_order(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh">
#           <revision>
#             <date>2024-12</date>
#           </revision>
#           <revision>
#             <date>2023-12-12</date>
#           </revision>
#           <revision>
#             <date>2022-04</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", {xmlid: "rh"},
                     D("revision", D("date", "2024-12")),
                     D("revision", D("date", "2023-12-12")),
                     D("revision", D("date", "2022-04")))
    appendnode(tree, revhistory)

    assert check_info_revhistory_revision_order(tree, {}) is None


def test_check_info_revhistory_revision_order_without_revision(tree):
    revhistory = D("revhistory", {xmlid: "rh"})
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match=".*Couldn't find any revision element.*"):
        check_info_revhistory_revision_order(tree, {})


def test_check_info_revhistory_revision_order_one_invalid_date(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh">
#           <revision>
#             <date>2024-53</date><!-- Wrong date -->
#           </revision>
#           <revision>
#             <date>2023-12-12</date>
#           </revision>
#           <revision>
#             <date>2022-04</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", {xmlid: "rh"},
                    D("revision", D("date", "2024-53")),
                    D("revision", D("date", "2023-12-12")),
                    D("revision", D("date", "2022-04"))
                    )
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match=".*Couldn't convert all dates.*see position dates=1.*"
                       ):
        check_info_revhistory_revision_order(tree, {})


def test_check_info_revhistory_revision_wrong_order(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <revhistory xml:id="rh">
#           <revision>
#             <date>2024-12</date>
#           </revision>
#           <revision>
#             <date>2023-12-12</date>
#           </revision>
#           <revision>
#             <date>2026-04</date>
#           </revision>
#         </revhistory>
#     </info>
#     <para/>
# </article>"""
    revhistory = D("revhistory", {xmlid: "rh"},
                    D("revision", D("date", "2024-12")),
                    D("revision", D("date", "2023-12-12")),
                    D("revision", D("date", "2026-04"))
                    )
    appendnode(tree, revhistory)

    with pytest.raises(InvalidValueError,
                       match=".*Dates in revhistory/revision are not in descending order.*"
                       ):
        check_info_revhistory_revision_order(tree, {})
