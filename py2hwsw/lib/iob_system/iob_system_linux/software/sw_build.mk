# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#########################################
#            Embedded targets           #
#########################################
ROOT_DIR ?=..

include $(ROOT_DIR)/software/auto_sw_build.mk

# Local embedded makefile settings for custom bootloader and firmware targets.

# Bootloader flow options:
# 1. CONSOLE_TO_EXTMEM: default: load firmware from console to external memory
# 2. CONSOLE_TO_FLASH: program flash with firmware
# 3. FLASH_TO_EXTMEM: load firmware from flash to external memory 
BOOT_FLOW ?= CONSOLE_TO_EXTMEM
UTARGETS += boot_flow

boot_flow:
	echo -n "$(BOOT_FLOW)" > boot.flow
	# -n to avoid newline


#
# Macros
#

#Function to obtain parameter named $(1) in verilog header file located in $(2)
#Usage: $(call GET_MACRO,<param_name>,<vh_path>)
GET_MACRO = $(shell grep "define $(1)" $(2) | rev | cut -d" " -f1 | rev)

#Function to obtain parameter named $(1) from iob_system_linux_conf.vh
GET_IOB_SYSTEM_LINUX_CONF_MACRO = $(call GET_MACRO,IOB_SYSTEM_LINUX_$(1),../src/iob_system_linux_conf.vh)

ifeq ($(USE_FPGA),)
SIMULATION=1
endif

#
# Bootloader
#

iob_system_linux_bootrom.hex: ../../software/iob_system_linux_preboot.bin ../../software/iob_system_linux_boot.bin
	../../scripts/makehex.py $^ 00000080 $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,BOOTROM_ADDR_W) $@

#
# OS
#

# OS sources and parameters
ifeq ($(RUN_LINUX),1)
OS_DIR = ../../software/src
OPENSBI_DIR = fw_jump.bin
DTB_DIR = iob_soc.dtb
DTB_ADDR:=00F80000
LINUX_DIR = Image
LINUX_ADDR:=00400000
ROOTFS_DIR = rootfs.cpio.gz
ROOTFS_ADDR:=01000000
FIRM_ARGS = $(OPENSBI_DIR)
FIRM_ARGS += $(DTB_DIR) $(DTB_ADDR)
FIRM_ARGS += $(LINUX_DIR) $(LINUX_ADDR)
FIRM_ARGS += $(ROOTFS_DIR) $(ROOTFS_ADDR)
FIRM_ADDR_W = $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,OS_ADDR_W)
FIRMWARE := fw_jump.bin iob_soc.dtb Image rootfs.cpio.gz
else
FIRM_ARGS = $<
FIRM_ADDR_W = $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,MEM_ADDR_W)
FIRMWARE := iob_system_linux_firmware.bin
endif

# Common firmware targets
iob_system_linux_firmware.hex: $(FIRMWARE)
	../../scripts/makehex.py $(FIRM_ARGS) $(FIRM_ADDR_W) > $@
#	../../scripts/hex_split.py iob_system_linux_firmware .
	../../scripts/makehex.py --split $< $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,MEM_ADDR_W) $@

iob_system_linux_firmware.bin: ../../software/iob_system_linux_firmware.bin
	cp $< $@


# Linux specific targets
Image rootfs.cpio.gz:
	cp $(OS_DIR)/$@ .

# Copy files from correct board directory
fw_jump.bin iob_soc.dtb:
	if [ "$(FPGA_TOOL)" != "" ]; then\
		cp $(FPGA_TOOL)/$(BOARD)/$@ .;\
	fi
# Set targets as PHONY to ensure that they are copied even if $(BOARD) is changed
.PHONY: fw_jump.bin iob_soc.dtb boot_flow

#
# Dependencies
#

../../software/%.bin:
	make -C ../../ sw-build

UTARGETS+=build_iob_system_linux_software tb
CSRS=./src/iob_uart_csrs.c

TEMPLATE_LDS=src/$@.lds


## define simulator in uppercase
#ifneq ($(SIMULATOR),)
#SIM_DEFINE=-D$(shell echo $(SIMULATOR) | tr  '[:lower:]' '[:upper:]')
#endif
#
## Compiler FLAGS with custom architecture, including atomic instructions
#IOB_SYSTEM_LINUX_CFLAGS ?=-Os -nostdlib -march=rv32imac -mabi=ilp32 --specs=nano.specs -Wcast-align=strict $(SIM_DEFINE)
IOB_SYSTEM_LINUX_CFLAGS ?=-Os -nostdlib -march=rv32imac -mabi=ilp32 --specs=nano.specs -Wcast-align=strict

IOB_SYSTEM_LINUX_INCLUDES=-Isrc -Isrc/crypto/McEliece -Isrc/crypto/McEliece/common

IOB_SYSTEM_LINUX_LFLAGS=-Wl,-L,src,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
IOB_SYSTEM_LINUX_FW_SRC=src/iob_system_linux_firmware.S
IOB_SYSTEM_LINUX_FW_SRC+=src/iob_system_linux_firmware.c
IOB_SYSTEM_LINUX_FW_SRC+=src/iob_printf.c

# NOTE: (Ruben) To speed up simulation, we do not include or simulate crypto code in simulation. It greatly increases binary size and some tests would take forever. Better to run all tests in fpga-run.
IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto.c
IOB_SYSTEM_LINUX_FW_SRC+=src/crypto/aes.c
IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto_common_tests.c
ifeq ($(SIMULATION),1)
IOB_SYSTEM_LINUX_FW_SRC+=src/versat_simple_crypto_tests.c
IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/arena.c)
IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/common/sha2.c)
else
IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto_tests.c
IOB_SYSTEM_LINUX_FW_SRC+=src/versat_mceliece.c
IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/*.c)
IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/common/*.c)
endif


# PERIPHERAL SOURCES
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
# Only add driver files if they exist
IOB_SYSTEM_LINUX_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
IOB_SYSTEM_LINUX_FW_SRC+=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))


# BOOTLOADER SOURCES
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.S
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_uart.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_uart_csrs.c
# IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_eth.c
# IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_eth_csrs.c
# IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_spi.c
# IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob__csrs.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_printf.c


# PREBOOT SOURCES
IOB_SYSTEM_LINUX_PREBOOT_SRC=src/iob_system_linux_preboot.S


build_iob_system_linux_software: iob_system_linux_firmware iob_system_linux_boot iob_system_linux_preboot

ifeq ($(SIMULATION),)
WRAPPER_CONFS_PREFIX=iob_system_linux_$(BOARD)
else
WRAPPER_CONFS_PREFIX=iob_uut
endif

iob_bsp:
	sed 's/$(WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' src/$(WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h

iob_system_linux_firmware: iob_bsp check_if_run_linux
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_FW_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

check_if_run_linux:
	python3 $(ROOT_DIR)/scripts/check_if_run_linux.py $(ROOT_DIR) iob_system_linux $(RUN_LINUX)

iob_system_linux_boot: iob_bsp
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_BOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_system_linux_preboot:
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_PREBOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" NO_HW_DRIVER=1


.PHONY: build_iob_system_linux_software iob_bsp iob_system_linux_firmware iob_system_linux_boot iob_system_linux_preboot

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.
EMUL_HDR+=iob_bsp

# SOURCES
EMUL_SRC+=src/iob_system_linux_firmware.c
EMUL_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
EMUL_SRC+=$(addprefix src/,$(addsuffix _csrs_pc_emul.c,$(PERIPHERALS)))
