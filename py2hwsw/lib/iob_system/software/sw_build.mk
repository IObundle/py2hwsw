# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#########################################
#            Embedded targets           #
#########################################
ROOT_DIR ?=..

include $(ROOT_DIR)/software/auto_sw_build.mk

# Local embedded makefile settings for custom bootloader and firmware targets.

#Function to obtain parameter named $(1) in verilog header file located in $(2)
#Usage: $(call GET_MACRO,<param_name>,<vh_path>)
GET_MACRO = $(shell grep "define $(1)" $(2) | rev | cut -d" " -f1 | rev)

#Function to obtain parameter named $(1) from iob_system_conf.vh
GET_IOB_SYSTEM_CONF_MACRO = $(call GET_MACRO,IOB_SYSTEM_$(1),$(ROOT_DIR)/hardware/src/iob_system_conf.vh)

iob_system_bootrom.hex: ../../software/iob_system_preboot.bin ../../software/iob_system_boot.bin
	../../scripts/makehex.py $^ 00000080 $(call GET_IOB_SYSTEM_CONF_MACRO,BOOTROM_ADDR_W) $@

iob_system_firmware.hex: iob_system_firmware.bin
	../../scripts/makehex.py $< $(call GET_IOB_SYSTEM_CONF_MACRO,MEM_ADDR_W) $@
	../../scripts/makehex.py --split $< $(call GET_IOB_SYSTEM_CONF_MACRO,MEM_ADDR_W) $@

iob_system_firmware.bin: ../../software/iob_system_firmware.bin
	cp $< $@

../../software/%.bin:
	make -C ../../ sw-build

UTARGETS+=build_iob_system_software tb
TB_SRC=./simulation/src/iob_uart_csrs.c
ifneq ($(wildcard ./simulation/src/iob_eth.c),)
TB_SRC+=./simulation/src/iob_eth_tb_driver.c ./simulation/src/iob_eth.c ./simulation/src/iob_eth_csrs.c 
endif

TB_INCLUDES ?=-I./simulation/src

TEMPLATE_LDS=src/$@.lds

IOB_SYSTEM_INCLUDES=-Isrc

IOB_SYSTEM_LFLAGS=-Wl,-L,src,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
IOB_SYSTEM_FW_SRC=src/iob_system_firmware.S
IOB_SYSTEM_FW_SRC+=src/iob_system_firmware.c
IOB_SYSTEM_FW_SRC+=src/iob_printf.c
# PERIPHERAL SOURCES
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
# Only add driver files if they exist
IOB_SYSTEM_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
IOB_SYSTEM_FW_SRC+=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))

# BOOTLOADER SOURCES
IOB_SYSTEM_BOOT_SRC+=src/iob_system_boot.S
IOB_SYSTEM_BOOT_SRC+=src/iob_system_boot.c
IOB_SYSTEM_BOOT_SRC+=src/iob_uart.c
IOB_SYSTEM_BOOT_SRC+=src/iob_uart_csrs.c

# PREBOOT SOURCES
IOB_SYSTEM_PREBOOT_SRC=src/iob_system_preboot.S

build_iob_system_software: iob_system_firmware iob_system_boot iob_system_preboot

ifneq ($(USE_FPGA),)
WRAPPER_CONFS_PREFIX=iob_system_$(BOARD)
WRAPPER_DIR=src
else
WRAPPER_CONFS_PREFIX=iob_uut
WRAPPER_DIR=simulation/src
endif

iob_bsp:
	sed 's/$(WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' $(WRAPPER_DIR)/$(WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h

iob_system_firmware: iob_bsp
	make $@.elf INCLUDES="$(IOB_SYSTEM_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_FW_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_system_boot: iob_bsp
	make $@.elf INCLUDES="$(IOB_SYSTEM_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_BOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_system_preboot:
	make $@.elf INCLUDES="$(IOB_SYSTEM_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_PREBOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" NO_HW_DRIVER=1


.PHONY: build_iob_system_software iob_bsp iob_system_firmware iob_system_boot iob_system_preboot

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.
EMUL_HDR+=iob_bsp

# SOURCES
EMUL_SRC+=src/iob_system_firmware.c
EMUL_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
EMUL_SRC+=$(addprefix src/,$(addsuffix _csrs_pc_emul.c,$(PERIPHERALS)))

# include software build segment of child systems
# child systems can add their own child_sw_build.mk without having to override this one.
ifneq ($(wildcard $(ROOT_DIR)/software/child_sw_build.mk),)
include $(ROOT_DIR)/software/child_sw_build.mk
endif
