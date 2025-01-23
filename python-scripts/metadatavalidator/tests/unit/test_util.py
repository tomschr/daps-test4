import pytest
from lxml import etree

from metadatavalidator.util import getfullxpath, parse_date

xmlcontent = """<article>
    <title/>
    <para/>
    <section>
       <title/>
       <para/>
       <para/>
    </section>
    </article>
"""


def test_getfullpath():
    root = etree.fromstring(xmlcontent)
    tree = root.getroottree()
    section = tree.find("./section")
    assert getfullxpath(section) == "/article/section"

    para = tree.find("./section/para[1]")
    assert getfullxpath(para) == "/article/section/para[1]"

    para = tree.find("./section/para[2]")
    assert getfullxpath(para) == "/article/section/para[2]"


@pytest.mark.parametrize("date_text, expected", [
    ("2021-01-01", "2021-01-01"),
    ("2021-1-1", "2021-01-01"),
    ("2021-01", "2021-01-01"),
    ("2021-1", "2021-01-01"),
    ("2021-01-1", "2021-01-01"),
    ("2021-1-01", "2021-01-01"),
    ("2024-12-12", "2024-12-12"),
])
def test_parse_valid_dates(date_text, expected):
    assert str(parse_date(date_text)) == expected


@pytest.mark.parametrize("date_text", [
    ("foo"),
    ("2021"),
    ("2024-14"),
    (""),
])
def test_parse_invalid_dates(date_text):
    with pytest.raises(ValueError):
        parse_date(date_text)
