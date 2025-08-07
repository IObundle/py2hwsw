# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

SIM_SERVER=$(QUESTA_SERVER)
SIM_USER=$(QUESTA_USER)
SIM_SSH_FLAGS=$(QUESTA_SSH_FLAGS)
SIM_SCP_FLAGS=$(QUESTA_SCP_FLAGS)
SIM_SYNC_FLAGS=$(QUESTA_SYNC_FLAGS)

SIM_PROC=vsim

CFLAGS = -quiet -sv +incdir+. +incdir+../src +incdir+../common_src  +incdir+src $(VFLAGS)
CFLAGS+=$(addprefix +incdir+,$(INCLUDE_DIRS))
SFLAGS = -voptargs="+acc" -c
ifeq ($(VCD),1)
CFLAGS+=+define+VCD
endif

comp: $(VHDR) $(VSRC) $(BUILD_DEPS)
	vlog $(CFLAGS) $(VSRC)

exec: comp
	vsim $(SFLAGS) $(NAME)_tb -do "run -all;quit"

clean: gen-clean
	@rm -f *.raw

very-clean:

.PHONY: comp exec clean very-clean
