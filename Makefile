
###############################################################################
## Trying to find the AppEngine SDK
###############################################################################
ifndef APPENGINE_SDK
# ../google_appengine
ifeq "$(shell [ -x ../google_appengine ] && echo -n 'Found')" "Found"
APPENGINE_SDK=../google_appengine
else

# which dev_appserver.py
APPENGINE_SDK=$(dir $(realpath $(shell which dev_appserver.py)))
ifeq ($(strip $(APPENGINE_SDK)),)

# which dev_appserver
APPENGINE_SDK=$(dir $(realpath $(shell which dev_appserver)))
ifeq ($(strip $(APPENGINE_SDK)),)

# FIXME: Put the next location to search here.

endif # which dev_appserver
endif # which dev_appserver.py
endif # ../google_appengine
endif # ndef APPENGINE_SDK

#ifeq "$(shell [ -x ${APPENGINE_SDK} ] && echo -n 'Found')" "Found"
ifndef APPENGINE_SDK
$(error Could not find AppEngine SDK, please set $$APPENGINE_SDK)
else
$(info Found AppEngine SDK at ${APPENGINE_SDK})
endif

###############################################################################
###############################################################################

###############################################################################
## How do we calculate md5s?
###############################################################################

ifndef MD5SUM
ifeq "$(shell md5sum >& /dev/null && echo -n 'Found')" "Found"
MD5SUM=md5sum
else
#Maybe we're on a mac
ifeq "$(shell md5 -q -s Found)" "5d695cc28c6a7ea955162fbdd0ae42b9" #md5sum of Found
MD5SUM=md5 -r
endif # md5
endif #md5sum
endif #ndef MD5SUM

###############################################################################
# Export the configuration to sub-makes
###############################################################################
export

###############################################################################
## Look at pylint
###############################################################################
PYLINT=$(shell which pylint)
ifeq ($(strip $(PYLINT)),)
$(error "Please install pylint\nOn Ubuntu/Debian run:\n    sudo apt-get install pylint\n")
endif
PYLINT_VERSION=$(shell pylint --version 2>/dev/null | head -1 | sed -e's/pylint //' -e's/,//')

# Newer versions of pylint uses --disable rather then --disable-msg
PYLINT_NEW=$(shell python -c "from pylint import lint; import sys; print cmp(tuple(int(x) for x in lint.version.split('.')), (0,20,0))" 2>/dev/null)

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
##############################################################################
FINDARGS=-type f -name \*.py -exec  echo "	{} \\" \;
TP=cd third_party;
TPT=third_party.zip.d.tmp

third_party:
	make -C third_party

third_party.zip.d: third_party
	@echo "Generating a third_party.zip dependency file."
	@echo "THIRD_PARTY_files=\\" >> $(TPT)
	@$(TP) find python-dateutil-*/dateutil $(FINDARGS) >> ../$(TPT)
	@$(TP) find python-datetime-tz/datetime_tz.py $(FINDARGS) >> ../$(TPT)
	@$(TP) find python-datetime-tz/pytz_abbr.py $(FINDARGS) >> ../$(TPT)
	@$(TP) find Markdown-*/markdown $(FINDARGS) >> ../$(TPT)
	@$(TP) find vobject/vobject $(FINDARGS) >> ../$(TPT)
	@$(TP) find PyRSS2Gen-*/PyRSS2Gen.py $(FINDARGS) >> ../$(TPT)
	@echo '' >> $(TPT)
	@echo 'THIRD_PARTY_here=$$(addprefix third_party/,$$(THIRD_PARTY_files)) ' >> $(TPT)
	@echo '' >> $(TPT)
	@echo 'third_party.zip: third_party.zip.d $$(THIRD_PARTY_here)' >> $(TPT)
	@echo '	cd third_party; zip -r ../third_party.zip $$(THIRD_PARTY_files)' >> $(TPT)
	@if [ ! -e $@ ]; then touch $@; fi
	@if [ `${MD5SUM} $@ | sed -e's/ .*//'` != `${MD5SUM} $(TPT) | sed -e's/ .*//'` ]; then \
		echo "third_party.zip.d has changed!"; \
		mv $(TPT) $@; \
	else \
		rm $(TPT); \
	fi


include third_party.zip.d

###############################################################################
###############################################################################

upload: update
deploy: update
update: third_party.zip
	${APPENGINE_SDK}/appcfg.py update .

serve: third_party.zip
	python2.6 ${APPENGINE_SDK}/dev_appserver.py -d .

clean:
	$(MAKE) -C third_party clean
	git clean -f -d

.PHONY : lint third_party upload deploy serve clean
