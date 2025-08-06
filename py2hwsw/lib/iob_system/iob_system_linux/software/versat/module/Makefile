# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

LINUX_DIR := ../../../submodules/OS/submodules/linux-5.15.98
PWD:=$(shell pwd)
obj-m += versat.o

# In order to compile the versat linux module, need to go to the submodules/OS folder, enter the nix-shell and do "make build-linux-kernel". 
# Afterwards, while inside the same nix-shell, cd to this directory and do "make". The result is a module called versat.ko
# This module is included as well in order to simplify the build process, because compiling the module requires building the entire linux-kernel.

all: module

module:
	$(MAKE) ARCH=riscv CROSS_COMPILE=riscv64-unknown-linux-gnu- -C $(LINUX_DIR) M=$(PWD) modules

clean:
	find . ! -name 'Makefile' -and ! -name '*.c' -and ! -name '*.h' -and ! -name '*.sh' -and ! -name '*.ko' -type f -exec rm -f {} +
	rm -f versat.mod.c
