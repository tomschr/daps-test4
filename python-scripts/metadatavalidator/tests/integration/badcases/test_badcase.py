import os.path
import json
import re
import pytest

from metadatavalidator.cli import main


BASEDIR = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH = os.path.relpath(BASEDIR, os.getcwd())


def test_integr_case1(capsys):
    cli = ["--config", f"{BASEDIR}/config-test.ini",
           "--format", "json",  # needed to avoid formatting issues
           f"{RELATIVE_PATH}/article.xml"]

    result = main(cli)
    captured = capsys.readouterr()
    assert result == 0
    result = json.loads(captured.out)
    assert result[0]['errors'] == []
    assert result[0]['xmlfile'] == f"{RELATIVE_PATH}/article.xml"



def test_integr_xml_with_syntax_error(capsys):
    cli = ["--config", f"{BASEDIR}/config-test.ini",
           "--format", "json",  # needed to avoid formatting issues
           f"{RELATIVE_PATH}/article-invalid.xml"]

    result = main(cli)
    captured = capsys.readouterr()
    assert result == 0
    result = json.loads(captured.out)
    message = result[0]['errors'][0]['message']
    # "Opening and ending tag mismatch: para line 6 and article, line 7, column 11 (article-invalid.xml, line 7)"
    assert re.match(r"Opening and ending tag mismatch:", message)
    assert result[0]['xmlfile'] == f"{RELATIVE_PATH}/article-invalid.xml"