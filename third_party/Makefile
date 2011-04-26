#!/bin/bash

TARGETS=dateutil pytz datetime-tz markdown pyrss vobject
TARGETS_CLEAN=$(addsuffix -clean,$(TARGETS))

all: git $(TARGETS)
clean: $(TARGETS_CLEAN)

###############################################################################
# There are some third_party modules managed by git
###############################################################################

git:
	@cd ..; echo "Updating git submodules." ;\
		git submodule init; \
		git submodule update

###############################################################################
# python-dateutil
###############################################################################

DATEUTIL=python-dateutil-1.5

# Download the tar.gz
$(DATEUTIL).tar.gz:
	curl -O http://labix.org/download/python-dateutil/$(DATEUTIL).tar.gz

# Extract the tar.gz
$(DATEUTIL): $(DATEUTIL).tar.gz
	tar -zxvf $^
	@# Update modtime on tar.gz to match directory so we don't continually rebuild
	@touch -m $^ -r $@

# Human name target
dateutil: $(DATEUTIL)

dateutil-clean:
	rm -rf $(DATEUTIL)*

###############################################################################
# pytz optimised for Google AppEngine
###############################################################################
GAEPYTZ=gaepytz-2011c

$(GAEPYTZ).tar.gz:
	curl -O http://pypi.python.org/packages/source/g/gaepytz/$(GAEPYTZ).tar.gz

$(GAEPYTZ): $(GAEPYTZ).tar.gz
	tar -zxvf $^
	rsync -Pa $(GAEPYTZ)/pytz pytz
	@# Update modtime on tar.gz to match directory so we don't continually rebuild
	@touch -m $^ -r $@

pytz: $(GAEPYTZ)

pytz-clean:
	rm -rf $(GAEPYTZ)* pytz

###############################################################################
# python-datetime-tz a datetime library which cares about timezones
###############################################################################

python-datetime-tz:
	svn checkout http://python-datetime-tz.googlecode.com/svn/trunk/ python-datetime-tz

datetime-tz: python-datetime-tz

datetime-tz-clean:
	rm -rf python-datetime-tz

###############################################################################
# Markdown parser
###############################################################################
MARKDOWN=Markdown-2.0.3
MARKDOWN_EXT=$(shell find markdown-extensions -type f -name *.py)

# Download the tar.gz
$(MARKDOWN).tar.gz:
	curl -O http://pypi.python.org/packages/source/M/Markdown/$(MARKDOWN).tar.gz

# Extract the tar.gz
$(MARKDOWN): $(MARKDOWN).tar.gz $(MARKDOWN_EXT)
	tar -zxvf $(MARKDOWN).tar.gz
	@# Update modtime on tar.gz to match directory so we don't continually rebuild
	@touch -m $^ -r $@
	for f in $(MARKDOWN_EXT); do \
		cp $$f $(MARKDOWN)/markdown/extensions/; \
	done

# Human name target
markdown: $(MARKDOWN)

markdown-clean:
	rm -rf $(MARKDOWN)*

###############################################################################
# RSS generator
###############################################################################
PYRSS=PyRSS2Gen-1.0.0

# Download the tar.gz
$(PYRSS).tar.gz:
	curl -O http://www.dalkescientific.com/Python/$(PYRSS).tar.gz

# Extract the tar.gz
$(PYRSS): $(PYRSS).tar.gz
	tar -zxvf $^
	@# Update modtime on tar.gz to match directory so we don't continually rebuild
	@touch -m $^ -r $@

# Human name target
pyrss: $(PYRSS)

pyrss-clean:
	rm -rf $(PYRSS)*

###############################################################################
# vobject a iCal file generator
###############################################################################

vobject:
	svn checkout -r 217 http://svn.osafoundation.org/vobject/trunk/ vobject

vobject-clean:
	rm -rf vobject

###############################################################################
.PHONY=all clean git $(TARGETS) $(TARGETS_CLEAN)
