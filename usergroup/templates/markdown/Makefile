
THIRD_PARTY=../../third_party
MARKDOWN=$(shell ls -d $(THIRD_PARTY)/Markdown-*/)
MARKDOWN_EXT=$(shell grep extensions ../../editevent.py | head -1 | sed -e"s/extensions = //" -e"s/[',\[\]]*//g")

%: %.md | $(THIRD_PARTY)
	@make -C $(THIRD_PARTY) -s
	@echo
	@echo
	@echo "Enabled markdown extensions"
	@echo "   " $(MARKDOWN_EXT)
	@echo
	@echo
	@echo "- $@ ----------------------------------------"
	@PYTHONPATH=$$PYTHONPATH:$(MARKDOWN) \
		$(MARKDOWN)/bin/markdown --noisy \
			$(addprefix -x, $(MARKDOWN_EXT)) \
		$<
	@echo
	@echo "---------------------------------------------"
