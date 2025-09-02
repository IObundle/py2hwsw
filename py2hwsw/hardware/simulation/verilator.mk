# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# remote simulation server
SIM_SERVER=$(VLT_SERVER)
SIM_USER=$(VLT_USER)

# top level module name and simulation object
VTOP=iob_uut
SIM_OBJ=V$(VTOP)
SW_DIR=../../software/src

ifneq ($(wildcard $(SW_DIR)/$(NAME)_csrs.c),)
VLT_SRC ?= $(SW_DIR)/$(NAME)_csrs.c
endif

# filter out the verilog testbench
VSRC:=$(filter-out $(wildcard ./src/*_tb.v), $(VSRC)) $(SW_DIR)/iob_core_tb.c $(SW_DIR)/iob_vlt_tb.cpp $(VLT_SRC)

# include files
VLT_INCLUDES+=$(addprefix -I, ./src ../src ../../software/src)
# Note that cpp includes are one directory deeper than vlt includes
CPP_INCLUDES+=$(addprefix -I, ../src ../../src ../../../software/src)

VFLAGS+=$(VLT_INCLUDES) -CFLAGS "$(CPP_INCLUDES) -g"

# verilator  flags
VFLAGS+=--cc --exe --top-module $(VTOP) #compile to C++, alow user C/C++ code, and set top module
VFLAGS+=-Wno-lint --Wno-UNOPTFLAT
VFLAGS+=--no-timing
ifeq ($(VCD),1)
VFLAGS+=--trace -DVCD
endif

comp: $(VHDR) $(VSRC) $(COBJ)
	verilator $(VFLAGS) $(VSRC)
	cd ./obj_dir && make -f $(SIM_OBJ).mk

exec: comp
	./obj_dir/$(SIM_OBJ)

clean: gen-clean
	@rm -rf obj_dir

very-clean: clean

.PHONY: comp exec clean
