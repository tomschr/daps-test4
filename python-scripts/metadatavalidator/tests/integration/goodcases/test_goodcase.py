import os.path
import json
import pytest

from metadatavalidator.cli import main


BASEDIR = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH = os.path.relpath(BASEDIR, os.getcwd())


def test_integr_article(capsys):
    xmlfile = f"{RELATIVE_PATH}/article.xml"
    cli = ["--config", f"{BASEDIR}/config-test.ini",
           "--format", "json",  # needed to avoid formatting issues
           xmlfile]

    result = main(cli)
    captured = capsys.readouterr()
    assert result == 0
    result = json.loads(captured.out)
    assert result[0]['errors'] == []
    assert result[0]['xmlfile'] == xmlfile


def test_integr_xml_with_entity_in_doctype(capsys):
    xmlfile = f"{RELATIVE_PATH}/article-with-entity-in-doctype.xml"
    cli = ["--config", f"{BASEDIR}/config-test.ini",
           "--format", "json",  # needed to avoid formatting issues
           xmlfile]

    result = main(cli)
    captured = capsys.readouterr()
    assert result == 0
    result = json.loads(captured.out)
    assert result[0]['errors'] == []
    assert result[0]['xmlfile'] == xmlfile


@pytest.mark.skip(reason="Works locally but not on CI")
def test_integr_xml_with_external_entity_in_nested_dir(capsys):
    xmlfile = f"{RELATIVE_PATH}/nested-dir/a/b/article-with-external-entity.xml"
    cli = ["--config", f"{BASEDIR}/config-test.ini",
           "--format", "json",  # needed to avoid formatting issues
           xmlfile]

    result = main(cli)
    captured = capsys.readouterr()
    assert result == 0
    result = json.loads(captured.out)
    assert result[0]['errors'] == []
    assert result[0]['xmlfile'] == xmlfile