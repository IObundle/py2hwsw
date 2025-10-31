# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

VFLAGS+=$(addprefix -I,$(INCLUDE_DIRS))

WAIVER_FILE ?= $(wildcard verilator_waiver.vlt)

run-lint:
	verilator --lint-only -Wall --timing $(VFLAGS) verilator_config.vlt $(WAIVER_FILE) $(VSRC)

clean-lint:

