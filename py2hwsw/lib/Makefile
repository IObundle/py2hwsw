# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile runs the examples in the IObundle library.
#

BUILD_DIR ?=build
INIT_MEM ?= 1
USE_EXTMEM ?= 0
BOARD ?= iob_aes_ku040_db_g
#BOARD_SERIAL_PORT ?= /dev/ttyUSB1

MEM_ADDR_W ?= 18
FW_ADDR_W ?= 18

# Default lib module to setup. Can be overriden by the user.
CORE ?= hardware/basic_tests/iob_and/iob_and.py

# List of lib cores that pass linter checks. This list will be deprecated when all lib cores pass linter checks.
CORES_READY_FOR_LINT=iob_pulse_gen iob_and iob_aoi

# Check if $(CORE) is in $(CORES_READY_FOR_LINT)
ifeq ($(filter $(CORE),$(CORES_READY_FOR_LINT)),)
SETUP_ARGS =--no_verilog_lint 
endif

all: sim-run

py2shell:
	nix-shell --run "py2hwsw_shell"

$(BUILD_DIR):
	nix-shell --run "py2hwsw_shell < $(CORE)"

#
# Simulation targets
#
sim-build: clean $(BUILD_DIR)
	nix-shell --run "make -C $(BUILD_DIR) sim-build"

sim-run: sim-build
	nix-shell --run "VCD=$(VCD) make -C $(BUILD_DIR) sim-run"

# List of tests to run
TESTS = hardware/basic_tests/iob_and/iob_and.py

sim-test: (TESTS)

$(TESTS):
	nix-shell --run "make -C $(BUILD_DIR) sim-run"

sim-clean:
	nix-shell --run "make -C $(BUILD_DIR) sim-clean"

#
# FPGA targets
#

fpga-build: clean $(BUILD_DIR)
	nix-shell --run "make -C $(BUILD_DIR) fpga-build"

fpga-run: fpga-build
	make -C $(BUILD_DIR)/ fpga-run BOARD=$(BOARD)

#
# Documentation targets
#

doc-build: 
	nix-shell --run "make clean setup -C $(BUILD_DIR) doc-build"

py2-doc-build:

py2-doc-update:

#fix me
delivery:
	nix-shell --run "py2hwsw $(CORE) deliver --build_dir '$(BUILD_DIR)'"

#fix me
lib-ipxact:
	nix-shell --run "py2hwsw --browse"
	./scripts/kactus2/import_library.py `realpath $(CURDIR)`/ipxact_lib
	nix-shell --run "kactus2"

# Install board server and client
board_server_install:
	sudo cp ../scripts/board_server.py /usr/local/bin/ && \
        sudo cp ../scripts/board_server.service /etc/systemd/system/ && \
        sudo systemctl daemon-reload && \
	sudo systemctl enable board_server && \
	sudo systemctl restart board_server

board_server_uninstall:
	sudo systemctl stop board_server && \
        sudo systemctl disable board_server && \
        sudo rm /usr/local/bin/board_server.py && \
        sudo rm /etc/systemd/system/board_server.service && \
        sudo systemctl daemon-reload

board_server_status:
	sudo systemctl status board_server

.PHONY: board_server_install board_server_uninstall board_server_status


clean:
	@if [ -d $(BUILD_DIR) ]; then \
		make -C $(BUILD_DIR) clean; \
		rm -rf $(BUILD_DIR); \
	fi
	@find . -name \*~ -delete


.PHONY: all py2shell setup sim-build sim-run sim-test fpga-build fpga-run doc-build py2-doc-build py2-doc-update delivery lib-ipxact board_server_install board_server_uninstall board_server_status clean



