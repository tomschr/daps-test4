# Adding missing metadata to DocBook files

The stylesheet in this folder adds missing SUSE metadata into `<info>` tag.

The stylesheet tries to find a specific `<meta>` tag.
If the tag is available, it copies the tag to the result tree without changes.
If the respective tag is missing, the stylesheet creates the tag in the
result tree. With parameters, you can influence if the tag should be created
at all and what content it should have.


# Preparing the XML files

If you want to preserver your entities, make sure you "mask" them appropriately.
See the directory `contrib/entities-exchange/` in this repo.


# Using the stylesheet

In its simplest form, call it like this:

    $ xsltproc --output XML_FILE.xml.new add-metadata.xsl XML_FILE.xml

Load the `XML_FILE.xml.new` file in your editor, search for `FIXME` and
replace it with the respective values.

If you want to "bulk-edit" a specific set of XML files, use a `for` loop:

    $ for xml in A.xml B.xml C.xml; do
       xsltproc --output ${xml}.new add-metadata.xsl ${xml}
      done

After you have edited the files, rename it and overwrite the original files:

    $ for i in *.xml.new; do
         xml=${i%*.new}
         mv -vi ${i} ${xml}
       done


# Using parameters

If you know some values for some meta information, it's easier to spare some
time and provide the necessary value(s) through parameters.

For example, if you want to add the series for several XML files, use this
approach:

    $ for xml in A.xml B.xml C.xml; do
         xsltproc --stringparam meta-series "My series" \
            --output $xml.new \
            add-metadata.xsl \
            $xml
      done

Some meta tags contains child elements like `<phrase>`. By default, use a comma-separated list of strings like in this example:

    $ xsltproc --stringparam meta-category A,B,C add-metadata.xsl XML_FILE.xml

This will create:

    <meta name="category">
      <phrase xmlns:d="http://docbook.org/ns/docbook">A</phrase>
      <phrase xmlns:d="http://docbook.org/ns/docbook">B</phrase>
      <phrase xmlns:d="http://docbook.org/ns/docbook">C</phrase>
    </meta>

If you want to introduce entities, there is a small problem. The ampersand (&)
is masked and appears as `&amp;` in the output.
You need to change it either in your editor or with `sed`.


# Enableing/disabling meta tags

In some cases, you don't want to add a specific meta tag. For example, for TRD, only `<meta name="type">` is useful. Other documentation should not receive this tag.

Any parameter to enable or disable starts with `use-meta-`. Pass the option `--param` and as value `0` or `"false()"` to disable and `1` and `"true()"`
to enable. For example, to not add `<meta name="type">` to your result tree,
use this:

    $ xsltproc --param use-meta-type 0 add-metadata.xsl XML_FILE.xml

Same for the other meta tags.


# Metadata parameter reference

* `meta-arch`: Comma separated list of architectures to add for `<meta name="architecture">`
* `meta-category`: Comma separated list of categories to add for `<meta name="category">`
* `meta-series`: String to add for `<meta name="series">`
* `meta-task`: Comma separated list of tasks to add for `<meta name="task">`
* `meta-type`: Comma separated list of tasks to add for `<meta name="type">`

# Parameters for enabling/disabling meta tags
Each parameter expects a boolean value like `0`/`false()` to disable, or
`1`/`true()` to enable. Pass the option `--param` for `xsltproc`.

* `use-meta-arch`: Enable/disable `<meta name="arch">`
* `use-meta-category`: Enable/disable `<meta name="series">`
* `use-meta-description`: Enable/disable `<meta name="description">`
* `use-meta-series`: Enable/disable `<meta name="series">`
* `use-meta-task`: Enable/disable `<meta name="task">`
* `use-meta-type` (default disabled): Enable/disable `<meta name="type">`

# General parameter reference
* `delim`: The delimiter used to separate each parameter (by default ",")
* `default-text`: The default text to use when we create an element with text
