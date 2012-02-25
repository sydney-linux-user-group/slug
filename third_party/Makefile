#!/bin/bash

all: .updated
clean: git_clean

###############################################################################
# third_party modules are managed by git
###############################################################################

.updated: ../.gitmodules
	@cd ..; echo "Updating git submodules." ;\
		git submodule init; \
		git submodule update
	touch -r ../.gitmodules .updated

.PHONY : all clean git
