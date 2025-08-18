# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

include auto_sim_build.mk

# Add iob-system software as a build dependency
BUILD_DEPS+=iob_system_bootrom.hex iob_system_firmware.hex

ROOT_DIR :=../..
include $(ROOT_DIR)/software/sw_build.mk

ifeq ($(USE_ETHERNET),1)
VSRC+=./src/iob_eth_csrs_emb_verilator.c ./src/iob_eth_driver_tb.cpp
endif

VLT_SRC=../../software/simulation/src/iob_uart_csrs.c
CPP_INCLUDES=-I../../../software/simulation/src

CONSOLE_CMD ?=rm -f soc2cnsl cnsl2soc; ../../scripts/console.py -L

GRAB_TIMEOUT ?= 3600

# include simulation build segment of child systems
# child systems can add their own child_sim_build.mk without having to override this one.
ifneq ($(wildcard child_sim_build.mk),)
include child_sim_build.mk
endif
