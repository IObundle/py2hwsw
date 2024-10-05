# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

run-lint:
	verilator --lint-only -Wall --timing -I. -I../src -I../simulation/src $(VSRC)

clean-lint:

