# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This file is copied to the root of the build directory and becomes the top Makefile.

SHELL:=bash

export SIMULATOR ?= icarus

include config_build.mk

SIM_DIR := hardware/simulation

#
# SIMULATE
#

sim-build:
	make -C $(SIM_DIR) -j1 build

sim-run:
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
# CLEAN
#

clean: sim-clean

.PHONY: sim-build sim-run sim-debug sim-clean \
	clean

