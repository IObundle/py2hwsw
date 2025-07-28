# Add iob_soc_opencryptolinux software as a build dependency
HEX+=iob_soc_opencryptolinux_boot.hex iob_soc_opencryptolinux_firmware.hex
HEX+=boot_flow

ROOT_DIR :=../..
include $(ROOT_DIR)/software/sw_build.mk

VTOP:=iob_soc_opencryptolinux_tb

# SOURCES
ifeq ($(SIMULATOR),verilator)

VSRC+=./src/iob_tasks.cpp

ifeq ($(USE_ETHERNET),1)
VSRC+=./src/iob_eth_swreg_emb_verilator.c ./src/iob_eth_driver_tb.cpp
endif

# verilator top module
VTOP:=iob_soc_opencryptolinux_sim_wrapper

VSRC_TMP:=$(filter-out ./src/N25Qxxx.v,$(VSRC))
VSRC=$(VSRC_TMP)
endif

CONSOLE_CMD ?=../../scripts/console.py -L

GRAB_TIMEOUT ?= 7200

TEST_LIST+=test1
test1:
	make -C ../../ fw-clean SIMULATOR=$(SIMULATOR) && make -C ../../ sim-clean SIMULATOR=$(SIMULATOR) && make run SIMULATOR=$(SIMULATOR)

.PHONY: boot_flow
