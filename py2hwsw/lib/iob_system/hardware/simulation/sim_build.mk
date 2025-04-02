# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

include auto_sim_build.mk

# Add iob-system software as a build dependency
HEX+=iob_system_bootrom.hex iob_system_firmware.hex

ROOT_DIR :=../..
include $(ROOT_DIR)/software/sw_build.mk

ifeq ($(USE_ETHERNET),1)
VSRC+=./src/iob_eth_csrs_emb_verilator.c ./src/iob_eth_driver_tb.cpp
endif

CSRS = ../../software/src/iob_uart_csrs.c

#replace iob_system_sim with iob_uut
VSRC:= $(subst iob_system_sim,iob_uut,$(VSRC))
./src/iob_uut.v: ./src/iob_system_sim.v
	mv ./src/iob_system_sim_conf.vh ./src/iob_uut_conf.vh
	mv $< $@ && sed -i 's/iob_system_sim/iob_uut/g' $@

CONSOLE_CMD ?=rm -f soc2cnsl cnsl2soc; ../../scripts/console.py -L

GRAB_TIMEOUT ?= 3600
