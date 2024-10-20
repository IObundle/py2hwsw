# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile simulates the hardware modules in this repo
#

BUILD_DIR ?=build
INIT_MEM ?= 1
USE_EXTMEM ?= 0
BOARD ?= aes_ku040_db_g
 
# Used by test.sh
LIB_DIR:=.
export LIB_DIR

# Default lib module to setup. Can be overriden by the user.
CORE ?=iob_ctls


all: sim-test

setup:
	nix-shell --run "py2hwsw $(CORE) setup --build_dir '$(BUILD_DIR)' --no_verilog_lint"

sim-build:
	nix-shell --run "scripts/test.sh build $(CORE)"

sim-run:
	nix-shell --run "VCD=$(VCD) scripts/test.sh $(CORE)"

sim-test:
	nix-shell --run "scripts/test.sh test"

sim-clean:
	nix-shell --run "scripts/test.sh clean"

print-attr:
	nix-shell --run "VCD=$(VCD) SETUP_ARGS='print_attr' scripts/test.sh $(CORE)"

fpga-build:
	nix-shell --run "make clean setup CORE=$(CORE) INIT_MEM=$(INIT_MEM) USE_EXTMEM=$(USE_EXTMEM) && make -C $(BUILD_DIR) fpga-fw-build BOARD=$(BOARD)"
	make -C $(BUILD_DIR)/ fpga-build BOARD=$(BOARD)


.PHONY: all setup sim-build sim-run sim-test sim-clean print-attr fpga-build fpga-clean


# Install board server and client
board_server_install:
	sudo cp scripts/board_client.py /usr/local/bin/ && \
	sudo cp scripts/board_server.py /usr/local/bin/ && \
        sudo cp scripts/board_server.service /etc/systemd/system/ && \
        sudo systemctl daemon-reload && \
	sudo systemctl enable board_server && \
	sudo systemctl restart board_server

board_server_uninstall:
	sudo systemctl stop board_server && \
        sudo systemctl disable board_server && \
        sudo rm /usr/local/bin/board_client.py && \
        sudo rm /usr/local/bin/board_server.py && \
        sudo rm /etc/systemd/system/board_server.service && \
        sudo systemctl daemon-reload

board_server_status:
	sudo systemctl status board_server

.PHONY: board_server_install board_server_uninstall board_server_status


clean:
	nix-shell --run "py2hwsw $(CORE) clean --build_dir '$(BUILD_DIR)'"
	@rm -rf ../*.summary ../*.rpt 
	@find . -name \*~ -delete

.PHONY: clean
