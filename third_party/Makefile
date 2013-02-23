#!/bin/bash

all: git
clean: git_clean

###############################################################################
# third_party modules are managed by git
###############################################################################

git:
	@cd ..; echo "Updating git submodules." ;\
		git submodule init; \
		git submodule update

git_clean:
	

.PHONY : all clean git git_clean
