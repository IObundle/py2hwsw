# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

SHELL:=bash

include ../../config_build.mk

REMOTE_BUILD_DIR=$(USER)/$(BUILD_DIR_NAME)
REMOTE_LINT_DIR=$(REMOTE_BUILD_DIR)/hardware/lint

LINTER ?=verilator
LINT_TOP=$(NAME)

INCLUDE_DIRS+=.
INCLUDE_DIRS+=../src

VSRC+=$(wildcard ../src/*.v)

#include local lint segment
ifneq ($(wildcard lint_build.mk),)
include lint_build.mk
endif

$(NAME)_files.list: $(VSRC)

$(VSRC):
	@ls $@ >> $(NAME)_files.list

RSYNC_ROOT_DIR=../..
include $(LINTER).mk

run: clean $(NAME)_files.list
	make run-lint LINTER=$(LINTER)

clean:
	make clean-lint LINTER=$(LINTER)

.PHONY: run $(VSRC) clean
