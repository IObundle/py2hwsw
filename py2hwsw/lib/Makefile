# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile simulates the hardware modules in this repo
#

BUILD_DIR ?=build
BOARD ?= iob_aes_ku040_db_g
#BOARD_SERIAL_PORT ?= /dev/ttyUSB1

# Used by test.sh
LIB_DIR:=.
export LIB_DIR

# Default lib module to setup. Can be overriden by the user.
CORE ?=iob_ctls

CSR_IF?=iob

# Fill PY_PARAMS if not defined
ifeq ($(PY_PARAMS),)
PY_PARAMS="csr_if=$(CSR_IF)"

# IOb-System parameters
ifneq ($(INIT_MEM),)
PY_PARAMS +=":init_mem=$(INIT_MEM)"
endif
ifneq ($(USE_EXTMEM),)
PY_PARAMS +=":use_extmem=$(USE_EXTMEM)"
endif
ifneq ($(USE_ETHERNET),)
PY_PARAMS +=":use_ethernet=$(USE_ETHERNET)"
endif
ifneq ($(MEM_ADDR_W),)
PY_PARAMS +=":mem_addr_w=$(MEM_ADDR_W)"
endif
ifneq ($(FW_ADDR_W),)
PY_PARAMS +=":fw_addr_w=$(FW_ADDR_W)"
endif
endif # ifndef PY_PARAMS

# List of lib cores that pass linter checks. This list will be deprecated when all lib cores pass linter checks.
CORES_READY_FOR_LINT=iob_pulse_gen iob_and iob_aoi iob_timer iob_uart

# Check if $(CORE) is in $(CORES_READY_FOR_LINT)
ifeq ($(filter $(CORE),$(CORES_READY_FOR_LINT)),)
SETUP_ARGS =--no_verilog_lint 
endif

all: sim-test

setup:
	nix-shell --run "py2hwsw $(CORE) setup --build_dir '$(BUILD_DIR)' --py_params '$(PY_PARAMS)' $(SETUP_ARGS)"

sim-build:
	nix-shell --run "scripts/test.sh build $(CORE)"

sim-run:
	nix-shell --run "VCD=$(VCD) scripts/test.sh $(CORE)"

sim-test:
	nix-shell --run "scripts/test.sh test"

sim-clean:
	nix-shell --run "scripts/test.sh clean"

fpga-build:
	nix-shell --run "make clean setup && make -C $(BUILD_DIR) fpga-sw-build BOARD=$(BOARD)" && make -C $(BUILD_DIR)/ fpga-build BOARD=$(BOARD)

fpga-run: fpga-build
	make -C $(BUILD_DIR)/ fpga-run BOARD=$(BOARD)


doc-build: 
	nix-shell --run "make clean setup && make -C $(BUILD_DIR) doc-build"

py2-doc-build:
	nix-shell --run "py2hwsw --py2hwsw_docs && make -C py2hwsw_generated_docs/document/ build"

py2-doc-update:
	cp py2hwsw_generated_docs/document/ug.pdf ../py2hwsw_document/document/ug.pdf


delivery:
	nix-shell --run "py2hwsw $(CORE) deliver --build_dir '$(BUILD_DIR)'"


lib-ipxact:
	nix-shell --run "py2hwsw --browse"
	./scripts/kactus2/import_library.py `realpath $(CURDIR)`/ipxact_lib
	nix-shell --run "kactus2"


.PHONY: all setup sim-build sim-run sim-test sim-clean fpga-build fpga-clean doc-build py2-doc-build py2-doc-update delivery lib-ipxact


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
	nix-shell --run "py2hwsw $(CORE) clean --build_dir '$(BUILD_DIR)'"
	@rm -rf ../*.summary ../*.rpt py2hwsw_generated_docs
	@find . -name \*~ -delete

.PHONY: clean
