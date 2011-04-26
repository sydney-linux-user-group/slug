
lint:
	# R0904 - Disable "Too many public methods" warning
	# W0221 - Disable "Arguments differ from parent", as get and post will.
	python -c "import config; config.lint_setup(); import sys; from pylint import lint; lint.Run(sys.argv[1:])" \
		--reports=n \
		--include-ids=y \
		--no-docstring-rgx "(__.*__)|(get)|(post)|(main)" \
		--disable-msg=W0221 \
		--disable-msg=R0904 \
		--const-rgx='[a-z_][a-z0-9_]{2,30}$$' *.py

3p: third_party.zip

third-party: third_party.zip

third_party.zip: init_third_party.sh third_party/mkzip
	./init_third_party.sh

upload: update

deply: update

update: third_party.zip
	appcfg.py update .

serve: third_party.zip
	python2.6 $(which dev_appserver.py) .
