# known layouts:
#
# Docbook:
#
# docbook4: e.g. /usr/share/xml/docbook/stylesheet/nwalsh/current
# docbook5: e.g. /usr/share/xml/docbook/stylesheet/nwalsh5/current
#
# common.mk automatically detects if $MAIN is docbook5
# or docbook4 and this file uses the stylesheets accordingly.

# The following variables need to be set for a custom layout
#
# STYLEROOT         : path to stylesheet directory, mandatory
# FALLBACK_STYLEROOT: path to alternative stylesheet directory, optional
# HTML_CSS          : css file for HTML (full path), optional
# EPUB_CSS          : css file for EPUB (full path), optional

# A custom layout does not need to provide stylesheets for all targets
# If stylesheet subdirectories for a certain target are not found, we
# will fall back to the docbook stylesheets, or--if specified--to
# FALLBACK_STYLEROOT (with the docbook stylsheets remaining the last resort).
# This allows to only define custom stylesheets for e.g. FO but still
# being able to build e.g. HTML
#
# The subdirectory layout in each STYLEROOT directory needs to be the same as
# in the original DocBook stylesheet directories

#----------------------------
# Stylesheet root directories
#
# 

ifeq ($(DOCBOOK_VERSION), 4)
  STYLE_DOCBOOK := $(DOCBOOK4_STYLES)
  EPUB_RUBY_SCRIPT := "$(DOCBOOK4_STYLES)/epub/bin/dbtoepub"
endif
ifeq ($(DOCBOOK_VERSION), 5)
  # the DocBook 5 XSLT 1.0 stylesheets are not available for
  # all targets (epub, for example, is missing), therefore we
  # need the DocBook4 stylesheets as a fallback
  STYLE_DOCBOOK := $(DOCBOOK5_STYLES) $(DOCBOOK4_STYLES)
  EPUB_RUBY_SCRIPT := "$(DOCBOOK4_STYLES)/epub/bin/dbtoepub"
endif


STYLE_CUSTOM          := $(STYLEROOT)

# It only makes sense to set a custom fallback when a custom styleroot 
# has been specified
#
ifdef STYLEROOT
  STYLE_CUSTOM_FALLBACK := $(FALLBACK_STYLEROOT)
endif
#
# if DTDROOT was changed on the commandline or in the config, we assume
# we are in "devel" mode and want to use stylesheets from the daps checkout
# This variables purpose is to make the life of the daps developers easier - it
# can not be used when deeloping custom stylesheets - in that case, specify
# SRYLEROOT on teh command line, ENV-file or user config

ifneq ($(DTDROOT), $(DEFAULT_DTDROOT))
#  STYLE_DEVEL           := $(DTDROOT)/suse-xslt
  STYLE_DEVEL           :=
endif

# Create a list with all stylesheet root directories. When setting the
# stylesheets to be used for the targets, the _first_ element from this
# list is used (firstword). As a consequence the ORDER is IMPORTANT!

STYLE_ROOTDIRS := $(wildcard $(STYLE_DEVEL) $(STYLE_CUSTOM) \
		  $(STYLE_CUSTOM_FALLBACK) $(STYLE_DOCBOOK) )


#----------------------------
# Stylesheet directory layout
# We assume that the directory layout for all stylesheet root directories is
# the same


EPUB_XSLT_STYLE := /epub/docbook.xsl
FO_STYLE        := /fo/docbook.xsl
JSP_STYLE       := /jsp/chunk.xsl
MAN_STYLE       := /manpages/docbook.xsl
WIKI_STYLE      := /db2mediawiki/docbook.xsl

# HTML is special, because single-html uses docbook.xsl while chunked html
# uses chunk.xsl. Whatsmore, we optionally allow html4.

ifeq ("$(firstword $(MAKECMDGOALS))", "html")
  H_STYLE := chunk.xsl
else
  H_STYLE := docbook.xsl
endif

ifeq ("$(HTML4)", "yes")
  H_DIR := /html/
else
  H_DIR := /xhtml/
endif

HTML_STYLEDIR := $(addsuffix $(H_STYLE), $(H_DIR))

#----------------------------
# No let's put it all together
# The following variables are actually used to build the targets:
#
# STYLEEPUBXSLT: epub
# STYLEFO:       fo (pdf)
# STYLEH:        html
# STYLEJ:        jsp
# STYLEMAN:      man
# STYLEWIKI:     wiki
#
# STYLE_EPUBCSS: css file for epub
# STYLE_HTMLCSS: cssfile for html
#
# By using ifndef we allow to overwrite the style/css on the command line by
# directly passing e.g. STYLEFO=<PATH> to make

#
# The combination of firstword and wildcard makes the following specifications
# "intelligent". wildcard filters the list of files to only include the ones
# that really exist, while firstword picks the first element of that
# list.
# So existing files are chosen in the order defined in $STYLE_ROOTDIRS
# So the DocBook stylesheets always raima the last resort

ifndef STYLEEPUBXSLT
  STYLEEPUBXSLT := $(firstword $(wildcard $(addsuffix $(EPUB_XSLT_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif
ifndef STYLEFO
  STYLEFO       := $(firstword $(wildcard $(addsuffix $(FO_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif
ifndef STYLEH
  STYLEH        := $(firstword $(wildcard $(addsuffix $(HTML_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif
ifndef STYLEJ
  STYLEJ        := $(firstword $(wildcard $(addsuffix $(JSP_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif
ifndef STYLEMAN
  STYLEMAN      := $(firstword $(wildcard $(addsuffix $(MAN_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif
ifndef STYLEWIKI
  STYLEWIKI     := $(firstword $(wildcard $(addsuffix $(WIKI_STYLE), \
		   $(STYLE_ROOTDIRS))))
endif

#
# CSS
ifndef STYLE_HTMLCSS
  STYLE_HTMLCSS := $(HTML_CSS)
endif
ifndef STYLE_EPUBCSS
  STYLE_EPUBCSS := $(EPUB_CSS)
endif


# inform  the stylesheets about the used fop processor
#
# FIXME - this should go into a wrapper script
#
ifeq ($(FOPTYPE), fop)
FOCOLSTRINGS  += --stringparam fop1.extensions 1 \
                 --stringparam xep.extensions 0
FOSTRINGS  += --stringparam fop1.extensions 1 \
              --stringparam xep.extensions 0
ifeq ($(DTDROOT), $(DEFAULT_DTDROOT))
FOP_CONFIG_FILE ?=/etc/daps/fop/fop-daps.xml
else
FOP_CONFIG_FILE ?=$(DTDROOT)/etc/fop/fop-daps.xml 
endif
else
ifeq ($(DTDROOT), $(DEFAULT_DTDROOT))
FOP_CONFIG_FILE ?=/etc/daps/xep/xep-daps.xml
else
FOP_CONFIG_FILE ?=$(DTDROOT)/etc/xep/xep-daps.xml 
endif
endif
