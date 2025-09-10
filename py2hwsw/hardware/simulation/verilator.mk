# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# remote simulation server
SIM_SERVER=$(VLT_SERVER)
SIM_USER=$(VLT_USER)

# top level module name and simulation object
ifeq ($(TBTYPE),C)
VTOP=iob_uut
endif

ifeq ($(TBTYPE),V)
# get 1st match in ./src/*_tb.v files
# take filename without extention
VTOP=$(basename $(notdir $(firstword $(wildcard ./src/*_tb.v))))
# VTOP=$(patsubst %_tb,%,$(basename $(notdir $(firstword $(wildcard ./src/*_tb.v)))))
endif

SIM_OBJ=V$(VTOP)
SW_DIR=../../software/src

ifneq ($(wildcard $(SW_DIR)/$(NAME)_csrs.c),)
VLT_SRC ?= $(SW_DIR)/$(NAME)_csrs.c
endif

# filter out the verilog testbench
ifeq ($(TBTYPE),C)
VSRC:=$(filter-out $(wildcard ./src/*_tb.v), $(VSRC)) $(SW_DIR)/iob_core_tb.c $(SW_DIR)/iob_vlt_tb.cpp $(VLT_SRC)
endif

# include files
VLT_INCLUDES+=$(addprefix -I, ./src ../src ../../software/src)
# Note that cpp includes are one directory deeper than vlt includes
CPP_INCLUDES+=$(addprefix -I, ../src ../../src ../../../software/src)

VFLAGS+=$(VLT_INCLUDES) -CFLAGS "$(CPP_INCLUDES) -g"

# verilator  flags
VFLAGS+=--cc --exe --top-module $(VTOP) #compile to C++, alow user C/C++ code, and set top module
VFLAGS+=-Wno-lint --Wno-UNOPTFLAT
ifneq ($(TBTYPE),V)
VFLAGS+=--no-timing
else
VFLAGS+=--main
VFLAGS+=--timing
endif
ifeq ($(VCD),1)
VFLAGS+=--trace -DVCD
endif

ifeq ($(COV),1)
VFLAGS+=--coverage
COV_RPT=$(VTOP)_coverage.dat
COV_ARG=+verilator+coverage+file+$(COV_RPT)
COV_MERGE=merged.dat
endif

comp: $(VHDR) $(VSRC) $(COBJ)
	verilator $(VFLAGS) $(VSRC)
	cd ./obj_dir && make -f $(SIM_OBJ).mk

exec: comp
	./obj_dir/$(SIM_OBJ) $(COV_ARG)
ifeq ($(COV),1)
	make cov-analyze
endif

cov-analyze: $(COV_RPT)
	# merge coverage
	verilator_coverage --write $(COV_MERGE) $(COV_RPT)
	# annotate coverage
	# --annotate <dir>: create coverage annotations in <dir>.
	#  					Note: only shows modules with missing coverage
	# --annotate-min <count>: set minimum threshold for toggle for sufficient coverage
	# --annotate-all: write annotations for all modules, even if 100% covered
	# more info: https://verilator.org/guide/latest/exe_verilator_coverage.html
	verilator_coverage --annotate cov_annotated --annotate-min 2 --annotate-all $(COV_MERGE)

clean: gen-clean
	@rm -rf obj_dir
	@rm -rf *.dat cov_annotated # coverage outputs

very-clean: clean

.PHONY: comp exec clean cov-analyze
