# Copyright (C) 2012-2020 SUSE Software Solutions Germany GmbH
#
# Author:
# Frank Sundermeyer <fsundermeyer at opensuse dot org>
#
# Stuff for DAPS that did not fit anywhere else
#
# Please submit feedback or patches to
# <fsundermeyer at opensuse dot org>
#


#--------------
# Bigfile
#

BIGFILE := $(TMP_DIR)/$(DOCNAME)_bigfile.xml

#
# JING_FLAGS is set in validate.mk
#

.PHONY: bigfile
bigfile: $(BIGFILE)
  ifeq "$(NOVALID)" "1"
    ifeq "$(DOCBOOK_VERSION)" "4"
	xmllint --noent --postvalid --noout --xinclude $< && \
	  ccecho "result" "Successfully validated the bigfile at:\n$<" || \
	  ccecho "error" "Validation failed for the bigfile at:\n$<"
    else
	$(JING_WRAPPER) $(JING_FLAGS) $(DOCBOOK5_RNG) $< && \
	  ccecho "result" "Successfully validated the bigfile at:\n$<" || \
	  ccecho "error" "Validation failed for the bigfile at:\n$<"
    endif
  else
	@ccecho "result" "Find the bigfile at:\n$<"
  endif

# Creates one big XML file from a profiled MAIN by following the xincludes
# considering the rootid. If no rootid is given, a bigfile for the whole set
# is created
# If --novalid is set, the XML sources are not checked for validness
# If xref's to non existing locations are found, they are resolved to text
# links
#

$(BIGFILE): | $(TMP_DIR)
ifneq "$(NOVALID)" "1"
  $(BIGFILE): $(PROFILEDIR)/.validate
endif
$(BIGFILE): $(PROFILES)
  ifeq "$(VERBOSITY)" "2"
	@echo "   Creating bigfile"
  endif
	$(XSLTPROC) --xinclude --output $(BIGFILE) $(ROOTSTRING) \
	  --stylesheet $(STYLEBIGFILE) --file $(PROFILED_MAIN) \
	  $(XSLTPROCESSOR) $(ERR_DEVNULL)

#--------------
# linkcheck
#
STYLELINKS := $(DAPSROOT)/daps-xslt/common/get-links.xsl
TESTPAGE   := $(TMP_DIR)/$(DOCNAME)-links.html

ifeq "$(VERBOSITY)" "2"
  CB_VERBOSITY := --verbose
endif

.PHONY: linkcheck
linkcheck: | $(TMP_DIR)
linkcheck: $(PROFILEDIR)/.validate 
linkcheck:
  ifeq "$(VERBOSITY)" "2"
	@echo "   Running linkchecker"
  endif
	$(XSLTPROC) --xinclude $(ROOTSTRING) -o $(TESTPAGE) \
	  --stylesheet $(STYLELINKS) --file $(PROFILED_MAIN) $(XSLTPROCESSOR) \
	  $(ERR_DEVNULL)
	checkbot --url file://localhost$(TESTPAGE) $(CB_VERBOSITY) \
	  $(CB_OPTIONS) --file $(TMP_DIR)/$(BOOK)-checkbot.html $(DEVNULL)
  ifeq "$(SHOW)" "1"
    ifdef BROWSER
	$$BROWSER $(TMP_DIR)/$(BOOK)-checkbot-localhost.html &
    else
	xdg-open $(TMP_DIR)/$(BOOK)-checkbot-localhost.html &
    endif
  endif
	@ccecho "result" "Find the linkcheck report at:\n$(TMP_DIR)/$(BOOK)-checkbot-localhost.html"

#--------------
# Style checker
#

STYLECHECK_OUTFILE := $(TMP_DIR)/$(DOCNAME)-stylecheck.xml

.PHONY: stylecheck
stylecheck: $(BIGFILE)
  ifeq "$(SHOW)" "1"
	@sdsc --show $(BIGFILE) $(STYLECHECK_OUTFILE)
  else
	@sdsc $(BIGFILE) $(STYLECHECK_OUTFILE) >/dev/null
  endif
	@ccecho "result" "Find the stylecheck report at:\n$(STYLECHECK_OUTFILE)"

#--------------
# Productname/Productversion
#

.PHONY: productinfo
ifeq "$(DOCBOOK_VERSION)" "5"
  productinfo: NAMESPACE := -N db5="http://docbook.org/ns/docbook"
  productinfo: ELEM_PREFIX := db5:
  productinfo: ATTR_PREFIX := xml:
endif
productinfo: $(BIGFILE)
  ifdef ROOTID
	@echo -n "PRODUCTNAME=\"$(shell $(XMLSTARLET) sel $(NAMESPACE) -t -v "//*[@$(ATTR_PREFIX)id='$(ROOTID)']/*/$(ELEM_PREFIX)productname" $< 2>/dev/null)\" "
	@echo -n "PRODUCTNUMBER=\"$(shell $(XMLSTARLET) sel $(NAMESPACE) -t -v "//*[@$(ATTR_PREFIX)id='$(ROOTID)']/*/$(ELEM_PREFIX)productnumber" $< 2>/dev/null)\""
  else
	@echo -n "PRODUCTNAME=\"$(shell $(XMLSTARLET) sel $(NAMESPACE) -t -v "(/*/*/$(ELEM_PREFIX)productname)[1]" $< 2>/dev/null)\" "
	@echo -n "PRODUCTNUMBER=\"$(shell $(XMLSTARLET) sel $(NAMESPACE) -t -v "(/*/*/$(ELEM_PREFIX)productnumber)[1]" $< 2>/dev/null)\""
  endif

#---------------
# Docinfo
#
STYLEDOCINFO := $(DAPSROOT)/daps-xslt/common/docinfo.xsl

# make sure to rebuils always
#
.PHONY: docinfo
docinfo: $(BIGFILE)
	$(XSLTPROC) --stylesheet $(STYLEDOCINFO) --file $< \
	  $(XSLTPROCESSOR) $(ERR_DEVNULL)


#---------------
# Metadata
#
# requires filelist.mk because of a setting for FILE4ID


METAFILE = $(PROFILEDIR)/$(notdir $(FILE4ID))
ifeq "$(ROOTID)" ""
  _ROOTID = $(shell $(XMLSTARLET) sel -N d=http://docbook.org/ns/docbook -T -t -v "/d:*/@xml:id" $(METAFILE))
else
  _ROOTID = $(ROOTID)
endif

.PHONY: metadata
metadata: $(PROFILES) $(DOCFILES) validate
ifneq "$(METADATA_OUTPUT)" ""
	@$(XSLTPROC) --stylesheet $(META_STYLE) --file $(METAFILE) $(XSLTPROCESSOR) 2>/dev/null > $(METADATA_OUTPUT)
	@echo -e "rootid=$(_ROOTID)" >> $(METADATA_OUTPUT)
	@echo "Find the metadata at $(METADATA_OUTPUT)"
else
	@$(XSLTPROC) --stylesheet $(META_STYLE) --file $(METAFILE) $(XSLTPROCESSOR) 2>/dev/null
	@echo -e "rootid=$(_ROOTID)"
endif

