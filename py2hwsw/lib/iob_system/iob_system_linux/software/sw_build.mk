
#########################################
#            Embedded targets           #
#########################################
ROOT_DIR ?=..
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

#Function to obtain parameter named $(1) in verilog header file located in $(2)
#Usage: $(call GET_MACRO,<param_name>,<vh_path>)
GET_MACRO = $(shell grep "define $(1)" $(2) | rev | cut -d" " -f1 | rev)

#Function to obtain parameter named $(1) from iob_system_linux_conf.vh
GET_IOB_SYSTEM_LINUX_CONF_MACRO = $(call GET_MACRO,IOB_SYSTEM_LINUX_$(1),$(ROOT_DIR)/hardware/src/iob_system_linux_conf.vh)

ifneq ($(shell grep -s "#define SIMULATION" src/bsp.h),)
SIMULATION=1
endif

iob_system_linux_boot.hex: ../../software/iob_system_linux_boot.bin
	../../scripts/makehex.py $< $(call GET_IOB_SYSTEM_LINUX_CONF_MACRO,BOOTROM_ADDR_W) > $@
	../../scripts/hex_split.py iob_system_linux_boot .

#OS
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
iob_system_linux_firmware.hex: $(FIRMWARE)
	../../scripts/makehex.py $(FIRM_ARGS) $(FIRM_ADDR_W) > $@
	../../scripts/hex_split.py iob_system_linux_firmware .

iob_system_linux_firmware.bin: ../../software/iob_system_linux_firmware.bin
	cp $< $@

Image rootfs.cpio.gz:
	cp $(OS_DIR)/$@ .

fw_jump.bin iob_soc.dtb:
	if [ "$(FPGA_TOOL)" != "" ]; then\
		cp $(FPGA_TOOL)/$(BOARD)/$@ .;\
	fi
# Set targets as PHONY to ensure that they are copied even if $(BOARD) is changed
.PHONY: fw_jump.bin iob_soc.dtb boot_flow

../../software/%.bin:
	make -C ../../ fw-build


UTARGETS+=build_iob_system_linux_software

TEMPLATE_LDS=src/$@.lds

# define simulator in uppercase
ifneq ($(SIMULATOR),)
SIM_DEFINE=-D$(shell echo $(SIMULATOR) | tr  '[:lower:]' '[:upper:]')
endif

IOB_SYSTEM_LINUX_CFLAGS ?=-Os -nostdlib -march=rv32imac -mabi=ilp32 --specs=nano.specs -Wcast-align=strict $(SIM_DEFINE)

IOB_SYSTEM_LINUX_INCLUDES=-I. -Isrc -Isrc/crypto/McEliece -Isrc/crypto/McEliece/common

IOB_SYSTEM_LINUX_LFLAGS=-Wl,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
IOB_SYSTEM_LINUX_FW_SRC=src/iob_system_linux_firmware.S
IOB_SYSTEM_LINUX_FW_SRC+=src/iob_system_linux_firmware.c
IOB_SYSTEM_LINUX_FW_SRC+=src/printf.c

# NOTE(Ruben): To speed up simulation, we do not include or simulate crypto code in simulation. It greatly increases binary size and some tests would take forever. Better to run all tests in fpga-run.
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
IOB_SYSTEM_LINUX_FW_SRC+=$(wildcard src/iob-*.c)
IOB_SYSTEM_LINUX_FW_SRC+=$(filter-out %_emul.c, $(wildcard src/*swreg*.c))

# BOOTLOADER SOURCES
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.S
IOB_SYSTEM_LINUX_BOOT_SRC+=src/iob_system_linux_boot.c
IOB_SYSTEM_LINUX_BOOT_SRC+=$(filter-out %_emul.c, $(wildcard src/iob*uart*.c))
IOB_SYSTEM_LINUX_BOOT_SRC+=$(filter-out %_emul.c, $(wildcard src/iob*cache*.c))
IOB_SYSTEM_LINUX_BOOT_SRC+=$(filter-out %_emul.c, $(wildcard src/iob*eth*.c))
IOB_SYSTEM_LINUX_BOOT_SRC+=$(filter-out %_emul.c, $(wildcard src/iob*spi*.c))
IOB_SYSTEM_LINUX_BOOT_SRC+=src/printf.c

build_iob_system_linux_software: iob_system_linux_firmware iob_system_linux_boot

iob_system_linux_firmware: check_if_run_linux
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_FW_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" CFLAGS="$(IOB_SYSTEM_LINUX_CFLAGS)"

check_if_run_linux:
	python3 $(ROOT_DIR)/scripts/check_if_run_linux.py $(ROOT_DIR) iob_system_linux $(RUN_LINUX)

iob_system_linux_boot:
	make $@.elf INCLUDES="$(IOB_SYSTEM_LINUX_INCLUDES)" LFLAGS="$(IOB_SYSTEM_LINUX_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SYSTEM_LINUX_BOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" CFLAGS="$(IOB_SYSTEM_LINUX_CFLAGS)"


.PHONY: build_iob_system_linux_software iob_system_linux_firmware check_if_run_linux iob_system_linux_boot

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.

# SOURCES
EMUL_SRC+=src/iob_system_linux_firmware.c
EMUL_SRC+=src/printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(wildcard src/iob-*.c)

