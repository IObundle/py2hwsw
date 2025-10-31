# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This makefile is used at build-time

SHELL:=bash

include ../../config_build.mk

#default simulator
SIMULATOR ?=icarus


REMOTE_BUILD_DIR=$(USER)/$(BUILD_DIR_NAME)
REMOTE_SW_DIR=$(REMOTE_BUILD_DIR)/software
REMOTE_SIM_DIR=$(REMOTE_BUILD_DIR)/tester/hardware/simulation
PYTHON_DIR = ../../scripts

#include simulation headers and sources
VHDR+=$(wildcard ./src/*.vh)
VSRC+=$(wildcard ./src/*.v)

ifeq ($(SYN),)
#include the module's headers and sources
VHDR+=$(wildcard ../src/*.vh)
VSRC+=$(wildcard ../src/*.v)
#include the UUT's headers and sources
VHDR+=$(wildcard ../../../hardware/src/*.vh)
VSRC+=$(wildcard ../../../hardware/src/*.v)
INCLUDE_DIRS+=../../../hardware/src

VHDR+=$(wildcard ../common_src/*.vh)
VSRC+=$(wildcard ../common_src/*.v)
else
NODE ?= umc130
include ../syn/$(NODE)/sim.mk
VSRC+= ../syn/results/*.v
../syn/%.v:
	make -C ../syn build
endif

#include local simulation segment
ifneq ($(wildcard sim_build.mk),)
include sim_build.mk
endif

#select testbench type
ifneq ($(TBTYPE),UVM)
ifneq ($(wildcard ./src/$(NAME)_tb.v),)
TBTYPE?=V
TB?=$(NAME)_tb
else
ifneq ($(wildcard ../../software/src/iob_core_tb.c),)
TBTYPE?=C
TB?=iob_v_tb
else
TBTYPE?=none
endif
endif
else
TB?=iob_v_uvm_tb
endif
$(info Testbench is $(TB).v)

#
# Include the simulator stub
#
include $(SIMULATOR).mk



UFLAGS+=VCD=$(VCD)
UFLAGS+=COV=$(COV)
UFLAGS+=SYN=$(SYN)
UFLAGS+=NODE=$(NODE)
UFLAGS+=COV_TEST=$(COV_TEST)
UFLAGS+=TBTYPE=$(TBTYPE)

remote_build_dir:
ifneq ($(SIM_SERVER),)
	ssh $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) "if [ ! -d $(REMOTE_BUILD_DIR) ]; then mkdir -p $(REMOTE_BUILD_DIR); fi"
	rsync $(SIM_SYNC_FLAGS) -avz --force --delete --exclude 'software/tb' ../../.. $(SIM_USER)@$(SIM_SERVER):$(REMOTE_BUILD_DIR)
endif

#choose tetsbench type: C, verilog, uvm or none
ifeq ($(TBTYPE),V)
VSRC:=$(filter-out ./src/iob_v_tb.v, $(VSRC))
endif

ifeq ($(TBTYPE),UVM)
VSRC:=$(filter-out ./src/iob_v_tb.v, $(VSRC))
VSRC:=$(filter-out ./src/$(NAME)_tb.v, $(VSRC))
SIMULATOR:=xcelium
endif

ifeq ($(TBTYPE),C)
VSRC:=$(filter-out ./src/$(NAME)_tb.v, $(VSRC))
endif


build: $(VHDR) $(VSRC) $(BUILD_DEPS) remote_build_dir
ifeq ($(SIM_SERVER),)
	make comp
else
	ssh -t $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) 'make -C $(REMOTE_SIM_DIR) $@ SIMULATOR=$(SIMULATOR) $(UFLAGS)'
endif

#board client command
GRAB_TIMEOUT ?= 300
BOARD_GRAB_CMD=../../scripts/board_client.py grab $(GRAB_TIMEOUT)

run: $(BUILD_DEPS) test.log
	@if ! grep -q "Test passed!" test.log; then echo "Test failed!"; exit 1; fi

SIM_CMD=make exec
ifneq ($(TBTYPE),none)
ifneq ($(TBTYPE),V)
ifneq ($(SIMULATOR), verilator) #if the simulator is not verilator, run the the C testbench separately
#run the C testbench in background and kill it when simulator exits
SIM_CMD=../../software/tb & make exec && (kill $$! >/dev/null 2>&1; true) || (kill $$! >/dev/null 2>&1; false)
endif
endif
endif


test.log: build
ifneq ($(TB),none)

ifeq ($(SIM_SERVER),) #is simulator in local machine?

ifneq ($(CONSOLE_CMD),)
	$(BOARD_GRAB_CMD) -s '$(SIM_CMD)' -c '$(CONSOLE_CMD)' && echo "Checking test log..." && sleep 2
else
	$(BOARD_GRAB_CMD) -s '$(SIM_CMD)' && echo "Checking test log..." && sleep 2
endif

else #simulator is in remote machine

#build the software testbench
ifneq ($(TBTYPE),non)
ifneq ($(TBTYPE),V)
	ssh -t $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) 'make -C $(REMOTE_SW_DIR) tb'
endif
endif

ifeq ($(VCD),1)
	trap 'trap - INT TERM; scp $(SIM_SCP_FLAGS) $(SIM_USER)@$(SIM_SERVER):$(REMOTE_SIM_DIR)/*.vcd .' INT TERM EXIT;\
	ssh -t $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) 'make -j1 -C $(REMOTE_SIM_DIR) $@ SIMULATOR=$(SIMULATOR) $(UFLAGS)' || true
else
	ssh -t $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) 'make -j1 -C $(REMOTE_SIM_DIR) $@ SIMULATOR=$(SIMULATOR) $(UFLAGS)'
endif
	sleep 1 && sync && scp $(SIM_SCP_FLAGS) $(SIM_USER)@$(SIM_SERVER):$(REMOTE_SIM_DIR)/*.log .
ifeq ($(COV),1)
	sleep 1 && sync && scp -r $(SIM_SCP_FLAGS) $(SIM_USER)@$(SIM_SERVER):$(REMOTE_SIM_DIR)/cov_work .
	sleep 1 && sync && scp $(SIM_SCP_FLAGS) $(SIM_USER)@$(SIM_SERVER):$(REMOTE_SIM_DIR)/coverage_report_summary.rpt .
	sleep 1 && sync && scp $(SIM_SCP_FLAGS) $(SIM_USER)@$(SIM_SERVER):$(REMOTE_SIM_DIR)/coverage_report_detail.rpt .
endif
endif
ifeq ($(VCD),1)
	make waves
endif
else
	echo "Test passed!" > test.log
endif


waves:
	if [ ! "`pgrep -u $(USER) gtkwave`" ]; then gtkwave -a uut.gtkw uut.vcd; fi &

fix-vcd:
	$(eval VCD_FILE:=$(shell ls *.vcd))
	@tail -n 1 $(VCD_FILE) | wc -c | xargs -I {} truncate $(VCD_FILE) -s -{}
	@echo "" >> $(VCD_FILE)

gen-clean:
	@rm -f *.hex ../../software/tb
	@find . -maxdepth 1 -name "*.vh" -not \( -name "uut_build.mk" \) -delete
ifneq ($(SIM_SERVER),)
	ssh -t $(SIM_SSH_FLAGS) $(SIM_USER)@$(SIM_SERVER) 'if [ -f $(REMOTE_SIM_DIR)/Makefile ]; then make -C $(REMOTE_SIM_DIR) $@; fi'
endif


test: $(TEST_LIST)

debug:
	@echo NAME=$(NAME)
	@echo VHDR=$(VHDR)
	@echo VSRC=$(VSRC)
	@echo UFLAGS=$(UFLAGS)
	@echo VFLAGS=$(VFLAGS)

.PRECIOUS: uut.vcd test.log

.PHONY: build run waves gen-clean debug test $(TEST_LIST) fix-vcd remote_build_dir build_hex
