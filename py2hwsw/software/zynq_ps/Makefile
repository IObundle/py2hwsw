
# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

VITIS_VERSION = 2024.2
VITIS_SETTINGS = /opt/Xilinx/Vitis/$(VITIS_VERSION)/settings64.sh

.PHONY: build

build:
	vitis -p sw_build.tcl





# Paths
ARM_TOOLCHAIN ?=  /opt/Xilinx/Vitis/2024.2/gnu/aarch32/lin/gcc-arm-none-eabi/bin


CC := $(ARM_TOOLCHAIN)/arm-none-eabi-gcc
OBJCOPY := $(ARM_TOOLCHAIN)/arm-none-eabi-objcopy

# Target
TARGET := ps_app
ELF := $(TARGET).elf
BIN := $(TARGET).bin

# Source files (add your source files here)
SRCS := $(wildcard src/*.c)
OBJS := $(SRCS:.c=.o)

# Compiler flags
CFLAGS := -O2 -mcpu=cortex-a9 -mfpu=vfpv3-d16 -mfloat-abi=hard \
          -ffreestanding -nostdlib -Wall -Werror

LDFLAGS := -T ./lscript.ld -nostdlib

all: $(ELF)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(ELF): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LDFLAGS) -o $@

bin: $(ELF)
	$(OBJCOPY) -O binary $< $(BIN)

clean:
	rm -f $(OBJS) $(ELF) $(BIN)

.PHONY: all clean bin
