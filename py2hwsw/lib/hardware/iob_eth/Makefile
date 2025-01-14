export SIMULATOR ?= icarus
export BOARD ?= AES-KU040-DB-G
export NODE ?= umc130

#------------------------------------------------------------
# SETUP
#------------------------------------------------------------
CORE := iob_eth
LIB_DIR ?= ../IOBSOC/submodules/LIB

DISABLE_LINT:=1

PROJECT_ROOT := ..

TOP_MODULE_NAME :=iob_eth

include ../IOBSOC/submodules/LIB/setup.mk



BUILD_DIR = ../$(CORE)_V*

$(BUILD_DIR):
	nix-shell --run 'make build-setup SETUP_ARGS="$(SETUP_ARGS)"'


setup: $(BUILD_DIR)

.PHONY: setup


#------------------------------------------------------------
# SIMULATION
#------------------------------------------------------------

sim-build: clean
	nix-shell --run 'make clean setup'
	nix-shell --run "make -C $(BUILD_DIR)/ sim-build"

sim-run: clean
	nix-shell --run 'make clean setup'
	nix-shell --run "make -C $(BUILD_DIR)/ sim-run"

sim-waves:
	nix-shell --run "make -C $(BUILD_DIR)/ sim-waves"

sim-test: sim-run

.PNONY: sim-build sim-run sim-waves sim-test


#------------------------------------------------------------
# FPGA
#------------------------------------------------------------

VIVADO_TIMING_SUMMARY=$(BUILD_DIR)/hardware/fpga/reports/*timing_summary.rpt
VIVADO_UTILIZATION=$(BUILD_DIR)/hardware/fpga/reports/*utilization.rpt
VIVADO_LOG=$(BUILD_DIR)/hardware/fpga/reports/*vivado.log

QUARTUS_MAP=$(BUILD_DIR)/hardware/fpga/reports/*map.rpt
QUARTUS_FIT=$(BUILD_DIR)/hardware/fpga/reports/*fit.rpt
QUARTUS_STA=$(BUILD_DIR)/hardware/fpga/reports/*sta.rpt

QUARTUS_FIT_SUMMARY=$(BUILD_DIR)/hardware/fpga/reports/*fit.summary
QUARTUS_STA_SUMMARY=$(BUILD_DIR)/hardware/fpga/reports/*sta.summary

fpga-build:
ifeq ($(TESTER),1)
	nix-shell --run 'make -j1 clean setup TESTER=$(TESTER) N_PINS_W=$(N_PINS_W) CSR_IF=$(CSR_IF)'
	nix-shell --run 'make -j1 -C $(BUILD_DIR)/. fpga-fw-build BOARD=$(BOARD)'
	make -C $(BUILD_DIR)/ fpga-build BOARD=$(BOARD)
else
	nix-shell --run "make clean setup && make -C $(BUILD_DIR)/ fpga-build"
endif
	set -e; file=$(VIVADO_TIMING_SUMMARY); if [ -f  $(VIVADO_TIMING_SUMMARY) ]; then cp $(VIVADO_TIMING_SUMMARY) ..; fi
	set -e; if [ -f  $(VIVADO_UTILIZATION) ]; then cp $(VIVADO_UTILIZATION) ..; fi
	if [ -f $(VIVADO_LOG) ]; then  grep -i critical $(VIVADO_LOG); fi; sleep 0;
	set -e; if [ -f $(QUARTUS_STA_SUMMARY) ]; then cp $(QUARTUS_STA_SUMMARY) ..; fi
	set -e; if [ -f $(QUARTUS_FIT_SUMMARY) ]; then cp $(QUARTUS_FIT_SUMMARY) ..; fi
	if [ -f $(QUARTUS_MAP) ]; then  grep -i critical $(QUARTUS_MAP); fi; sleep 0;
	if [ -f $(QUARTUS_FIT) ]; then  grep -i critical $(QUARTUS_FIT); fi; sleep 0;
	if [ -f $(QUARTUS_STA) ]; then  grep -i critical $(QUARTUS_STA); fi; sleep 0;

fpga-run:
	nix-shell --run "make -C $(BUILD_DIR)/ fpga-run BOARD=$(BOARD)"



.PHONY: fpga-build fpga-test fpga-run



#------------------------------------------------------------
# DOCUMENT BUILD
#------------------------------------------------------------
doc-build: clean
	nix-shell --run "make setup && make -C $(BUILD_DIR)/ doc-build"
	xdg-open $(BUILD_DIR)/document/ug.pdf &

.PHONY: doc-build

# Create a virtual network interface
ETH_IF ?= eth10
virtual-network-if:
	su root -c "modprobe dummy;\
	ip link add $(ETH_IF) type dummy;\
	ifconfig $(ETH_IF) up"

remove-virtual-network-if:
	su root -c "ip link del $(ETH_IF);\
	rmmod dummy"

.PHONY: virtual-network-if remove-virtual-network-if
