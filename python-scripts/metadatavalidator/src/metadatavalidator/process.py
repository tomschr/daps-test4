import asyncio
from argparse import Namespace
# from configparser import ConfigParser
import typing as t
import os.path

from lxml import etree

# from .checks.check_root import check_root_tag, check_namespace
from . import checks
from .exceptions import InvalidValueError, MissingAttributeWarning
from .logging import log
from .util import green, red


def get_all_check_functions(name):
    """"Yield a check function from the :mod:`metadatavalidator.checks`
    package
    """
    import importlib
    module = importlib.import_module(name)
    # The order of the checks is important and uses it from checks.__all__
    for name, obj in module.__dict__.items():
        if callable(obj) and name.startswith("check_"):
            yield obj


async def process_xml_file(xmlfile: str, config: dict[t.Any, t.Any]):
    """Process a single XML file

    :param xmlfile: the XML file to check for meta data
    :param config: read-only configuration from INI file
    """
    errors = []
    basexmlfile = os.path.basename(xmlfile)

    returndict = {
        "xmlfile": xmlfile,
        "absxmlfilename": os.path.abspath(xmlfile),
        "basename": basexmlfile,
    }
    # log.debug("Config %s", config)
    # First check if the file is a well-formed XML file
    # If not, don't bother to check further
    try:
         tree = etree.parse(xmlfile,
                            parser=etree.XMLParser(
                                encoding="UTF-8",
                                # huge_tree=True,
                                resolve_entities=True)
                                )

    except etree.XMLSyntaxError as e:
            # log.fatal("Syntax error in %r: %s", xmlfile, e)
            log.fatal("Syntax error in %r: %s", basexmlfile, e)
            errors.append({
                'checkfunc': None,
                'message': str(e)
            })
            return { **returndict, "errors": errors }

    for checkfunc in get_all_check_functions(checks.__package__):
        log.debug("Checking %r with %r",
                  basexmlfile,
                  checkfunc.__name__)
        try:
            # loop = asyncio.get_running_loop()
            # tree = await loop.run_in_executor(None, etree.parse, xmlfile)
            # Apply check function
            checkfunc(tree, config)
            # await asyncio.sleep(0.1)

        except (InvalidValueError, MissingAttributeWarning) as e:
            #log.fatal("Invalid value in %r for %s: %s",
            #          xmlfile, checkfunc.__name__,  e)
            errors.append({
                'checkfunc': checkfunc.__name__,
                'message': str(e)
            })
        else:
            # log.info("Passed check %r for %r", checkfunc.__name__, basexmlfile)
            pass

    log.info("File %r checked.", basexmlfile)
    return { **returndict, "errors": errors }


def format_results_text(results: list[t.Any]):
    """Format the results for output

    :param results: the results from the checks
    """
    error_template = """[{idx}] {xmlfile}:"""
    ok_template = f"""[{{idx}}] {{xmlfile}}: {green("OK")}"""

    print("==== RESULTS ====")
    for allidx, result in enumerate(results, 1):
        if not result['errors']:
            print(ok_template.format(idx=allidx, **result))
        else:
            print(error_template.format(idx=allidx, **result))

            for idx, error in enumerate(result['errors'], 1):
                msg = red(error['message'])
                print(f"  {allidx}.{idx}: {error['checkfunc']}: {msg}")
            print()


def format_results_json(results: list[t.Any]):
    """Format the results for output

    :param results: the results from the checks
    """
    import json
    print(json.dumps(results, indent=2))


async def process(args: Namespace, config: dict[t.Any, t.Any]):
    """Process all XML files that are passed on CLI

    :param args: the arguments parsed by argparse
    :param config: read-only configuration from INI file
    """
    log.debug("Process all XML files...")
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for xmlfile in args.xmlfiles:
             task = tg.create_task(process_xml_file(xmlfile, config))
             tasks.append(task)

    results = []
    for task in tasks:
        maybeissue = await task
        if maybeissue:
            results.append(maybeissue)

    # Use strategy pattern to format the results
    formatmap = {
        "text": format_results_text,
        "json": format_results_json,
    }

    formatmap[args.format](results)
