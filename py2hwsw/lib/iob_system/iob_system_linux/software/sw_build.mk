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
# Set UFLAGS to pass flow option to remote machines
UFLAGS +=BOOT_FLOW=$(BOOT_FLOW)
# Add boot_flow as dependency of simulation/fpga build process
BUILD_DEPS += boot_flow

boot_flow:
	echo -n "$(BOOT_FLOW)" > boot.flow
	# -n to avoid newline

# Set target as PHONY to ensure that it is built even if $(BOARD) is changed
.PHONY: boot_flow

#
# Macros
#

#Function to obtain parameter named $(1) in verilog header file located in $(2)
#Usage: $(call GET_MACRO,<param_name>,<vh_path>)
GET_MACRO = $(shell grep "define $(1)" $(2) | rev | cut -d" " -f1 | rev)

#Function to obtain parameter named $(1) from iob_system_linux_conf.vh
GET_IOB_SYSTEM_LINUX_CONF_MACRO = $(call GET_MACRO,IOB_SYSTEM_LINUX_$(1),$(ROOT_DIR)/hardware/src/iob_system_linux_conf.vh)

ifeq ($(USE_FPGA),)
SIMULATION=1
endif

ifeq ($(SIMULATION),)
WRAPPER_CONFS_PREFIX=iob_system_linux_$(BOARD)
WRAPPER_DIR=src
else
WRAPPER_CONFS_PREFIX=iob_uut
WRAPPER_DIR=simulation/src
endif

#
# Bootloader
#

iob_system_linux_bootrom.hex: ../../software/iob_system_linux_preboot.bin ../../software/iob_system_linux_boot.bin
	../../scripts/makehex.py $^ 00000080 $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,BOOTROM_ADDR_W) $@

#
# OS
#

# Set UFLAGS to pass RUN_LINUX option to remote machines
UFLAGS +=RUN_LINUX=$(RUN_LINUX)
# OS sources and parameters
ifeq ($(RUN_LINUX),1)
OS_DIR = $(ROOT_DIR)/submodules/iob_linux
# Relative path from OS directory to Root directory
REL_OS2ROOT :=`realpath $(ROOT_DIR) --relative-to=$(OS_DIR)`
OPENSBI_DIR = fw_jump.bin
DTB_DIR = iob_system_linux.dtb
DTB_ADDR:=00F80000
LINUX_DIR = Image
LINUX_ADDR:=00400000
ROOTFS_DIR = rootfs.cpio.gz
ROOTFS_ADDR:=01000000
FIRM_ARGS = $(OPENSBI_DIR)
FIRM_ARGS += $(DTB_DIR) $(DTB_ADDR)
FIRM_ARGS += $(LINUX_DIR) $(LINUX_ADDR)
FIRM_ARGS += $(ROOTFS_DIR) $(ROOTFS_ADDR)
UTARGETS += compile_device_tree compile_opensbi
FIRMWARE := fw_jump.bin iob_system_linux.dtb Image rootfs.cpio.gz
# Set simulation/FPGA board grab timeout to 1 hour
GRAB_TIMEOUT ?= 3600
else
FIRM_ARGS = $<
UTARGETS += iob_system_linux_firmware 
FIRMWARE := iob_system_linux_firmware.bin
endif
FIRM_ADDR_W = $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,MEM_ADDR_W)

# Common firmware targets
iob_system_linux_firmware.hex: $(FIRMWARE)
	../../scripts/makehex.py $(FIRM_ARGS) $(FIRM_ADDR_W) $@
#	../../scripts/hex_split.py iob_system_linux_firmware .
	../../scripts/makehex.py --split $< $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,MEM_ADDR_W) $@

iob_system_linux_firmware.bin: ../../software/iob_system_linux_firmware.bin
	cp $< $@


# Linux specific targets
fw_jump.bin iob_system_linux.dtb:
	cp $(OS_DIR)/software/OS_build/$@ .

Image rootfs.cpio.gz:
	cp $(ROOT_DIR)/software/src/$@ .

ifeq ($(SIMULATION),1)
FLOW_DIR = $(ROOT_DIR)/hardware/simulation
else  # FPGA
BOARD_DIR := $(shell find hardware/fpga -name $(BOARD) -type d -print -quit)
FLOW_DIR = $(ROOT_DIR)/$(BOARD_DIR)
endif

# Generate linux_build_macros.txt from conf.h and mmap.h files
linux_build_macros.txt:
	# Copy every line that starts with #define from <flow>_conf.h, and remove the prefix
	sed '/^#define $(WRAPPER_CONFS_PREFIX)_/I!d; s/#define $(WRAPPER_CONFS_PREFIX)_//Ig' $(WRAPPER_DIR)/$(WRAPPER_CONFS_PREFIX)_conf.h > $@
	# Include mmap.h info in linux_build_macros.txt
	grep '^#define ' src/iob_system_linux_mmap.h | sed 's/^#define //; s/0x//g' >> $@
	# Include macros from iob_system_linux_conf
	sed '/^#define IOB_SYSTEM_LINUX_/I!d; s/#define IOB_SYSTEM_LINUX_//Ig' src/iob_system_linux_conf.h >> $@
	# Delete duplicate macros
	awk '!seen[$$1]++' $@ > $@.tmp && mv $@.tmp $@

# Set targets as PHONY to ensure that they are built even if $(BOARD) is changed
.PHONY: linux_build_macros.txt

compile_device_tree: linux_build_macros.txt
	nix-shell $(OS_DIR)/default.nix --run 'make -C $(OS_DIR) build-dts MACROS_FILE=$(REL_OS2ROOT)/software/linux_build_macros.txt DTS_FILE=$(REL_OS2ROOT)/software/iob_system_linux.dts'

compile_opensbi:
	nix-shell $(OS_DIR)/default.nix --run 'make -C $(OS_DIR) build-opensbi MACROS_FILE=$(REL_OS2ROOT)/software/linux_build_macros.txt OPENSBI_PLATFORM_DIR=$(REL_OS2ROOT)/software/opensbi_platform/iob_system_linux'

.PHONY: compile_device_tree compile_opensbi

#
# Dependencies
#

../../software/%.bin:
	make -C ../../ sw-build

UTARGETS +=tb
TB_SRC+=./simulation/src/iob_uart_csrs.c
TB_INCLUDES ?=-I./simulation/src

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

# # NOTE: (Ruben) To speed up simulation, we do not include or simulate crypto code in simulation. It greatly increases binary size and some tests would take forever. Better to run all tests in fpga-run.
# IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto.c
# IOB_SYSTEM_LINUX_FW_SRC+=src/crypto/aes.c
# IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto_common_tests.c
# ifeq ($(SIMULATION),1)
# IOB_SYSTEM_LINUX_FW_SRC+=src/versat_simple_crypto_tests.c
# IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/arena.c)
# IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/common/sha2.c)
# else
# IOB_SYSTEM_LINUX_FW_SRC+=src/versat_crypto_tests.c
# IOB_SYSTEM_LINUX_FW_SRC+=src/versat_mceliece.c
# IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/*.c)
# IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/crypto/McEliece/common/*.c)
# endif

# CRYPTO_SRC := src/iob-versat.c $(wildcard src/linux/*.c) $(wildcard src/crypto/McEliece/*.c) $(wildcard src/crypto/McEliece/common/*.c)
# CRYPTO_HDR := $(wildcard src/linux/*.h) $(wildcard src/crypto/McEliece/*.h)
# UTARGETS+=crypto
# 
# crypto:
# 	riscv64-unknown-linux-gnu-gcc -std=gnu99 -march=rv32imac -mabi=ilp32 -Wcast-align=strict -Os -s -ffunction-sections $(CRYPTO_SRC) -o crypto -Isrc/crypto/McEliece -Isrc/crypto/McEliece/common -Isrc/linux -Wl,-gc-sections -Wl,--strip-all
# 
# .PHONY: crypto


# PERIPHERAL SOURCES
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
# Only add driver files if they exist
IOB_SYSTEM_LINUX_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
IOB_SYSTEM_LINUX_FW_SRC+=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))
# Filter out iob_uart16550_csrs.c since it has no csrs
IOB_SYSTEM_LINUX_FW_SRC:=$(filter-out src/iob_uart16550_csrs.c,$(IOB_SYSTEM_LINUX_FW_SRC))


# BOOTLOADER SOURCES
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.S
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_uart16550.c
# IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_uart16550_csrs.c # UART16550 does not have csrs file
ifneq ($(USE_ETHERNET),)
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_eth.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_eth_csrs.c
endif
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_spi.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_spiplatform.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_spi_master_csrs.c
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_printf.c


# PREBOOT SOURCES
IOB_SYSTEM_LINUX_PREBOOT_SRC=src/iob_system_linux_preboot.S


UTARGETS +=iob_system_linux_baremetal_boot check_if_run_linux

iob_system_linux_baremetal_boot: iob_system_linux_boot iob_system_linux_preboot

iob_bsp:
	sed 's/$(WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' $(WRAPPER_DIR)/$(WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h

iob_system_linux_firmware: iob_bsp
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_FW_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

check_if_run_linux:
	python3 $(ROOT_DIR)/scripts/check_if_run_linux.py $(ROOT_DIR) iob_system_linux $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,FW_BASEADDR) $(RUN_LINUX)

iob_system_linux_boot: iob_bsp
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_BOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)"

iob_system_linux_preboot:
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_PREBOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" NO_HW_DRIVER=1


.PHONY: iob_system_linux_baremetal_boot iob_bsp iob_system_linux_firmware check_if_run_linux iob_system_linux_boot iob_system_linux_preboot

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
