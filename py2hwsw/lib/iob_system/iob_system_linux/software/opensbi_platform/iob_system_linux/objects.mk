#
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (C) 2019 FORTH-ICS/CARV
#		Panagiotis Peristerakis <perister@ics.forth.gr>
#

# Compiler flags
platform-cppflags-y =
platform-cflags-y =
platform-asflags-y =
platform-ldflags-y =

# Object to build
platform-objs-y += platform.o

#
# Command for platform specific "make run"
# Useful for development and debugging on plaftform simulator (such as QEMU)
#
OS_BUILD_DIR ?= ../../software/OS_build
platform-runcmd = cp build/platform/iob_system_linux/firmware/*.bin $(OS_BUILD_DIR)

#
# Platform RISC-V XLEN, ABI, ISA and Code Model configuration.
# These are optional parameters but platforms can optionaly provide it.
# Some of these are guessed based on GCC compiler capabilities
#
PLATFORM_RISCV_XLEN = 32
PLATFORM_RISCV_ABI = ilp32
PLATFORM_RISCV_ISA = rv32imac
# PLATFORM_RISCV_CODE_MODEL = medany

# Firmware load address configuration. This is mandatory.
FW_TEXT_START=0x80000000

# Optional parameter for path to external FDT
# FW_FDT_PATH="path to platform flattened device tree file"

#
# Dynamic firmware configuration.
# Optional parameters are commented out. Uncomment and define these parameters
# as needed.
#
FW_DYNAMIC=n

#
# Jump firmware configuration.
# Optional parameters are commented out. Uncomment and define these parameters
# as needed.
#
FW_JUMP=y
# This needs to be 4MB aligned for 32-bit support
# This needs to be 2MB aligned for 64-bit support
ifeq ($(PLATFORM_RISCV_XLEN), 32)
FW_JUMP_ADDR=0x80400000
else
FW_JUMP_ADDR=0x80200000
endif
FW_JUMP_FDT_ADDR=0x80F80000

#
# Firmware with payload configuration.
# Optional parameters are commented out. Uncomment and define these parameters
# as needed.
#
FW_PAYLOAD=n
# This needs to be 4MB aligned for 32-bit support
# This needs to be 2MB aligned for 64-bit support
ifeq ($(PLATFORM_RISCV_XLEN), 32)
FW_PAYLOAD_OFFSET=0x400000
else
FW_PAYLOAD_OFFSET=0x200000
endif
# FW_PAYLOAD_ALIGN=0x1000
# FW_PAYLOAD_PATH="path to next boot stage binary image file"
FW_PAYLOAD_FDT_ADDR=0x80F80000
