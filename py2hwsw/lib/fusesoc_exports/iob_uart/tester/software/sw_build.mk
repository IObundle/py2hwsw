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

#Function to obtain parameter named $(1) from iob_uart_tester_conf.vh
GET_IOB_UART_TESTER_CONF_MACRO = $(call GET_MACRO,IOB_UART_TESTER_$(1),$(ROOT_DIR)/hardware/src/iob_uart_tester_conf.vh)

iob_uart_tester_bootrom.hex: ../../software/iob_uart_tester_preboot.bin ../../software/iob_uart_tester_boot.bin
	../../scripts/makehex.py $^ 00000080 $(call GET_IOB_UART_TESTER_CONF_MACRO,BOOTROM_ADDR_W) $@

iob_uart_tester_firmware.hex: iob_uart_tester_firmware.bin
	../../scripts/makehex.py $< $(call GET_IOB_UART_TESTER_CONF_MACRO,MEM_ADDR_W) $@
	../../scripts/makehex.py --split $< $(call GET_IOB_UART_TESTER_CONF_MACRO,MEM_ADDR_W) $@

iob_uart_tester_firmware.bin: ../../software/iob_uart_tester_firmware.bin
	cp $< $@

../../software/%.bin:
	make -C ../../ sw-build

UTARGETS+=build_iob_uart_tester_software tb
TB_SRC+=./simulation/src/iob_uart_csrs.c
TB_INCLUDES ?=-I./simulation/src

TEMPLATE_LDS=src/$@.lds

IOB_UART_TESTER_INCLUDES=-Isrc

IOB_UART_TESTER_LFLAGS=-Wl,-L,src,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
IOB_UART_TESTER_FW_SRC=src/iob_uart_tester_firmware.S
IOB_UART_TESTER_FW_SRC+=src/iob_uart_tester_firmware.c
IOB_UART_TESTER_FW_SRC+=src/iob_printf.c
# PERIPHERAL SOURCES
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
# Only add driver files if they exist
IOB_UART_TESTER_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
IOB_UART_TESTER_FW_SRC+=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))

# BOOTLOADER SOURCES
IOB_UART_TESTER_BOOT_SRC+=src/iob_uart_tester_boot.S
IOB_UART_TESTER_BOOT_SRC+=src/iob_uart_tester_boot.c
IOB_UART_TESTER_BOOT_SRC+=src/iob_uart.c
IOB_UART_TESTER_BOOT_SRC+=src/iob_uart_csrs.c

# PREBOOT SOURCES
IOB_UART_TESTER_PREBOOT_SRC=src/iob_uart_tester_preboot.S

build_iob_uart_tester_software: iob_uart_tester_firmware iob_uart_tester_boot iob_uart_tester_preboot

ifneq ($(USE_FPGA),)
WRAPPER_CONFS_PREFIX=iob_uart_tester_$(BOARD)
WRAPPER_DIR=src
else
WRAPPER_CONFS_PREFIX=iob_uut
WRAPPER_DIR=simulation/src
endif

iob_bsp:
	sed 's/$(WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' $(WRAPPER_DIR)/$(WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h

iob_uart_tester_firmware: iob_bsp
	make $@.elf INCLUDES="$(IOB_UART_TESTER_INCLUDES)" LFLAGS="$(IOB_UART_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_UART_TESTER_FW_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_uart_tester_boot: iob_bsp
	make $@.elf INCLUDES="$(IOB_UART_TESTER_INCLUDES)" LFLAGS="$(IOB_UART_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_UART_TESTER_BOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_uart_tester_preboot:
	make $@.elf INCLUDES="$(IOB_UART_TESTER_INCLUDES)" LFLAGS="$(IOB_UART_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_UART_TESTER_PREBOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" NO_HW_DRIVER=1


.PHONY: build_iob_uart_tester_software iob_bsp iob_uart_tester_firmware iob_uart_tester_boot iob_uart_tester_preboot

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.
EMUL_HDR+=iob_bsp

# SOURCES
EMUL_SRC+=src/iob_uart_tester_firmware.c
EMUL_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
EMUL_SRC+=$(addprefix src/,$(addsuffix _csrs_pc_emul.c,$(PERIPHERALS)))

# include software build segment of child systems
# child systems can add their own child_sw_build.mk without having to override this one.
ifneq ($(wildcard $(ROOT_DIR)/software/child_sw_build.mk),)
include $(ROOT_DIR)/software/child_sw_build.mk
endif
