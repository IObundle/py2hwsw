# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# Default to dynamic linking for small size.
# Use 'make STATIC=1' for a standalone binary.
STATIC ?= 0

BIN ?= iob_eth_test
SRC = $(BIN).c
CC = riscv64-unknown-linux-gnu-gcc
# Strip debug symbols to make binary smaller
STRIP = riscv64-unknown-linux-gnu-strip

# Use -Os for smaller size, or -O2 for best performance
FLAGS = -Wall -Werror -Os
FLAGS += -march=rv32imac
FLAGS += -mabi=ilp32

ifeq ($(STATIC), 1)
	FLAGS += -static
endif

$(BIN): $(SRC)
	$(CC) $(FLAGS) $(INCLUDE) -o $(BIN) $(SRC)
	$(STRIP) --strip-unneeded $(BIN)

clean:
	rm -f $(BIN)

.PHONY: clean
