import configparser
from pathlib import Path
import re
# import tomllib
import typing as t

from .exceptions import MissingKeyError, MissingSectionError, NoConfigFilesFoundError
from .logging import log


# def read_and_merge_toml_files(*paths: str) -> dict[t.Any, t.Any]:
#     """Read and merge TOML files from given paths.

#     :param paths:
#     :return: the merged configuration as dictionary.
#     """
#     merged_config = {}
#     for path in paths:
#         full_path = Path(path).resolve()
#         if full_path.exists():
#             with open(full_path, mode='rb') as f:
#                 config = tomllib.load(f)
#                 # merged_config.update(config)
#                 merged_config |= config
#     return merged_config

SPLIT = re.compile(r"[;, ]")


def as_dict(config: configparser.ConfigParser) -> dict[str, t.Any]:
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict


def truefalse(value: str|bool|int) -> bool:
    """Convert a string to a boolean value
    """
    if isinstance(value, bool):
        return value

    return str(value).lower() in ("true", "yes", "1", "on")


# def retrievekey(config: configparser.ConfigParser,
#                 section: str, key: str, default: t.Any = None) -> t.Any:
#     """Retrieve a key from a section in a config file

#     :param config: the configuration object
#     :param section: the section to look for
#     :param key: the key to look for
#     :param default: the default value if the key is not found
#     :return: the value of the key
#     """
#     if not config.has_section(section):
#         raise MissingSectionError(section)
#     return config.get(section, key, fallback=default)


# def get_metadata(config: configparser.ConfigParser, key) -> dict[str, t.Any]:
#     """Retrieve the metadata section from the config

#     :param config: the configuration object
#     :return: a dictionary with the metadata section
#     """
#     return retrievekey(config, "metadata", key)


def validate_check_root_elements(config: dict) -> list[str]:
    """Validate the language section of the config

    :param config: the configuration object
    :return: a list of valid languages
    """
    check_root_elements = config.get("validator", {}).get("check_root_elements")
    if check_root_elements is None:
        raise MissingKeyError("validator.check_root_elements")

    return SPLIT.split(check_root_elements)


def validate_valid_languages(config: dict) -> list[str]:
    """Validate the language section of the config

    :param config: the configuration object
    :return: a list of valid languages
    """

    # valid_languages = retrievekey(config, "validator", "valid_languages")
    valid_languages = config.get("validator", {}).get("valid_languages")
    if valid_languages is None:
        raise MissingKeyError("validator.valid_languages")

    return SPLIT.split(valid_languages)


def validate_meta_title_length(config: dict) -> int:
    """Validate the meta title length

    :param config: the configuration object
    :return: the meta title length
    """
    try:
        meta_title_length = int(config.get("metadata", {}).get("meta_title_length"))
        if meta_title_length < 0:
            raise ValueError("meta_title_length should be a positive integer")
        return meta_title_length

    except TypeError:
        raise MissingKeyError("metadata.meta_title_length")


def validate_meta_description_length(config: dict) -> int:
    """Validate the meta description length

    :param config: the configuration object
    :return: the meta description length
    """
    try:
        meta_description_length = int(config.get("metadata", {}).get("meta_description_length"))
        if meta_description_length < 0:
            raise ValueError("meta_description_length should be a positive integer")
        return meta_description_length

    except TypeError:
        raise MissingKeyError("metadata.meta_description_length")


def validate_valid_meta_series(config: dict) -> list[str]:
    """Validate the meta series

    :param config: the configuration object
    :return: a list of valid meta series
    """
    # split = re.compile(r"[;,]")  # no space!
    return [x.strip() for x in re.split(r"[;,]",
                                        config.get("metadata", {}).get("valid_meta_series", "")
                                        )
            if x
            ]


def validate_valid_meta_architectures(config: dict) -> list[str]:
    """Validate the meta architecture

    :param config: the configuration object
    :return: a list of valid meta architecture
    """
    return [x.strip() for x in re.split(r"[;,]",
                                        config.get("metadata", {}).get("valid_meta_architectures", "")
                                        )
                if x
            ]


def validate_valid_meta_categories(config: dict) -> list[str]:
    """Validate the meta category

    :param config: the configuration object
    :return: a list of valid meta category
    """
    return [x.strip() for x in re.split(r"[;,]",
                                        config.get("metadata", {}).get("valid_meta_categories", "")
                                        )
                if x
            ]


def validate_valid_meta_tasks(config: dict) -> list[str]:
    """Validate the meta task

    :param config: the configuration object
    :return: a list of valid meta task
    """
    return [x.strip() for x in re.split(r"[;,]",
                                        config.get("metadata", {}).get("valid_meta_tasks", "")
                                        )
                if x
            ]


def validate_and_convert_config(config: configparser.ConfigParser) -> dict[t.Any, t.Any]:
    """Validate sections, keys, and their values of the config

    :param config: the :class:`configparser.Configparser` object
    :return: a dict that contains converted keys into their
             respective datatypes
    """
    # TODO: This should be better used with pydantic
    if not config.has_section("validator"):
        raise MissingSectionError("validator")
    if not config.has_section("metadata"):
        raise MissingSectionError("metadata")

    theconfig = as_dict(config)
    # Section "validator"
    theconfig["validator"]["check_root_elements"] = validate_check_root_elements(theconfig)
    theconfig["validator"]["valid_languages"] = validate_valid_languages(theconfig)

    # Section "metadata"
    # <revhistory>
    theconfig.setdefault("metadata", {})[
        "require_revhistory"
    ] = truefalse(theconfig.get("metadata", {}).get("require_revhistory", True))
    theconfig.setdefault("metadata", {})[
        "require_xmlid_on_revision"
    ] = truefalse(theconfig.get("metadata", {}).get("require_xmlid_on_revision", True))

    # <meta name="title">
    theconfig.setdefault("metadata", {})[
        "meta_title_length"
    ] = validate_meta_title_length(theconfig)

    # <meta name="description">
    theconfig.setdefault("metadata", {})[
        "require_meta_description"
    ] = truefalse(theconfig.get("metadata", {}).get("require_meta_description", False))
    theconfig.setdefault("metadata", {})[
        "meta_description_length"
    ] = validate_meta_description_length(theconfig)

    # <meta name="series">
    theconfig.setdefault("metadata", {})[
        "require_meta_series"
    ] = truefalse(theconfig.get("metadata", {}).get("require_meta_series", False))
    theconfig.setdefault("metadata", {})[
        "valid_meta_series"
    ] = validate_valid_meta_series(theconfig)

    # <meta name="architecture">
    theconfig.setdefault("metadata", {})[
        "require_meta_architecture"
        ] = truefalse(theconfig.get("metadata", {}).get("require_meta_architecture",
                                                        False))
    theconfig.setdefault("metadata", {})[
        "valid_meta_architectures"
    ] = validate_valid_meta_architectures(theconfig)

    # <meta name="techpartner">
    require_meta_techpartner = truefalse(
        theconfig.get("metadata", {}).get("require_meta_techpartner", False)
    )
    theconfig.setdefault("metadata", {})[
        "require_meta_techpartner"
    ] = require_meta_techpartner

    # <meta name="platform">
    theconfig.setdefault("metadata", {})[
        "require_meta_platform"
    ] = truefalse(theconfig.get("metadata", {}).get("require_meta_platform", False))

    # <meta name="category">
    theconfig.setdefault("metadata", {})[
        "require_meta_category"
    ] = truefalse(theconfig.get("metadata", {}).get("require_meta_category", False))
    theconfig.setdefault("metadata", {})[
        "valid_meta_categories"
    ] = validate_valid_meta_categories(theconfig)

    # <meta name="task">
    theconfig.setdefault("metadata", {})[
        "require_meta_task"
    ] = truefalse(theconfig.get("metadata", {}).get("require_meta_task", False))
    theconfig.setdefault("metadata", {})[
        "valid_meta_tasks"
    ] = validate_valid_meta_tasks(theconfig)

    # Store the configfiles
    theconfig["configfiles"] = getattr(config, "configfiles")
    return theconfig


def readconfig(dirs: t.Sequence) -> dict[t.Any, t.Any]:  # configparser.ConfigParser
    """Read config data from config files

    :param dirs: the directories to search for config files
    :return: a :class:`configparser.ConfigParser` object
    """
    config = configparser.ConfigParser()
    configfiles = config.read(dirs)
    if not configfiles:
        raise NoConfigFilesFoundError("Config files not found")
    setattr(config, "configfiles", configfiles)

    return validate_and_convert_config(config)

