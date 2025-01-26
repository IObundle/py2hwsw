# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

SHELL:=bash

include ../../config_build.mk

LINTER ?=verilator

REMOTE_BUILD_DIR=$(USER)/$(BUILD_DIR_NAME)
REMOTE_LINT_DIR=$(REMOTE_BUILD_DIR)/hardware/lint

LINT_TOP=$(NAME)

INCLUDE_DIRS+=.
INCLUDE_DIRS+=../src
INCLUDE_DIRS+=../simulation/src

VSRC=$(wildcard ../src/*.v)
VSRC=$(wildcard ../simulation/src/*.v)

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
