
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
