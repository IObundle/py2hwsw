# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

ifeq ($(SIMULATOR),verilator)
VSRC+=./src/iob_uart_csrs.c
endif

