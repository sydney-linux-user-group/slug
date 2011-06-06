define \n


endef

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
ifeq "$(shell echo -n 'Found' | md5sum 2>/dev/null)" "5d695cc28c6a7ea955162fbdd0ae42b9  -"
MD5SUM=md5sum
else
#Maybe we're on a mac
ifeq "$(shell md5 -q -s Found 2>/dev/null)" "5d695cc28c6a7ea955162fbdd0ae42b9" #md5sum of Found
MD5SUM=md5 -r
else
$(error "${\n}Please install md5sum${\n}On Ubuntu/Debian run:${\n}    sudo apt-get install md5sum${\n}")
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
PYLINT=$(shell python -c "import pylint; print 'ok'" 2>/dev/null)
ifeq ($(strip $(PYLINT)),)
$(error "${\n}Please install pylint${\n} On Ubuntu/Debian run:${\n} sudo apt-get install pylint${\n}")
endif

# Newer versions of pylint uses --disable rather then --disable-msg
PYLINT_NEW=$(shell python -c "from pylint import lint; import sys; print cmp(tuple(int(x) for x in lint.version.split('.')), (0,20,0))" 2>/dev/null)

ifeq "${PYLINT_NEW}" "1"
PYLINT_DISABLE="--disable"
else
PYLINT_DISABLE="--disable-msg"
endif

lint: third_party.zip
	@# R0904 - Disable "Too many public methods" warning
	@# W0221 - Disable "Arguments differ from parent", as get and post will.
	@# E1103 - Disable "Instance of 'x' has no 'y' member (but some types could not be inferred)"
	@python \
		-W "ignore:disable-msg is:DeprecationWarning:pylint.lint" \
		-c "import config; config.lint_setup(); import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
		--reports=n \
		--include-ids=y \
		--no-docstring-rgx "(__.*__)|(get)|(post)|(main)" \
		--indent-string='    ' \
		${PYLINT_DISABLE}=W0221 \
		${PYLINT_DISABLE}=R0904 \
		${PYLINT_DISABLE}=E1103 \
		--const-rgx='[a-z_][a-z0-9_]{2,30}$$' *.py

###############################################################################
# Third Party Zip file creation
##############################################################################
FINDARGS=-type f -name \*.py -exec  echo "	{} \\" \;
TP=cd third_party;
TPT=third_party.zip.d.tmp

third_party:
	make -C third_party

third_party.zip.d: third_party third_party.paths
	@echo "Generating a third_party.zip dependency file."
	@echo "THIRD_PARTY_files=\\" >> $(TPT)
	@cd third_party; \
	 cat ../third_party.paths | grep ^third_party.zip | sed -e's-third_party.zip/--' | (while read LINE; do \
		PREFIX=$${LINE%% *}; \
		for SUFFIX in $${LINE#* }; do \
			find $$PREFIX/$$SUFFIX $(FINDARGS) >> ../$(TPT); \
		done; \
	 done)
	@echo '' >> $(TPT)
	@echo 'THIRD_PARTY_here=$$(addprefix third_party/,$$(THIRD_PARTY_files)) ' >> $(TPT)
	@echo '' >> $(TPT)
	@echo 'third_party.zip: third_party.zip.d $$(THIRD_PARTY_here)' >> $(TPT)
	@echo '	@echo Changed files: $$?' >> $(TPT)
	@echo '	@cd third_party; rm ../third_party.zip; zip -r ../third_party.zip $$(THIRD_PARTY_files)' >> $(TPT)
	@if [ ! -e $@ ]; then touch $@; fi
	@if [ `${MD5SUM} $@ | sed -e's/ .*//'` != `${MD5SUM} $(TPT) | sed -e's/ .*//'` ]; then \
		echo "third_party.zip.d has changed!"; \
		mv $(TPT) $@; \
	else \
		echo "third_party.zip.d has not changed!"; \
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
	${APPENGINE_SDK}/dev_appserver.py -a 0.0.0.0 -d --enable_sendmail .

clean:
	$(MAKE) -C third_party clean
	git clean -f -d

.PHONY : lint third_party upload deploy serve clean
