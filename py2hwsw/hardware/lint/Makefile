# SPDX-FileCopyrightText: 2025 IObundle
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

VSRC+=$(wildcard ../src/*.v)

ifneq ($(BOARD_DIR),)
INCLUDE_DIRS+=../../$(BOARD_DIR)
VSRC+=$(wildcard ../../$(BOARD_DIR)/*.v)
INCLUDE_DIRS+=../fpga/src
VSRC+=$(wildcard ../fpga/src/*.v)
else
INCLUDE_DIRS+=../simulation/src
VSRC+=$(wildcard ../simulation/src/*.v)
endif

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
