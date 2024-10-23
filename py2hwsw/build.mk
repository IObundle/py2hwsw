# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# This file is copied to the root of the build directory and becomes the top Makefile.

SHELL:=bash

export SIMULATOR ?= icarus
export SYNTHESIZER ?= yosys
export BOARD ?= cyclonev_gt_dk

include config_build.mk

BSP_H ?= software/src/bsp.h
SIM_DIR := hardware/simulation
BOARD_DIR := $(shell find -name $(BOARD) -type d -print -quit)

#
# Create bsp.h from bsp.vh
#

ifeq (fpga,$(findstring fpga,$(MAKECMDGOALS)))
  USE_FPGA = 1
endif

ifeq ($(USE_FPGA),1)
BSP_VH = $(BOARD_DIR)/bsp.vh
else
BSP_VH = $(SIM_DIR)/src/bsp.vh
endif

BOARD_UPPER=$(shell echo $(BOARD) | tr '[:lower:]' '[:upper:]')

$(BSP_VH):
ifeq ($(USE_FPGA),1)
	@echo "Creating $(BSP_VH) for FPGA"
	cp $(BOARD_DIR)/$(BOARD)_conf.vh $@;
	sed -i 's/ $(BOARD_UPPER)_/ /g' $@;
else
	@echo "Creating $(BSP_VH) for simulation"
	cp $(SIM_DIR)/src/iob_sim_conf.vh $@;
	sed -i 's/ IOB_SIM_/ /g' $@;
endif

$(BSP_H): $(BSP_VH)
	cp $(BSP_VH) $@;
	sed -i 's/`/#/' $@;
	sed -i 's/`//g' $@;


# 
# EMBEDDED SOFTWARE
#
SW_DIR=software
fw-build: $(BSP_H)
	make -C $(SW_DIR) build

fw-clean:
	if [ -f "$(SW_DIR)/Makefile" ]; then make -C $(SW_DIR) clean; fi

#this target is not the same as fw-build because bsp.h is build for FPGA when fw-build is called
#see $(BSP_H) target that uses $(MAKECMDGOALS) to check if fw-build is called for FPGA or simulation
fpga-fw-build: fw-build

#
# PC EMUL
#
pc-emul-build: fw-build
	make -C $(SW_DIR) build_emul

pc-emul-run: $(BSP_H)
	make -C $(SW_DIR) run_emul

pc-emul-test: $(BSP_H)
	make -C $(SW_DIR) test_emul

pc-emul-clean:
	if [ -f "$(SW_DIR)/Makefile" ]; then make -C $(SW_DIR) clean; fi


#
# LINT
#

LINTER ?= spyglass
LINT_DIR=hardware/lint
lint-run:
	make -C $(LINT_DIR) run

lint-clean:
	if [ -f "$(LINT_DIR)/Makefile" ]; then make -C $(LINT_DIR) clean; fi

lint-test:
	make lint-run LINTER=spyglass
	make lint-run LINTER=alint


#
# SIMULATE
#
sim-build: fw-build
	make -C $(SIM_DIR) -j1 build

sim-run: fw-build
	make -C $(SIM_DIR) -j1 run

sim-waves:
	make -C $(SIM_DIR) waves

sim-test:
	make -C $(SIM_DIR) test

sim-debug: 
	make -C $(SIM_DIR) debug

sim-clean:
	if [ -f "$(SIM_DIR)/Makefile" ]; then make -C $(SIM_DIR) clean; fi

sim-cov: sim-clean
	make -C $(SIM_DIR) -j1 run COV=1



#
# FPGA
#
FPGA_DIR=hardware/fpga
fpga-build:
	make -C $(FPGA_DIR) -j1 build

fpga-run:
	make -C $(FPGA_DIR) -j1 run

fpga-test:
	make -C $(FPGA_DIR) test

fpga-debug:
	echo "BOARD=$(BOARD)"
	make -C $(FPGA_DIR) debug

fpga-clean:
	if [ -f "$(FPGA_DIR)/Makefile" ]; then make -C $(FPGA_DIR) clean; fi

#
# SYN
#
SYN_DIR=hardware/syn
syn-build:
	make -C $(SYN_DIR) build

syn-clean:
	if [ -f "$(SYN_DIR)/Makefile" ]; then make -C $(SYN_DIR) clean; fi

syn-test: syn-clean syn-build

#
# DOCUMENT
#
DOC_DIR=document
doc-build: $(BSP_H)
	make -C $(DOC_DIR) build

doc-view: $(BSP_H)
	make -C $(DOC_DIR) view

doc-debug: 
	make -C $(DOC_DIR) debug

doc-clean:
	if [ -f "$(DOC_DIR)/Makefile" ]; then make -C $(DOC_DIR) clean; fi

ifneq ($(wildcard document/tsrc),)
doc-test: doc-clean
	make -C $(DOC_DIR) test
else
doc-test:
endif


#
# TEST
#
test: sim-test fpga-test doc-test

ptest: dtest lint-test sim-cov

dtest: test syn-test 



#
# CLEAN
#

clean: fw-clean pc-emul-clean lint-clean sim-clean fpga-clean syn-clean doc-clean
	rm -f $(BSP_H)


.PHONY: fw-build fpga-fw-build fw-clean \
	pc-emul-build pc-emul-run pc-emul-clean \
	lint-test lint-run lint-clean \
	sim-build sim-run sim-debug sim-clean \
	fpga-build fpga-debug fpga-clean \
	doc-build doc-view doc-debug doc-test doc-clean \
	test clean debug

