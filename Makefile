
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

ifeq "${PYLINT_VERSION}" "0.22.0"
PYLINT_DISABLE="--disable-msg"
else
PYLINT_DISABLE="--disable"
endif
###############################################################################
###############################################################################

lint:
	@# R0904 - Disable "Too many public methods" warning
	@# W0221 - Disable "Arguments differ from parent", as get and post will.
	@python -c "import config; config.lint_setup(); import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
		--reports=n \
		--include-ids=y \
		--no-docstring-rgx "(__.*__)|(get)|(post)|(main)" \
		--indent-string='    ' \
		${PYLINT_DISABLE}=W0221 \
		${PYLINT_DISABLE}=R0904 \
		--const-rgx='[a-z_][a-z0-9_]{2,30}$$' *.py

3p: third_party.zip

third-party: third_party.zip

third_party.zip: init_third_party.sh third_party/mkzip
	./init_third_party.sh

upload: update
deploy: update
update: third_party.zip
	${APPENGINE_SDK}/appcfg.py update .

serve: third_party.zip
	${APPENGINE_SDK}/dev_appserver.py .

.PHONY = lint sdk serve deploy
