###############################################################################
## Helpful Definitions
###############################################################################
define \n


endef

ACTIVATE = . bin/activate

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

all: test

virtualenv: bin/activate

distclean: virtualenv-clean clean

virtualenv-clean:
	rm -rf bin include lib lib64 share

clean:
	find . \( -name \*\.pyc -o -name \*\.dot -o -name \*\.svg -o -name \*\.png \) -delete
	git clean -f -d

bin/activate:
	virtualenv --no-site-packages .

freeze:
	$(ACTIVATE) && pip freeze -E . > requirements.txt

lib: bin/activate
	$(ACTIVATE) && pip install ez_setup
	$(ACTIVATE) && pip install -E . -r requirements.txt

third_party/jquery-openid:
	git submodule init

install: lib third_party/jquery-openid
	git submodule update

test: install
	$(ACTIVATE) && unit2 discover -t ./ tests/

lint: install
	@# R0904 - Disable "Too many public methods" warning
	@# W0221 - Disable "Arguments differ from parent", as get and post will.
	@# E1103 - Disable "Instance of 'x' has no 'y' member (but some types could not be inferred)"
	@# I0011 - Disable "Locally disabling 'xxxx'"
	@$(ACTIVATE) && python \
		-W "ignore:disable-msg is:DeprecationWarning:pylint.lint" \
		-c "import config; config.lint_setup(); import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
		--reports=n \
		--include-ids=y \
		--no-docstring-rgx "(__.*__)|(get)|(post)|(main)" \
		--indent-string='    ' \
		--disable=W0221 \
		--disable=R0904 \
		--disable=E1103 \
		--disable=I0011 \
		--const-rgx='[a-z_][a-z0-9_]{2,30}$$' *.py 2>&1 | grep -v 'maximum recursion depth exceeded'

###############################################################################
###############################################################################

serve: install
	$(ACTIVATE) && python manage.py collectstatic --noinput
	$(ACTIVATE) && python manage.py syncdb
	$(ACTIVATE) && python manage.py runserver

edit:
	$(EDITOR) *.py templates/*.html static/css/*.css

.PHONY : lint third_party upload deploy serve clean edit
