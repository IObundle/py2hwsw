# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT
include ../../config_build.mk

LATEX_DIR = ./latex
INPUT_PATH = ../../software/src

DOXYGEN_NAME=$(NAME)
# get VX.YZ from BUILD_DIR_NAME=CORE_VX.YZ format
DOXYGEN_VERSION=$(shell echo $(BUILD_DIR_NAME) | sed 's/^.*_\([^_]*\)$$/\1/')
# only include documentation from files with @file Doxygen tag
DOXYGEN_INPUT = $(shell grep -rl "@file" ${INPUT_PATH})

REFMAN_TEX ?= $(LATEX_DIR)/refman.tex

all: clean $(REFMAN_TEX)

$(REFMAN_TEX):
	export DOXYGEN_NAME="$(DOXYGEN_NAME)";\
	export DOXYGEN_VERSION="$(DOXYGEN_VERSION)";\
	export DOXYGEN_INPUT="$(DOXYGEN_INPUT)";\
		doxygen Doxyfile

list-doxygen-file-docs: $(REFMAN_TEX)
	@sed -n '/^\\chapter{File Documentation}/,/^%--- End generated contents ---/p' $(REFMAN_TEX) | grep input

clean:
	rm -rf $(LATEX_DIR)

.PHONY: all clean list-doxygen-file-docs
