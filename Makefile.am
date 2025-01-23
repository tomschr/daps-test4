# Copyright (C) 2012-2020 SUSE Software Solutions Germany GmbH
#
# Author:
# Frank Sundermeyer <fsundermeyer at opensuse dot org>
#
# Makefile.am for DocBook Authoring and Publishing Suite (daps)
# Generate catalogs and install daps
#
#
# TODO:
# Stylesheets for building xhtml need to be packaged in src tar

#------------------------
AUTOMAKE_OPTIONS = 1.10 foreign dist-bzip2 no-dist-gzip no-installinfo \
			-Wall -Werror -Wno-portability
ACLOCAL_AMFLAGS = -I m4
SUBDIRS = 

# additional files to add to the tarball
EXTRA_DIST := COPYING-2.0 COPYING-3.0 packaging/daps.spec

#------------------------
# Replace placeholders with distribution-specfic paths
#

REPL_PATH = sed \
             -e 's|@sysconfdir[@]|$(sysconfdir)|g' \
             -e 's|@bindir[@]|$(bindir)|g' \
             -e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
             -e 's|@datadir[@]|$(datadir)|g' \
             -e 's|@prefix[@]|$(prefix)|g' \
             -e 's|@db5version[@]|$(db5_version)|g' \
             -e 's|@PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g'

DAPSROOT     := $(abs_top_srcdir)

#------------------------
# Build directory - all generated files go there
#
BUILD_ROOT   := build
FIRSTBUILD   := $(BUILD_ROOT)/.firstbuild

#------------------------
# Catalog
#
DAPS_CATALOG_DIR      := $(BUILD_ROOT)/catalog.d
DAPS_CATALOG          := $(DAPS_CATALOG_DIR)/$(PACKAGE).xml

#------------------------
# fop config / jing wrapper
#
FOP_CONFIG           := etc/fop/fop-daps.xml
FOP_CONFIG_DEFAULT   := etc/fop/fop-daps.generic
JING_WRAPPER         := libexec/daps-jing
JING_WRAPPER_DEFAULT := libexec/daps-jing.generic
if !DIST_DEBIAN
  DAPS_CATALOG_TEMPLATE := etc/catalog.generic
endif
if DIST_SUSE
  FOP_CONFIG_SRC   := etc/fop/fop-daps.suse
endif
if DIST_SUSEBS
  FOP_CONFIG_SRC := etc/fop/fop-daps.suse
endif
if DIST_REDHAT
  FOP_CONFIG_SRC := etc/fop/fop-daps.redhat
endif
if DIST_DEBIAN
  JING_WRAPPER_SRC      := libexec/daps-jing.debian
  DAPS_CATALOG_TEMPLATE := etc/catalog.debian
endif

#------------------------
# Saxon
SAXON_CONFIG := etc/saxon/saxon.conf
if HAS_SAXON
	SAXON_CONFIG_SRC := etc/saxon/saxon${SAXON_VERSION}.conf
else
	SAXON_CONFIG_SRC := etc/saxon/saxon10.conf
endif

# stylesheets
if HAS_DAPS_XSL
  STYLEROOT := $(daps_xsl)
else
  STYLEROOT := $(patsubst //%,%,$(patsubst file:%,%,$(shell $(XMLCATALOG) $(root_catalog) $(db4_xslt_url))))
endif


# Man pages
DC_MANPAGES    := DC-daps-manpages
MAN_PAGE_DIR   := $(subst DC-,,$(DC_MANPAGES))
MAN_PAGES      := daps.1 ccecho.1 daps-init.1 daps-autobuild.1
MAN_BUILD_PATH := $(srcdir)/man/build/$(MAN_PAGE_DIR)/man/

# Manuals
DC_USERGUIDE    := $(srcdir)/doc/DC-daps-user
DC_QUICKSTART   := $(srcdir)/doc/DC-daps-quick
DC_ADOCGUIDE    := $(srcdir)/doc/DC-daps-asciidoc
USERGUIDE_NAME  := daps-user
QUICKSTART_NAME := daps-quick
ADOCGUIDE_NAME  := daps-asciidoc
USERGUIDE       := $(srcdir)/doc/build/$(USERGUIDE_NAME)/single-html/$(USERGUIDE_NAME)/$(USERGUIDE_NAME).html
QUICKSTART      := $(srcdir)/doc/build/$(QUICKSTART_NAME)/single-html/$(QUICKSTART_NAME)/$(QUICKSTART_NAME).html
ADOCGUIDE       := $(srcdir)/doc/build/$(ADOCGUIDE_NAME)/single-html/$(ADOCGUIDE_NAME)/$(ADOCGUIDE_NAME).html
MANUALS         := $(dir $(USERGUIDE)) $(dir $(QUICKSTART))
if HAS_ASCIIDOCTOR
  MANUALS += $(dir $(ADOCGUIDE))
endif

#------------------------
# Installation hooks
#
dapsconfdir    = @sysconfdir@/daps
fopconfdir     = $(dapsconfdir)/fop
xepconfdir     = $(dapsconfdir)/xep
hyphendir      = $(xepconfdir)/hyphen
saxondir       = $(dapsconfdir)/saxon

catalogdir     = @sysconfdir@/xml/catalog.d

dapslibdir     = $(pkgdatadir)/lib
dapslibexecdir = $(pkgdatadir)/libexec
dapsmakedir    = $(pkgdatadir)/make
emacssitedir   = @datadir@/emacs/site-lisp
templatedir    = $(pkgdatadir)/init_templates
bashcompletiondir =@datadir@/bash-completion/completions

htmldocdir     = @docdir@/html

xsltdir          = $(pkgdatadir)/daps-xslt
xsltasciidocdir  = $(xsltdir)/asciidoc
xsltcommondir    = $(xsltdir)/common
xsltcontribdir   = $(xsltdir)/contrib
xsltdesktopdir   = $(xsltdir)/desktop
xsltepubdir      = $(xsltdir)/epub
xsltindexdir     = $(xsltdir)/index
xsltlibdir       = $(xsltdir)/lib
xsltmallarddir   = $(xsltdir)/mallard
xsltmigratedir   = $(xsltdir)/migrate
xsltprofilingdir = $(xsltdir)/profiling
xsltrelnotesdir  = $(xsltdir)/relnotes
xsltxhtmldir     = $(xsltdir)/xhtml
xsltyelpdir      = $(xsltdir)/yelp

#------------------------
# Automake primaries

# BIN
dist_bin_SCRIPTS         = $(wildcard bin/*[^.in] $(BUILD_ROOT)/bin/*)
# exclude daps-jing.*
dist_dapslibexec_SCRIPTS = $(filter-out $(wildcard libexec/daps-jing.*),$(wildcard libexec/*))

# CONFIG files
dist_dapsconf_DATA    = etc/config etc/docbook-xmlformat.conf \
			etc/docbook-xmlformat-1.04.conf \
			etc/docbook-xmlformat-1.9.conf \
			etc/CatalogManager.properties
dist_fopconf_DATA     = etc/fop/fop-daps.xml
dist_xepconf_DATA     = etc/xep/xep-daps.xml
dist_hyphen_DATA      = $(wildcard etc/xep/hyphen/*.tex) \
			$(wildcard etc/xep/hyphen/*.il2)
# BASH completion
dist_bashcompletion_DATA = bash_completion/daps
# Saxon config file
dist_saxon_DATA = etc/saxon/saxon${SAXON_VERSION}.conf

# DATA
if !CATALOG_EDIT
dist_catalog_DATA   = $(DAPS_CATALOG)
endif
dist_dapslib_DATA       = $(wildcard lib/*)
dist_emacssite_DATA     = misc/docbook_macros.el
dist_dapsmake_DATA      = $(wildcard make/*.mk)
dist_template_DATA      = $(wildcard init_templates/*)
dist_xsltasciidoc_DATA  = $(wildcard daps-xslt/asciidoc/*.xsl)
dist_xsltcommon_DATA    = $(wildcard daps-xslt/common/*.xsl) \
			   $(wildcard daps-xslt/common/*.xml) \
			   $(wildcard daps-xslt/common/*.svg)
dist_xsltcontrib_DATA   = $(wildcard daps-xslt/contrib/*.xsl)
dist_xsltdesktop_DATA   = $(wildcard daps-xslt/desktop/*.xsl)
dist_xsltepub_DATA      = $(wildcard daps-xslt/epub/*.xsl)
dist_xsltindex_DATA     = $(wildcard daps-xslt/index/*.xsl)
dist_xsltlib_DATA       = $(wildcard daps-xslt/lib/*.xsl)
dist_xsltmallard_DATA   = $(wildcard daps-xslt/mallard/*.xsl)
dist_xsltmigrate_DATA   = $(wildcard daps-xslt/migrate/*.xsl)
dist_xsltprofiling_DATA = $(wildcard daps-xslt/profiling/*.xsl)
dist_xsltrelnotes_DATA  = $(wildcard daps-xslt/relnotes/*.xsl)
dist_xsltxhtml_DATA     = $(wildcard daps-xslt/xhtml/*.xsl)
dist_xsltyelp_DATA      = $(wildcard daps-xslt/yelp/*.xsl)

# DOCUMENTATION
dist_doc_DATA      = BUGS COPYING COPYING-2.0 COPYING-3.0 INSTALL.adoc \
			README.adoc README.quickstart.adoc
dist_man1_MANS      = $(addprefix $(MAN_BUILD_PATH), $(MAN_PAGES))



#---------------------------Local TARGETS--------------------------------------

#
# These targets need to be built _after_ the guides have been built, to make
# sure the local config, as provided by the repo, is used. Otherwise we have
# a mixture of system and repo setup and that will not work

#
# Only build the adoc guide if asciidoctor is installed
#
if HAS_ASCIIDOCTOR
  bin/daps bin/daps-xmlformat etc/config $(FOP_CONFIG) $(JING_WRAPPER): $(ADOCGUIDE)
  all-local: $(ADOCGUIDE)
endif

bin/daps bin/daps-xmlformat etc/config $(FOP_CONFIG) $(JING_WRAPPER): $(USERGUIDE) $(QUICKSTART) $(dist_man1_MANS)

all-local: $(USERGUIDE) $(QUICKSTART) $(dist_man1_MANS) $(DAPS_CATALOG)


#---------------------------Local INSTALLATION--------------------------------

INSTALLDIRS = $(DESTDIR)$(docdir)/html $(DESTDIR)$(pkgdatadir) \
	$(DESTDIR)$(datadir)/xml/$(PACKAGE)/schema/ \
	$(DESTDIR)$(templatedir)


install-data-local: $(INSTALLDIRS) autobuild/daps-autobuild
install-data-local: TMP_CATALOG := $(shell mktemp -q $(BUILD_ROOT)/daps_catalog.XXXXX)
install-data-local:
	for BOOK in $(MANUALS); do \
	  tar c --mode=u+w,go+r-w,a-s -C $$BOOK . | \
		(cd $(DESTDIR)$(docdir)/html; tar xp); \
	done
	install -m755 autobuild/daps-autobuild $(DESTDIR)$(bindir)
	install -m644 autobuild/daps-autobuild.rnc $(DESTDIR)$(datadir)/xml/$(PACKAGE)/schema/
	install -m644 autobuild/daps-autobuild.xml $(DESTDIR)$(templatedir)
if CATALOG_EDIT
# remove old DAPS entries in root catalog and create new entry
	$(XMLLINT) --nocatalogs --format $(root_catalog) | \
	    awk "/<\/group>/ && s == 1 {s=0;next} s == 1 {next} \
	      /<group id=\"$(PACKAGE)\">/{s=1;next} {print}" | \
	      sed '/<\/catalog>/d' >$(TMP_CATALOG)
	$(XMLLINT) --nocatalogs --format $(DAPS_CATALOG) | \
	  awk '/<\/catalog>/{next} s == 1 {print} /<catalog/{s=1} \
	    END{print "</catalog>"}' >>$(TMP_CATALOG)
	chmod --reference=$(root_catalog) $(TMP_CATALOG)
	mv $(TMP_CATALOG) $(root_catalog)
endif


#---------------------------Local UNINSTALL-----------------------------------
if CATALOG_EDIT
uninstall-local: TMP_CATALOG := $(shell mktemp -q $(BUILD_ROOT)/catalog.XXXXX)
uninstall-local:
	$(XMLLINT) --nocatalogs --format $(root_catalog) | \
	  awk "/<\/group>/ && s == 1 {s=0;next} s == 1 {next} /<group id=\"$(PACKAGE)\">/{s=1;next} {print}" > $(TMP_CATALOG)
	chmod --reference=$(root_catalog) $(TMP_CATALOG)
	mv $(TMP_CATALOG) $(root_catalog)
endif
#-----------------------------CLEAN--------------------------------------------

clean-local:
	rm -rf build/ man/build/ doc/build/ $(DAPS_CATALOG_DIR)
	(cd autobuild && ln -sf daps-autobuild.in daps-autobuild)
	(cd bin && (ln -sf daps.in daps; ln -sf daps-xmlformat.in daps-xmlformat))
	(cd bin && ln -sf daps-xmlformat.in daps-xmlformat)
	(cd etc && ln -sf config.in config)
	(cd etc/fop && ln -sf fop-daps.suse $(notdir $(FOP_CONFIG)))
	(cd libexec && ln -sf $(notdir $(JING_WRAPPER_DEFAULT)) $(notdir $(JING_WRAPPER)))
	(cd doc/xml && ln -sf entity-decl.ent.in entity-decl.ent)

#-----------------------------DAPS--------------------------------------------

#
# Use the local catalogs (etc/catalog.generic, etc/catalog.debian) to generate
# system catalogs

$(DAPS_CATALOG): DAPS_PROFDIR := $(pkgdatadir)/daps-xslt/profiling
$(DAPS_CATALOG): $(DAPS_CATALOG_TEMPLATE) $(BUILD_ROOT) $(DAPS_CATALOG_DIR)
	sed 's_\(xml:base\)="[^"]*"_\1="file:///usr/share/daps/daps-xslt/"_g' $< > $@


# the sources contain links bin/daps, etc/config and $(FOP_CONFIG)
# These need to be replaced by real files/different links created by
# the respective targets below.
# To make sure they are rebuild at least once when make is called for
# the first time, we make them depend on a file we create first
# This file will be newer than the existing links and thus the targets
# will be rebuild.
# This helps to avoid PHONY targets which would be called with every single
# make call (even make clean) - something we definetely would like to avoid

$(FIRSTBUILD): $(BUILD_ROOT)
	touch $@

# see http://www.gnu.org/software/autoconf/manual/autoconf.html#Installation-Directory-Variables
bin/daps bin/daps-xmlformat: $(FIRSTBUILD)
	if [ -L $@ ]; then rm -f $@; fi
	$(REPL_PATH) $@.in > $@
	chmod +x $@

etc/config: $(FIRSTBUILD)
	if [ -L $@ ]; then rm -f $@; fi
	$(REPL_PATH) $@.in > $@

autobuild/daps-autobuild: $(FIRSTBUILD)
	if [ -L $@ ]; then rm -f $@; fi
	$(REPL_PATH) $@.in > $@
	chmod +x $@

# Create the FOP config file. RedHat and SUSE require a special version
# (see FOP_CONFIG_SRC definitions above)
$(FOP_CONFIG): $(FOP_CONFIG_SRC) $(FOP_CONFIG_DEFAULT) $(FIRSTBUILD)
	if test -n "$(FOP_CONFIG_SRC)"; then \
	  ln -sf $(notdir $(FOP_CONFIG_SRC)) $@; \
	else \
	  ln -sf $(notdir $(FOP_CONFIG_DEFAULT)) $@; \
	fi


$(SAXON_CONFIG): $(SAXON_CONFIG_SRC) $(FIRSTBUILD)


# Create the Jing Wrapper. Debian and Ubuntu require a special version
# (see JING_WRAPPER definitions above)
$(JING_WRAPPER): $(JING_WRAPPER_SRC) $(JING_WRAPPER_DEFAULT) $(FIRSTBUILD)
	if test -n "$(JING_WRAPPER_SRC)"; then \
	  cp --remove-destination $(JING_WRAPPER_SRC) $@; \
	else \
	  cp --remove-destination $(JING_WRAPPER_DEFAULT) $@; \
	fi

$(USERGUIDE):
	+$(Q)bin/daps $(DEBUG) --dapsroot=$(DAPSROOT) \
	    --styleroot=$(STYLEROOT) --docconfig=$(DC_USERGUIDE) html \
	    --single --name=$(USERGUIDE_NAME)
	+$(Q)$(srcdir)/bin/ccecho "result" "Created $@"

$(QUICKSTART):
	+$(Q)bin/daps $(DEBUG) --dapsroot=$(DAPSROOT)  \
	    --styleroot=$(STYLEROOT) --docconfig=$(DC_QUICKSTART) html \
	    --single --name=$(QUICKSTART_NAME)
	+$(Q)$(srcdir)/bin/ccecho "result" "Created $@"

$(ADOCGUIDE):
	+$(Q)bin/daps $(DEBUG) --dapsroot=$(DAPSROOT)  \
            --schema "http://docbook.org/xml/5.0/rng/docbookxi.rng" \
	    --styleroot=$(STYLEROOT) --docconfig=$(DC_ADOCGUIDE) html \
	    --single --name=$(ADOCGUIDE_NAME)
	+$(Q)$(srcdir)/bin/ccecho "result" "Created $@"

# Generate man pages on the fly
$(dist_man1_MANS):
	+$(Q)bin/daps $(DEBUG) --dapsroot=$(DAPSROOT) --color=0 \
	  --docconfig=$(DAPSROOT)/man/$(DC_MANPAGES) man --nogzip
	+$(Q)$(srcdir)/bin/ccecho "result" "Created man pages $@"

$(INSTALLDIRS) $(BUILD_ROOT) $(DAPS_CATALOG_DIR):
	test -z "$@" || $(MKDIR_P) $@

.PHONY: debian ubuntu redhat

debian ubuntu:
	(cd etc/fop && ln -sf fop-daps.generic fop-daps.xml)
	(cd libexec && ln -sf daps-jing.debian daps-jing)
	(cd etc     && ln -sf catalog.debian catalog.xml)

redhat:
	(cd etc/fop && ln -sf fop-daps.redhat fop-daps.xml)
