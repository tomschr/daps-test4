import pytest

from _utils import appendnode, D, xmlid

from metadatavalidator.common import NAMESPACES
from metadatavalidator.checks.check_meta import (
    check_meta_category,
    check_meta_task,
)
from metadatavalidator.exceptions import InvalidValueError


def test_meta_task(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="task">
#             <phrase>Configuration</phrase>
#         </meta>
#     </info>
# </article>"""
    meta = D("meta", {"name": "task"},
             D("phrase", "Configuration")
             )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_task=True,
                                valid_meta_tasks=["Configuration"]))
    assert check_meta_task(tree, config) is None


def test_missing_required_meta_task(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#     </info>
# </article>"""
    config = dict(metadata=dict(require_meta_task=True,
                                valid_meta_tasks=["Configuration"]))
    with pytest.raises(InvalidValueError,
                          match=r".*Couldn't find required meta\[@name='task'\].*"):
          check_meta_task(tree, config)


def test_missing_child_meta_task(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="task"/>
#     </info>
# </article>"""
    meta = D("meta", {"name": "task"})
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_task=True),
                                valid_meta_tasks=["Configuration"])
    with pytest.raises(InvalidValueError,
                       match=r".*Couldn't find any child elements in meta.*"):
        check_meta_task(tree, config)


def test_duplicate_child_meta_task(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="task">
#             <phrase>Configuration</phrase>
#             <phrase>Configuration</phrase>
#         </meta>
#     </info>
# </article>"""
    meta = D("meta", {"name": "task"},
             D("phrase", "Configuration"),
             D("phrase", "Configuration"),
             )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_task=True),
                                valid_meta_tasks=["Configuration"])
    with pytest.raises(InvalidValueError,
                       match=r".*Duplicate tasks found in meta.*"):
        check_meta_task(tree, config)


def test_unknown_child_meta_task(tree):
#     xmlcontent = """<article xmlns="http://docbook.org/ns/docbook" version="5.2">
#     <info>
#         <title>Test</title>
#         <meta name="task">
#             <phrase>Configuration</phrase>
#             <phrase>Unknown</phrase>
#         </meta>
#     </info>
# </article>"""
    meta = D("meta", {"name": "task"},
             D("phrase", "Configuration"),
             D("phrase", "Unknown"),
             )
    appendnode(tree, meta)

    config = dict(metadata=dict(require_meta_task=True,
                                valid_meta_tasks=["Configuration"]))
    with pytest.raises(InvalidValueError,
                       match=r".*Unknown task\(s\) \{'Unknown'\}.*"):
        check_meta_task(tree, config)