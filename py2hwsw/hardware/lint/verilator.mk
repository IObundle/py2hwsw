# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

VFLAGS+=$(addprefix -I,$(INCLUDE_DIRS))

run-lint:
	verilator --lint-only -Wall --timing $(VFLAGS) verilator_config.vlt $(VSRC)

clean-lint:

