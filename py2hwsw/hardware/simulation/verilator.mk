# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

CSRC = $(wildcard ./src/*.c)
OBJSRC = $(CSRC:.c=.o)

UFLAGS+=VERILATOR=$(VERILATOR)
VSRC:=$(filter-out $(wildcard ./src/*_tb.v), $(VSRC)) $(OBJSRC)
VSRC+=$(wildcard ./src/*_tb.cpp)


VTOP?=$(NAME)

VFLAGS+=--cc --exe -I. -I../src -I../common_src -Isrc --top-module $(VTOP)
VFLAGS+=$(addprefix -I,$(INCLUDE_DIRS))
VFLAGS+=-Wno-lint --Wno-UNOPTFLAT
VFLAGS+=--no-timing
# Include embedded headers
VFLAGS+=-CFLAGS "-I../../../software/src -I../../../software/include -I../../../software"

ifeq ($(VCD),1)
VFLAGS+=--trace
VFLAGS+=-DVCD -CFLAGS "-DVCD"
endif

ifneq ($(VTHREADS),)
VFLAGS+=--threads $(VTHREADS)
# Setup multi-threading optimizations according to:
# https://verilator.org/guide/latest/verilating.html
V_MULTI_THREAD_STR:=numactl -m 0 -C $(shell seq -s, 0 $$(($(VTHREADS)-1)) ) --
endif

SIM_SERVER=$(VSIM_SERVER)
SIM_USER=$(VSIM_USER)

SIM_OBJ=V$(VTOP)

%.o: %.c
	gcc -I../../       -I../../software/src -c -o $@ $<

comp: $(VHDR) $(VSRC) $(HEX)
	verilator $(VFLAGS) $(VSRC)
	cd ./obj_dir && make -f $(SIM_OBJ).mk

exec: comp
	$(V_MULTI_THREAD_STR) ./obj_dir/$(SIM_OBJ)

clean: gen-clean
	@rm -rf obj_dir

very-clean: clean

.PHONY: comp exec clean
