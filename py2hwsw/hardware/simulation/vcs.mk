# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

SIM_SERVER=$(SYNOPSYS_SERVER)
SIM_USER=$(SYNOPSYS_USER)
SIM_SSH_FLAGS=$(SYNOPSYS_SSH_FLAGS)
SIM_SCP_FLAGS=$(SYNOPSYS_SCP_FLAGS)
SIM_SYNC_FLAGS=$(SYNOPSYS_SYNC_FLAGS)

SIM_PROC=simv

SFLAGS=-nc -sverilog +incdir+. +incdir+../src +incdir+../common_src  +incdir+src $(VFLAGS)
SFLAGS+=$(addprefix +incdir+,$(INCLUDE_DIRS))
ifeq ($(VCD),1)
SFLAGS+=+define+VCD
endif

EFLAGS=-debug_access+nomemcbk+dmptf -licqueue -debug_region+cell -notice +bidir+1

#+lint=all

comp: $(VHDR) $(VSRC)
	vlogan $(SFLAGS) $(VSRC) && vcs $(EFLAGS) $(TB)

exec: comp
	./simv

clean: gen-clean
	@rm -f simv *.raw

very-clean:


.PHONY: comp exec clean very-clean
