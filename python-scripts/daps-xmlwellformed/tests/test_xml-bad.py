from pathlib import Path
import logging
import re
import sys

import pytest

# "dxwf" is the abbreviated name for daps-xmlwellformed
# We can't import a name with a "-" so we use a link here:
import dxwf


THISDIR = Path(__file__).parent
DATADIR = THISDIR / "data"
BADDIR = DATADIR / "bad"


def test_syntax_error():
    # Given
    xmlfile = str(BADDIR / "test-syntax-err-tag-name-mismatch.xml")

    # When
    result = dxwf.check_wellformedness(xmlfile)

    # Then
    assert result != 0


def test_syntax_error_stderr(caplog):
    # Given
    xmlfile = "test-syntax-err-tag-name-mismatch.xml"
    messages = (
        ("Opening and ending tag mismatch: title line 7 and article",),
        # These error messages are different between different lxml versions:
        ("EndTag: '</' not found",  # lxml >=4.5.2
         "Premature end of data in tag article line 5", # lxml >=4.4.3
         ),
    )
    file = str(BADDIR / xmlfile)

    # When
    with caplog.at_level(logging.ERROR):
        dxwf.check_wellformedness(file)

    # Then
    assert len(caplog.records) == len(messages)
    for record, msg in zip(caplog.records, messages):
        assert record.msg in msg


def test_unknown_entity_stderr(caplog):
    # Given
    xmlfile = "test-syntax-err-undeclared-entity.xml"
    messages = (
        "Entity 'unknown' not defined",
    )
    file = str(BADDIR / xmlfile)

    # When
    with caplog.at_level(logging.ERROR):
        result = dxwf.check_wellformedness(file)

    # Then
    assert result == dxwf.ExitCode.syntax
    assert len(caplog.records) == len(messages)
    for record, msg in zip(caplog.records, messages):
        assert record.msg == msg


@pytest.mark.parametrize("xmlfile", [
    "test-syntax-err-hyphen-in-comment.xml",
    "test-syntax-err-name-required.xml",
    "test-syntax-err-ltslash-required.xml",
])
def test_syntax_errors(xmlfile):
    # Given
    xmlfile = str(BADDIR / xmlfile)

    # When
    result = dxwf.check_wellformedness(xmlfile)

    # Then
    assert result == dxwf.ExitCode.syntax


def test_file_not_found():
    # Given
    xmlfile = str(BADDIR / "unknown.xml")

    # When
    result = dxwf.check_wellformedness(xmlfile)

    # Then
    assert result == dxwf.ExitCode.file_not_found


@pytest.mark.parametrize("xmlfile,messages", [
    ("test-xinclude-file-not-found.xml",
     (r"could not load (.*)tests/data/bad/file-not-found.xml, and no fallback was found",
      )
     ),
    ("test-xinclude-undeclared-entity.xml",
     ("Entity 'unknown' not defined",
      r"could not load (.*)tests/data/bad/test-syntax-err-undeclared-entity.xml, and no fallback was found",
      )
     ),
])
def test_xinclude_errors(xmlfile, messages, caplog):
    # Given
    xmlfile = str(BADDIR / xmlfile)

    # When
    with caplog.at_level(logging.ERROR):
        result = dxwf.check_wellformedness(xmlfile, xinclude=True)

    # Then
    assert len(caplog.records) == len(messages)
    for record, pattern in zip(caplog.records, messages):
        assert re.search(pattern, record.msg)



def test_xinclude_file_not_found_missing_entity_file(caplog):
    # Given
    xmlfile = str(BADDIR /
                  "test-xinclude-file-not-found-missing-entity-file.xml")
    expected_return_codes = (logging.getLevelName(logging.FATAL),
                             logging.getLevelName(logging.ERROR)
                             )
    
    # When
    with caplog.at_level(logging.ERROR):
        result = dxwf.check_wellformedness(xmlfile, xinclude=True)
    
    # Then
    assert caplog.records
    assert len(caplog.records) == len(expected_return_codes)

    records = caplog.records
    return_codes = tuple([logging.getLevelName(getattr(logging, record.levelname))
                          for record in caplog.records])
    assert return_codes == expected_return_codes

    # for record in caplog.records:
    #    print(record)
