# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This file becomes the fpga makefile when copied to the build
# directory

SHELL:=bash

include ../../config_build.mk

#include local fpga build segment
ifneq ($(wildcard fpga_build.mk),)
include fpga_build.mk
endif

REMOTE_BUILD_DIR=$(USER)/$(BUILD_DIR_NAME)
REMOTE_FPGA_DIR=$(REMOTE_BUILD_DIR)/hardware/fpga
PYTHON_DIR = ../../scripts

#default board
ifeq ($(BOARD),)
$(warning BOARD not set, skipping build)
$(exit 0)
endif

#fpga toolchain
FPGA_TOOL:=$(shell find . -name $(BOARD) | cut -d"/" -f2)

ifeq ($(FPGA_TOOL),)
$(warning Unsupported FPGA board $(BOARD) or FPGA toolchain. Check the board name and FPGA toochain installation.)
$(exit 0)
endif



FPGA_TOP ?=$(NAME)_$(BOARD)


include $(FPGA_TOOL)/$(BOARD)/board.mk
include $(FPGA_TOOL)/build.mk

#include the module's headers and sources
VHDR += $(wildcard ../src/*.vh) $(wildcard ./src/*.vh)
VSRC += $(wildcard ../src/*.v) $(wildcard ./src/*.v)
VHDR += $(wildcard ../common_src/*.vh)
VSRC += $(wildcard ../common_src/*.v)

ifneq ($(wildcard $(FPGA_TOOL)/$(BOARD)/$(FPGA_TOP).v),)
VSRC+=$(FPGA_TOOL)/$(BOARD)/$(FPGA_TOP).v
endif

UFLAGS+=FPGA_TOP=$(FPGA_TOP)
UFLAGS+=IS_FPGA=$(IS_FPGA)
UFLAGS+=USE_QUARTUS_PRO=$(USE_QUARTUS_PRO)

#build fpga image or netlist
build: $(VHDR) $(VSRC) $(BUILD_DEPS)
ifeq ($(FPGA_SERVER),)
	make $(FPGA_OBJ)
else 
	ssh $(FPGA_SSH_FLAGS) $(FPGA_USER)@$(FPGA_SERVER) "if [ ! -d $(REMOTE_BUILD_DIR) ]; then mkdir -p $(REMOTE_BUILD_DIR); fi"
	rsync $(FPGA_SYNC_FLAGS) -avz --force --delete --exclude 'software/tb' ../.. $(FPGA_USER)@$(FPGA_SERVER):$(REMOTE_BUILD_DIR)
	ssh -t $(FPGA_SSH_FLAGS) $(FPGA_USER)@$(FPGA_SERVER) 'if [ -f quartus_env ]; then source quartus_env $(USE_QUARTUS_PRO); fi; make -C $(REMOTE_FPGA_DIR) $@ BOARD=$(BOARD) $(UFLAGS)'
	scp $(FPGA_SCP_FLAGS) $(FPGA_USER)@$(FPGA_SERVER):$(REMOTE_FPGA_DIR)/$(FPGA_OBJ) .
	scp -r $(FPGA_SCP_FLAGS) $(FPGA_USER)@$(FPGA_SERVER):$(REMOTE_FPGA_DIR)/reports .
ifneq ($(FPGA_STUB),)
	scp $(FPGA_SCP_FLAGS) $(FPGA_USER)@$(FPGA_SERVER):$(REMOTE_FPGA_DIR)/$(FPGA_STUB) .
endif
endif

BOARD_SERIAL_PORT ?=/dev/usb-uart
#console start command
CONSOLE_CMD ?=$(PYTHON_DIR)/console.py -s $(BOARD_SERIAL_PORT)

#board client command
GRAB_TIMEOUT ?= 300
BOARD_GRAB_CMD=../../scripts/board_client.py grab $(GRAB_TIMEOUT)

#run fpga image
run: build $(RUN_DEPS)
ifneq ($(NORUN),1)
ifeq ($(BOARD_SERVER),)
	$(BOARD_GRAB_CMD) -p '$(FPGA_PROG)' -c '$(CONSOLE_CMD)'  && echo "Checking test log..." && test "$$(cat test.log)" = "Test passed!"
else
	ssh $(BOARD_USER)@$(BOARD_SERVER) "if [ ! -d $(REMOTE_BUILD_DIR) ]; then mkdir -p $(REMOTE_BUILD_DIR); fi"
	rsync $(BOARD_SYNC_FLAGS) -avz --force --delete --exclude 'software/tb' ../.. $(BOARD_USER)@$(BOARD_SERVER):$(REMOTE_BUILD_DIR)
	ssh -t $(BOARD_USER)@$(BOARD_SERVER) 'if [ -f quartus_env ]; then source quartus_env $(USE_QUARTUS_PRO); fi; make -C $(REMOTE_FPGA_DIR) $@ BOARD=$(BOARD) GRAB_TIMEOUT=$(GRAB_TIMEOUT) $(UFLAGS)'
	scp $(BOARD_USER)@$(BOARD_SERVER):$(REMOTE_FPGA_DIR)/*.log . 2> /dev/null | true
endif
endif

# clean
clean: $(FPGA_TOOL)-clean
	find . -maxdepth 1 -type f -not \( -name "Makefile" -o -name "fpga_build.mk" -o -name "uut_build.mk" \) -delete
	@rm -rf resynthesis *.hex
ifneq ($(FPGA_SERVER),)
	ssh $(FPGA_SSH_FLAGS) $(FPGA_USER)@$(FPGA_SERVER) 'rm -rf $(REMOTE_BUILD_DIR)'
ifneq ($(BOARD_SERVER),)
	ssh $(BOARD_SSH_FLAGS) $(BOARD_USER)@$(BOARD_SERVER) 'rm -rf  $(REMOTE_BUILD_DIR)'
endif
endif

test: $(TEST_LIST)

build_deps: $(RUN_DEPS)

run_deps: $(RUN_DEPS)

debug:
	@echo SIMULATOR=$(SIMULATOR)
	@echo BOARD=$(BOARD)
	@echo VHDR=$(VHDR)
	@echo VSRC=$(VSRC)
	@echo FPGA_SERVER=$(FPGA_SERVER)
	@echo FPGA_OBJ=$(FPGA_OBJ)

.PRECIOUS: $(FPGA_OBJ) test.log s_fw.bin

.PHONY: run build clean debug test build_deps run_deps $(TEST_LIST)
