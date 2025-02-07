# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

include auto_sim_build.mk

# Add iob-system software as a build dependency
HEX+=iob_system_bootrom.hex iob_system_firmware.hex

ROOT_DIR :=../..
include $(ROOT_DIR)/software/sw_build.mk

VTOP:=iob_system_tb

# VERILATOR ADDITIONAL SOURCES #####################################
ifeq ($(SIMULATOR),verilator)

# uart control header
VHDR+=../../software/src/iob_uart_csrs.h

# verilator top module
VTOP:=iob_system_sim

endif
####################################################################

CONSOLE_CMD ?=rm -f soc2cnsl cnsl2soc; ../../scripts/console.py -L

GRAB_TIMEOUT ?= 3600
