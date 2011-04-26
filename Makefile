
###############################################################################
## Trying to find the AppEngine SDK
###############################################################################
ifndef APPENGINE_SDK
# ../google_appengine
ifeq "$(shell [ -x ../google_appengine ] && echo -n 'Found')" "Found"
APPENGINE_SDK=../google_appengine
else

# which dev_appserver.py
APPENGINE_SDK=$(dir $(shell which dev_appserver.py))
ifeq ($(strip $(APPENGINE_SDK)),)

# which dev_appserver
APPENGINE_SDK=$(dir $(shell which dev_appserver))
ifeq ($(strip $(APPENGINE_SDK)),)

# FIXME: Put the next location to search here.

endif # which dev_appserver
endif # which dev_appserver.py
endif # ../google_appengine
endif # ndef APPENGINE_SDK

ifeq "$(shell [ -x ${APPENGINE_SDK} ] && echo -n 'Found')" "Found"
$(info Found AppEngine SDK at ${APPENGINE_SDK})
else
$(error Could not find AppEngine SDK, please set $$APPENGINE_SDK)
endif

export
###############################################################################
###############################################################################

###############################################################################
## Look at pylint
###############################################################################
PYLINT=$(shell which pylint)
ifeq ($(strip $(PYLINT)),)
$(error "Please install pylint\nOn Ubuntu/Debian run:\n    sudo apt-get install pylint\n")
endif
PYLINT_VERSION=$(shell pylint --version | head -1 | sed -e's/pylint //' -e's/,//')

# Newer versions of pylint uses --disable rather then --disable-msg
PYLINT_NEW=$(shell python -c "from pylint import lint; import sys; print cmp(tuple(int(x) for x in lint.version.split('.')), (0,20,0))")

ifeq "${PYLINT_NEW}" "1"
PYLINT_DISABLE="--disable"
else
PYLINT_DISABLE="--disable-msg"
endif

lint:
	@# R0904 - Disable "Too many public methods" warning
	@# W0221 - Disable "Arguments differ from parent", as get and post will.
	@python \
		-W "ignore:disable-msg is:DeprecationWarning:pylint.lint" \
		-c "import config; config.lint_setup(); import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
		--reports=n \
		--include-ids=y \
		--no-docstring-rgx "(__.*__)|(get)|(post)|(main)" \
		--indent-string='    ' \
		${PYLINT_DISABLE}=W0221 \
		${PYLINT_DISABLE}=R0904 \
		--const-rgx='[a-z_][a-z0-9_]{2,30}$$' *.py

###############################################################################
# Third Party Zip file creation
###############################################################################
FILES=-type f -name \*.py
THIRD_PARTY=$(shell cd third_party; find python-dateutil-*/dateutil $(FILES))\
	python-datetime-tz/datetime_tz.py \
	python-datetime-tz/pytz_abbr.py \
	$(shell cd third_party; find Markdown-*/markdown $(FILES)) \
	$(shell cd third_party; find vobject/vobject/ $(FILES)) \
	PyRSS2Gen-*/PyRSS2Gen.py

THIRD_PARTY_here=$(addprefix third_party/, $(THIRD_PARTY))

$(THIRD_PARTY_here):
	$(MAKE) -C third_party

third_party.zip: $(THIRD_PARTY_here)
	cd third_party; \
	zip -r ../third_party.zip \
		$(THIRD_PARTY)

###############################################################################
###############################################################################

upload: update
deploy: update
update: third_party.zip
	${APPENGINE_SDK}/appcfg.py update .

serve: third_party.zip
	python2.6 ${APPENGINE_SDK}/dev_appserver.py .

clean:
	$(MAKE) -C third_party clean
	git clean -f -d

.PHONY = lint upload deploy serve clean
