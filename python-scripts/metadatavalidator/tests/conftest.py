from configparser import ConfigParser
import os, os.path
import typing as t

from lxml import etree
import pytest

from metadatavalidator.config import as_dict


os.environ.setdefault("PYTHONPATH",
                      os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def xmlparser():
    return etree.XMLParser(encoding="UTF-8")


@pytest.fixture
def xmlcontent() -> str:
    return """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
    <info>
        <title>Test</title>
        <!-- We add here additional content in the respective tests -->
    </info>
</article>"""


@pytest.fixture
def tree(xmlcontent, xmlparser) -> etree._ElementTree:
    return etree.ElementTree(etree.fromstring(xmlcontent, parser=xmlparser))


@pytest.fixture
def assemblystr() -> str:
    return """<assembly version="5.2"
       xml:lang="en"
       xmlns:xlink="http://www.w3.org/1999/xlink"
       xmlns:trans="http://docbook.org/ns/transclusion"
       xmlns:its="http://www.w3.org/2005/11/its"
       xmlns:xi="http://www.w3.org/2001/XInclude"
       xmlns="http://docbook.org/ns/docbook">
       <structure>
         <merge>
              <!-- We add here additional content in the respective tests -->
         </merge>
       </structure>
</assembly>"""


@pytest.fixture
def asmtree(assemblystr, xmlparser) -> etree._ElementTree:
    return etree.ElementTree(etree.fromstring(assemblystr, parser=xmlparser))


@pytest.fixture(scope="function")
def config() -> ConfigParser:
    config = ConfigParser()
    config.add_section("validator")
    config.set("validator", "check_root_elements", "book article")
    config.set("validator", "file_extension", ".xml")
    config.set("validator", "valid_languages", "en-us de-de")
    #
    config.add_section("metadata")
    config.set("metadata", "revhistory", "0")
    config.set("metadata", "require_xmlid_on_revision", "true")
    config.set("metadata", "meta_title_length", "50")
    config.set("metadata", "meta_description_length", "150")
    #
    config.set("metadata", "valid_meta_architectures", "A, B, C")
    config.set("metadata", "valid_meta_categories", "D, E, F")
    setattr(config, "configfiles", None)
    return config


@pytest.fixture(scope="function")
def dict_config(config) -> dict[str, t.Any]:
    return as_dict(config)
