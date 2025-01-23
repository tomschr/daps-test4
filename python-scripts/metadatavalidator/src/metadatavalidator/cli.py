"""
Parses a XML file and checks for metadata. Can be applied for regular
DocBook files and assembly files.

For "Suggested values and structure" see:
https://confluence.suse.com/x/aQDWNg
"""
import argparse
import asyncio
import logging
from logging.config import dictConfig
import sys
import typing as t

from . import __author__, __version__
from .config import readconfig
from .common import CONFIGDIRS
from .exceptions import BaseConfigError, NoConfigFilesFoundError
from .logging import DEFAULT_LOGGING_DICT, LOGLEVELS, log
from .process import process

#: Change root logger level from WARNING (default) to NOTSET
#: in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)

PROGPATH = sys.argv[0]

def parsecli(cliargs=None) -> argparse.Namespace:
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result
    :param cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    """
    epilog = f"""
{__package__} {__version__} written by {__author__} from {PROGPATH}
"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog=epilog,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     )

    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0, # emit warnings, errors, and critical
                        help="increase verbosity level")

    parser.add_argument('-C', '--config',
                        help="The configuration file to use (disables other systems or home configuration files)",
                        metavar="CONFIGFILE",)

    parser.add_argument('-F', '--format',
                        help="Output format (default %(default)r)",
                        choices=["text", "json"],
                        default="text"
                        )

    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {__version__} written by {__author__}'
                        )
    parser.add_argument("xmlfiles",
                        metavar="XMLFILES",
                        nargs="+",
                        help="Searches for metadata in the XML file"
                        )

    args = parser.parse_args(args=cliargs)
    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    # Setup logging and the log level according to the "-v" option
    # If user requests more, cut it and return always DEBUG
    loglevel = LOGLEVELS.get(args.verbose, logging.DEBUG)

    # Set console logger to the requested log level
    for handler in log.handlers:
        if handler.name == "console":
            handler.setLevel(loglevel)

    return args


def main(cliargs=None) -> int:
    """Entry point for the application script
    :param cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    """
    try:
        # just try to import lxml.etree
        from lxml import etree  # noqa: F401

        args = parsecli(cliargs)
        # Either use the config file from the CLI or the default config files
        if args.config is None:
            configfiles = CONFIGDIRS
        else:
            configfiles = [args.config]
        config = readconfig(configfiles)
        args.config = config
        log.debug("CLI args %s", args)

        asyncio.run(process(args, config))

        return 0

    except ImportError as error:
        log.critical("lxml is not installed")
        return 50

    except NoConfigFilesFoundError as error:
        log.critical("No config files found")
        return 100

    except BaseConfigError as error:
        log.critical(error)
        return 150

    except Exception as error:  # FIXME: add a more specific exception here!
        log.exception("Some unknown exception occured", error)
        # Use whatever return code is appropriate for your specific exception
        return 200


if __name__ == "__main__":
    sys.exit(main())