###############################################################################
## Helpful Definitions
###############################################################################
define \n


endef

ACTIVATE = . bin/activate
DJANGO = DJANGO_SETTINGS_MODULE=usergroup.settings

###############################################################################
# Export the configuration to sub-makes
###############################################################################
export

all: test README.rst

virtualenv: bin/activate
lib: bin/activate

distclean: virtualenv-clean clean

virtualenv-clean:
	rm -rf bin include lib lib64 share src

clean:
	find . \( -name \*\.pyc \) -delete
	git clean -f -d

bin/activate:
	virtualenv --no-site-packages .
	-rm distribute*.tar.gz

freeze:
	$(ACTIVATE) && pip freeze > requirements.txt

lib/python2.6/site-packages/distribute-0.6.25-py2.6.egg-info: lib
	$(ACTIVATE) && pip install -U distribute

lib/python2.6/site-packages/ez_setup.py: lib
	$(ACTIVATE) && pip install ez_setup

third_party:
	cd third_party && make

src/pip-delete-this-directory.txt: requirements.txt
	$(ACTIVATE) && pip install -r requirements.txt
	touch -r requirements.txt src/pip-delete-this-directory.txt

install: lib/python2.6/site-packages/ez_setup.py lib/python2.6/site-packages/distribute-0.6.25-py2.6.egg-info third_party src/pip-delete-this-directory.txt README.rst

prepare-serve: install
	$(ACTIVATE) && python manage.py collectstatic --noinput
	$(ACTIVATE) && python manage.py syncdb

test: clitest firefoxtest

clitest: install
	$(ACTIVATE) && python manage.py test -v2 usergroup.django_tests

firefoxtest: install
	$(ACTIVATE) && TEST_DISPLAY=1 python manage.py test -v 2 usergroup.selenium_tests

chrometest: install
	$(ACTIVATE) && TEST_DRIVER="chrome" TEST_DISPLAY=1 python manage.py test -v 2 usergroup.selenium_tests

lint: install
	@# R0904 - Disable "Too many public methods" warning
	@# W0221 - Disable "Arguments differ from parent", as get and post will.
	@# E1103 - Disable "Instance of 'x' has no 'y' member (but some types could not be inferred)"
	@# I0011 - Disable "Locally disabling 'xxxx'"
	@$(ACTIVATE) && $(DJANGO) python \
		-W "ignore:disable-msg is:DeprecationWarning:pylint.lint" \
		-c "import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
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

config:
	$(ACTIVATE) && git-cl config file://$$PWD/.codereview.settings

upload:
	$(ACTIVATE) && git-cl upload

serve: prepare-serve install
	$(ACTIVATE) && python manage.py runserver

edit:
	$(EDITOR) *.py templates/*.html static/css/*.css

private:
	rm -rf private
	git clone git+ssh://git@github.com/mithro/slug-private.git private

doc: README.rst
	$(ACTIVATE) && cd doc && $(MAKE) html

README.rst: doc/README.rst
	cp $^ $@

.PHONY : lint upload deploy serve clean config edit private prepare-serve third_party doc
