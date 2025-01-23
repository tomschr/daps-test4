from configparser import ConfigParser
import os.path

import pytest

from metadatavalidator.config import (
    readconfig,
    truefalse,
    validate_check_root_elements,
    validate_and_convert_config,
    validate_valid_meta_architectures,
    )
from metadatavalidator.exceptions import (
    MissingKeyError,
    MissingSectionError,
    NoConfigFilesFoundError,
    )


@pytest.mark.parametrize("value, expected", [
    ("true", True),
    ("True", True),
    ("false", False),
    ("False", False),
    ("1", True),
    ("0", False),
    ("on", True),
    ("off", False),
    ("On", True),
    ("Off", False),
    (True, True),
    (False, False),
    (1, True),
    (0, False),
])
def test_truefalse(value, expected):
    assert truefalse(value) == expected


def test_valid_validate_and_convert_config(config):
    result = validate_and_convert_config(config)
    assert result.get("validator") == {
            "check_root_elements": ["book", "article"],
            "file_extension": ".xml",
            "valid_languages": ["en-us", "de-de",],
            # ""
        }


def test_missing_config_files():
    with pytest.raises(NoConfigFilesFoundError, match=".*Config files not found.*"):
        readconfig([])


def test_missing_validator_section():
    config = ConfigParser()
    with pytest.raises(MissingSectionError, match=".*validator.*"):
        validate_and_convert_config(config)


def test_missing_metadata_section():
    config = ConfigParser()
    config.add_section("validator")
    with pytest.raises(MissingSectionError, match=".*metadata.*"):
        validate_and_convert_config(config)


def test_missing_key_check_root_elements(config):
    config.remove_option("validator", "check_root_elements")
    with pytest.raises(MissingKeyError, match=".*validator.check_root_elements.*"):
        validate_and_convert_config(config)


def test_missing_key_valid_languages(config):
    config.remove_option("validator", "valid_languages")
    with pytest.raises(MissingKeyError, match=".*validator.valid_languages.*"):
        validate_and_convert_config(config)


def test_missing_key_meta_title_length(config):
    config.remove_option("metadata", "meta_title_length")
    with pytest.raises(MissingKeyError, match=".*metadata.meta_title_length.*"):
        validate_and_convert_config(config)


def test_meta_title_length_not_positive(config):
    config.set("metadata", "meta_title_length", "-1")
    with pytest.raises(ValueError, match=".*meta_title_length should be a positive integer.*"):
        validate_and_convert_config(config)


def test_meta_description_length_not_positive(config):
    config.set("metadata", "meta_description_length", "-1")
    with pytest.raises(ValueError, match=".*meta_description_length should be a positive integer.*"):
        validate_and_convert_config(config)


def test_missing_key_meta_description_length(config):
    config.remove_option("metadata", "meta_description_length")
    with pytest.raises(MissingKeyError, match=".*metadata.meta_description_length.*"):
        validate_and_convert_config(config)


def test_readconfig():
    configfile = os.path.join(os.path.dirname(__file__), "data/metadatavalidator.ini")
    result = readconfig([configfile])
    assert result.get("validator") == {
            "check_root_elements": ["book", "article", "topic"],
            "file_extension": ".xml",
            "valid_languages": ["de-de", "en-us", "es-es", "fr-fr"]
        }
    assert result.get("configfiles") == [configfile]


def test_validate_check_root_elements(dict_config):
    assert validate_check_root_elements(dict_config) == ["book", "article"]

def test_validate_check_root_elements_missing_key(dict_config):
    dict_config["validator"].pop("check_root_elements")
    with pytest.raises(MissingKeyError, match=".*validator.check_root_elements.*"):
        validate_check_root_elements(dict_config)

def test_validate_valid_meta_architectures(dict_config):
    assert validate_valid_meta_architectures(dict_config) == ["A", "B", "C"]