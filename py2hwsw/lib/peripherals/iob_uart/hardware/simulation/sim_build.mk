# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
# This file is included in BUILD_DIR/sim/Makefile
#

NOCLEAN+=-o -name "uart_tb.v"

# VERILATOR ADDITIONAL SOURCES #####################################
ifeq ($(SIMULATOR),verilator)

VSRC+=./src/iob_tasks.cpp ./src/iob_uart_csrs_emb_verilator.c ./src/iob_uart_core_tb.c

VHDR+=src/iob_uart_csrs.h

src/iob_uart_csrs.h:
	cp src/iob_uart_csrs_verilator.h src/iob_uart_csrs.h

#COBJ=
#$(COBJ): src/iob_uart_core_tb.c src/iob_uart_csrs.h
#	gcc -I../../ -I../../software/src -I./src/ -c -o $@ $<

endif
####################################################################
