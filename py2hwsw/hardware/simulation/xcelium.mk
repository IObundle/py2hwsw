# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

SIM_SERVER=$(CADENCE_SERVER)
SIM_USER=$(CADENCE_USER)
SIM_SSH_FLAGS=$(CADENCE_SSH_FLAGS)
SIM_SCP_FLAGS=$(CADENCE_SCP_FLAGS)
SIM_SYNC_FLAGS=$(CADENCE_SYNC_FLAGS)

COV_TEST?=test

SFLAGS = -errormax 15 -status -licqueue
EFLAGS = $(SFLAGS) -access +wc
ifeq ($(COV),1)
COV_SFLAGS= -covoverwrite -covtest $(COV_TEST)
COV_EFLAGS= -covdut $(NAME) -coverage A -covfile xcelium_cov_commands.ccf
endif

VFLAGS+=$(SFLAGS) -update -linedebug -sv -incdir .

ifneq ($(wildcard ../src),)
VFLAGS+=-incdir ../src
endif

ifneq ($(wildcard ../common_src),)
VFLAGS+=-incdir ../common_src
endif

ifneq ($(wildcard src),)
VFLAGS+=-incdir src
endif

ifneq ($(wildcard hardware/src),)
VFLAGS+=-incdir hardware/src
endif

VFLAGS+=$(addprefix -incdir ,$(INCLUDE_DIRS))

ifeq ($(VCD),1)
VFLAGS+=-define VCD
endif

ifeq ($(SYN),1)
VFLAGS+=-define SYN
endif

xmvlog.log: $(VHDR) $(VSRC) $(HEX)
ifeq ($(TBTYPE),UVM)
	xrun -compile -sv_lib uvm_dpi $(UVM_HOME)/src/dpi/uvm_dpi.cc -cdslib . +UVM_TESTNAME=iob_test
	xmvlog $(VFLAGS) -incdir $(UVM_HOME)/src +define+UVM  $(UVM_HOME)/src/uvm_pkg.sv $(VSRC)
else
	xmvlog $(VFLAGS) $(VSRC)
endif

xmelab.log : xmvlog.log xcelium.d/worklib
ifeq ($(TBTYPE),UVM)
	xmelab $(EFLAGS) $(COV_EFLAGS) worklib.iob_uvm_tb:module
else
	xmelab $(EFLAGS) $(COV_EFLAGS) worklib.iob_v_tb:module
endif

comp: xmelab.log

exec: comp
ifeq ($(TBTYPE),UVM)
	sync && sleep 2 && xmsim $(SFLAGS) -sv_lib ./xcelium.d/run.lnx8664.23.03.d/librun worklib.iob_uvm_tb:module
else
	sync && sleep 2 && xmsim $(SFLAGS) $(COV_SFLAGS) worklib.iob_v_tb:module
endif
ifeq ($(COV),1)
	ls -d cov_work/scope/* > all_ucd_file
	imc -execcmd "merge -runfile all_ucd_file -overwrite -out merge_all"
	imc -init iob_cov_waiver.tcl -exec xcelium_cov.tcl
endif

clean: gen-clean
	@rm -f xmelab.log  xmsim.log  xmvlog.log
	@rm -f iob_cov_waiver.vRefine

very-clean: clean
	@rm -rf cov_work *.log
	@rm -f coverage_report_summary.rpt coverage_report_detail.rpt


.PHONY: comp exec clean very-clean
