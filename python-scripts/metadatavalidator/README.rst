Metadata validator for DocBook
==============================

The script in this directory check several metadata definition for DocBook.
Metadata can be found in the ``<meta>`` and ``<info>`` tags.


Requirements
------------

* lxml (the more recent, the better)
* Python >=3.11 (only due to for installing with :file:`pyproject.toml`.)


Preparing the environment
-------------------------

It's recommended to create a Python virtual environment first before you
proceed further. The virtual environment is a self-contained Python environment
that separates the dependencies from the system Python installation.

To create a virtual environment, execute the following steps:

1. Create a virtual environment with Python 3.11:

    .. code-block:: bash

        $ python3.11 -m venv .venv311

1. Activate the virtual environment:

    .. code-block:: bash

        $ source .venv311/bin/activate

    Your prompt changes to show the active virtual environment:

    .. code-block:: bash

        (.venv311) $

1. Upgrade the package manager ``pip`` and ``setuptools`` to the latest version:

    .. code-block:: bash

        (.venv311) $ pip install --upgrade pip setuptools

This makes your virtual environment ready for the next steps.

If you don't need the virtual environment anymore, you can deactivate it:

.. code-block:: bash

    (.venv311) $ deactivate



Installing the script
---------------------

Before you install the script, your current directory must be
`python-scripts/metadatavalidator/`.
To install the script, run the following command:

.. code-block:: bash

    $ pip install .


For development, install the script in "editable" mode:

.. code-block:: bash

    $ pip install -e .[test]


Setting the configuration
-------------------------

Before you call the script, check the values in the configuration file.
The configuration file is an INI file and is searched in the following order (from highest to lowest):

* Command line with :option:`--config`. This doesn't search for other configuration files.
* Environment variable :envar:`METAVALIDATOR_CONFIG`.
* In the current directory: :file:`metadatavalidator.ini`
* In the users' home directory: :file:`~/.config/metadatavalidator/config.ini`
* In the system: :file:`/etc/metadatavalidator/config.ini`

The configuration file is a standard INI file.
All boolean values are case-insensitive and can be ``true``/``yes``, ``on``/``off`` or ``0``/``1``.
Everything else is considered as ``false``.
List values are separated by commas.

All config files are merged together. If a key is defined in multiple files,
the last one wins. This way you can have a global configuration in the
system directory and a local one in the current directory.


Calling the script
------------------

Call the script with the following command:

.. code-block:: bash

    $ metadatavalidator PATH_TO_DOCBOOK_FILES

The script will show all problems with metadata:

.. code-block::

    $ metadatavalidator a.xml b.xml
    ==== RESULTS ====
    [1] a.xml:
      1.1: check_info_revhistory_revision: Missing recommended attribute in /d:article/d:info[2]/d:revhistory[12]/d:revision/@xml:id

    [2] b.xml:
      2.1: check_meta_task: Invalid value in metadata Unknown task(s) {'Clusering'}. Allowed are ...

The output shows:

* The filename.
* The name of the check that the script executed and failed.
* A description of the problem.
* In some cases a line number.


If wanted, you can add your own configuration file with the option :option:`--config`:

.. code-block:: bash

    $ metadatavalidator --config /path/to/config.ini PATH_TO_DOCBOOK_FILES

For machine readable output of the result, use the option :option:`--format`:

.. code-block:: bash

    $ metadatavalidator --format json PATH_TO_DOCBOOK_FILES


Configuration
-------------

The configuration file is search in the following order (first is the highest):

1. Command line with :option:`--config`. This doesn't search for other configuration files.

1. Environment variable :envar:`METAVALIDATOR_CONFIG`.

1. In the current directory: :file:`metadatavalidator.ini`

1. In the users' home directory: :file:`~/.config/metadatavalidator/config.ini`

1. In the system: :file:`/etc/metadatavalidator/config.ini`


Configuration values
--------------------

The following values are recognized:

* :var:`validator`: Global options to configure the validator.
    * :var:`file_extension`: The file extension to search for. Default is
      ``.xml``.

    * :var:`check_root_elements`: List of allowed root elements (space separated by local DocBook name). Default is ``assembly article book topic``.

    * :var:`valid_languages`: List of valid languages (space separated by ISO 639-1 code). Default is ``ar-ar cs-cz de-de en-us es-es fr-fr hu-hu it-it ja-jp ko-kr nl-nl pl-pl pt-br ru-ru sv-se zh-cn zh-tw``.

* :var:`metadata`: Options to change behaviour of specific `<meta>` tags.
    * :var:`require_revhistory`: Requires a ``<revhistory>`` tag or not.

    * :var:`require_xmlid_on_revision`:  Requires a ``xml:id`` attribute on each ``<revision>`` tag or not.

    * :var:`require_meta_title`: Requires a ``<meta name="title">`` tag or not.

    * :var:`meta_title_length`: Checks the length of the text content in ``<meta name="title">``. Default is 55.

    * :var:`require_meta_description`: Requires a ``<meta name="description">`` tag or not.

    * :var:`meta_description_length`: Checks the length of the text content in ``<meta name="description">``. Default is 155.

    * :var:`require_meta_series`: Requires a ``<meta name="series">`` tag or not.

    * :var:`valid_meta_series`: Lists the valid series names for ``<meta name="series">``.

    * :var:`require_meta_techpartner`: Requires a ``<meta name="techpartner">`` tag or not.

    * :var:`require_meta_platform`: Requires a ``<meta name="platform">`` tag or not.

    * :var:`require_meta_architecture`: Requires a ``<meta name="architecture">`` tag or not.

    * :var:`valid_meta_architectures`: Lists the valid architecture names for ``<meta name="architecture">/<phrase>``.

    * :var:`require_meta_category`: Requires a ``<meta name="category">`` tag or not.

    * :var:`valid_meta_categories`: Lists the valid category names for ``<meta name="category">/<phrase>``.

    * :var:`require_meta_task`: Requires a ``<meta name="task">`` tag or not.

    * :var:`valid_meta_tasks`: Lists the valid task names for ``<meta name="task">/<phrase>``.
