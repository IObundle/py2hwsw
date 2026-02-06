# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# (c) 2022-Present IObundle, Lda, all rights reserved
#
# This makefile simulates the hardware modules in this repo
#

BUILD_DIR ?=build
BOARD ?= iob_aes_ku040_db_g
#BOARD_SERIAL_PORT ?= /dev/ttyUSB1

# Used by test.sh
LIB_DIR:=.
export LIB_DIR

# Default lib module to setup. Can be overriden by the user.
CORE ?=iob_ctls

CSR_IF?=iob

# Fill PY_PARAMS
ifneq ($(CSR_IF),)
PY_PARAMS:=$(PY_PARAMS):csr_if=$(CSR_IF)
endif
# IOb-System parameters
ifneq ($(INIT_MEM),)
PY_PARAMS:=$(PY_PARAMS):init_mem=$(INIT_MEM)
endif
ifneq ($(USE_INTMEM),)
PY_PARAMS:=$(PY_PARAMS):use_intmem=$(USE_INTMEM)
endif
ifneq ($(USE_EXTMEM),)
PY_PARAMS:=$(PY_PARAMS):use_extmem=$(USE_EXTMEM)
endif
ifneq ($(USE_ETHERNET),)
PY_PARAMS:=$(PY_PARAMS):use_ethernet=$(USE_ETHERNET)
endif
ifneq ($(MEM_ADDR_W),)
PY_PARAMS:=$(PY_PARAMS):mem_addr_w=$(MEM_ADDR_W)
endif
ifneq ($(FW_ADDR_W),)
PY_PARAMS:=$(PY_PARAMS):fw_addr_w=$(FW_ADDR_W)
endif
ifneq ($(CPU),)
PY_PARAMS:=$(PY_PARAMS):cpu=$(CPU)
endif
# Remove first char (:) from PY_PARAMS
PY_PARAMS:=$(shell echo $(PY_PARAMS) | cut -c2-)

# List of lib cores that pass linter checks. This list will be deprecated when all lib cores pass linter checks.
CORES_READY_FOR_LINT=iob_pulse_gen iob_and iob_aoi iob_timer iob_uart

# Get the name of the generated core (sometimes not equal to $(CORE), like the generated 'iob_cache_axi' of the iob_cache core)
CORE_NAME=$(shell nix-shell --run "py2hwsw $(CORE) print_core_name --py_params '$(PY_PARAMS)'")
VERSION=$(shell nix-shell --run "py2hwsw $(CORE) print_core_version --py_params '$(PY_PARAMS)'")

# Check if $(CORE) is in $(CORES_READY_FOR_LINT)
ifeq ($(filter $(CORE),$(CORES_READY_FOR_LINT)),)
SETUP_ARGS =--no_verilog_lint 
endif

all: sim-test

setup:
	nix-shell --run "py2hwsw $(CORE) setup --build_dir '$(BUILD_DIR)' --py_params '$(PY_PARAMS)' $(SETUP_ARGS)"

sim-build:
	nix-shell --run "scripts/test.sh build $(CORE)"

sim-run:
	nix-shell --run "VCD=$(VCD) scripts/test.sh $(CORE)"

sim-test:
	nix-shell --run "scripts/test.sh test"

sim-clean:
	nix-shell --run "scripts/test.sh clean"

fpga-build:
	nix-shell --run "make clean setup && make -C $(BUILD_DIR) fpga-sw-build BOARD=$(BOARD)" && make -C $(BUILD_DIR)/ fpga-build BOARD=$(BOARD)

fpga-run: fpga-build
	make -C $(BUILD_DIR)/ fpga-run BOARD=$(BOARD)


doc-build: 
	nix-shell --run "make clean setup && make -C $(BUILD_DIR) doc-build"

py2-doc-build:
	nix-shell --run "py2hwsw --py2hwsw_docs && make -C py2hwsw_generated_docs/document/ build"

py2-doc-update:
	cp py2hwsw_generated_docs/document/ug.pdf ../py2hwsw_document/document/ug.pdf


delivery:
	nix-shell --run "py2hwsw $(CORE) deliver --build_dir '$(BUILD_DIR)'"

fusesoc-export: clean setup
	nix-shell --run "py2hwsw $(CORE) export_fusesoc --build_dir '$(BUILD_DIR)' --py_params '$(PY_PARAMS)'"

fusesoc-test: fusesoc-export
	rm -rf fusesoc_test
	mkdir -p fusesoc_test/fusesoc_libraries
	ln -s ../../fusesoc_exports fusesoc_test/fusesoc_libraries/py2hwsw
	printf "[library.py2]\nlocation = fusesoc_libraries/py2hwsw\n" > fusesoc_test/fusesoc.conf
	nix-shell --run "cd fusesoc_test && fusesoc run --target=sim iobundle:py2hwsw:$(CORE_NAME)"

define MULTILINE_TEXT
provider:
  name: url
  url: https://github.com/IObundle/py2hwsw/releases/latest/download/$(CORE)_V$(VERSION).tar.gz
  filetype: tar
endef

# Generate independent fusesoc .core file. FuseSoC will obtain the Verilog sources from remote url with a pre-built build directory.
export MULTILINE_TEXT
fusesoc-core-file: fusesoc-export
	cp fusesoc_exports/$(CORE_NAME).core .
	# Append provider remote url to .core file
	printf "\n%s\n" "$$MULTILINE_TEXT" >> $(CORE_NAME).core
	echo "Generated independent $(CORE_NAME).core file."


lib-ipxact:
	nix-shell --run "py2hwsw --browse"
	./scripts/kactus2/import_library.py `realpath $(CURDIR)`/ipxact_lib
	nix-shell --run "kactus2"


.PHONY: all setup sim-build sim-run sim-test sim-clean fpga-build fpga-clean doc-build py2-doc-build py2-doc-update delivery fusesoc-export fusesoc-test fusesoc-core-file lib-ipxact


# Install board server and client
board_server_install:
	sudo cp ../scripts/board_server.py /usr/local/bin/ && \
        sudo cp ../scripts/board_server.service /etc/systemd/system/ && \
        sudo systemctl daemon-reload && \
	sudo systemctl enable board_server && \
	sudo systemctl restart board_server

board_server_uninstall:
	sudo systemctl stop board_server && \
        sudo systemctl disable board_server && \
        sudo rm /usr/local/bin/board_server.py && \
        sudo rm /etc/systemd/system/board_server.service && \
        sudo systemctl daemon-reload

board_server_status:
	sudo systemctl status board_server

.PHONY: board_server_install board_server_uninstall board_server_status


clean:
	nix-shell --run "py2hwsw $(CORE) clean --build_dir '$(BUILD_DIR)'"
	@rm -rf ../*.summary ../*.rpt py2hwsw_generated_docs fusesoc_exports fusesoc_test *.core
	@find . -name \*~ -delete

.PHONY: clean

# Release Artifacts

release-artifacts:
	make fusesoc-export CORE=iob_uart
	VERSION=`grep 'name:' fusesoc_exports/iob_uart.core | tr ':' '\n' | tail -1 | xargs`;\
	[ -n "$$VERSION" ] || { echo "Error: Could not extract version"; exit 1; };\
	tar -czf iob_uart_V$$VERSION.tar.gz -C ./fusesoc_exports .

.PHONY: release-artifacts

#
# Linux targets
#

# Regenerate timer userspace driver binaries and recompile buildroot of iob_system_linux
LINUX_SUBMODULE_DIR=iob_system/iob_system_linux/submodules/iob_linux
#SOC_LINUX_BUILD_DIR=../../../soc_linux_V0.8
buildroot-update:
	# Generate $(CORE)
	make clean setup CORE=$(CORE) BUILD_DIR=$(BUILD_DIR)
	# Compile userspace binaries
	nix-shell $(LINUX_SUBMODULE_DIR) --run 'make -C $(BUILD_DIR)/software/linux/user all'
	# Copy driver binaries to iob_system_linux buildroot
	for file in "$(CORE)_user_sysfs" "$(CORE)_user_dev" "$(CORE)_user_ioctl" "$(CORE)_tests_sysfs" "$(CORE)_tests_dev" "$(CORE)_tests_ioctl"; do\
		cp $(BUILD_DIR)/software/linux/user/$$file iob_system/iob_system_linux/software/buildroot/board/IObundle/iob-soc/rootfs-overlay/root/;\
	done
	# Compile kernel driver
	nix-shell $(LINUX_SUBMODULE_DIR) --run 'make -C $(LINUX_SUBMODULE_DIR) build-linux-drivers MODULE_NAME=$(CORE) MODULE_DRIVER_DIR=../../../../$(BUILD_DIR)/software/linux/drivers ROOTFS_OVERLAY_DIR=../../software/buildroot/board/IObundle/iob-soc/rootfs-overlay/drivers'
	# Copy iob_system_linux buildroot to iob_linux
	cp -r iob_system/iob_system_linux/software/buildroot/* $(LINUX_SUBMODULE_DIR)/software/buildroot/;
	# Recompile buildroot
	nix-shell $(LINUX_SUBMODULE_DIR) --run 'make -C $(LINUX_SUBMODULE_DIR) build-buildroot'
	# Copy rootfs to iob_system_linux
	cp $(LINUX_SUBMODULE_DIR)/software/OS_build/rootfs.cpio.gz iob_system/iob_system_linux/software/src/rootfs.cpio.gz
ifneq (SOC_LINUX_BUILD_DIR,)
	# Copy it to existing soc_linux build dir. Re-running soc_linux on fpga without rebuilding, will cause it to upload this new version of rootfs.
	cp iob_system/iob_system_linux/software/src/rootfs.cpio.gz $(SOC_LINUX_BUILD_DIR)/hardware/fpga/rootfs.cpio.gz
endif

.PHONY: buildroot-update

# Find board directoy in py2hwsw/hardware/fpga
BOARD_DIR := $(shell find ../hardware/fpga -name $(BOARD) -type d -print -quit)
# Include board.mk to set BOARD_USER, BOARD_SERVER, and BOARD_SERIAL_PORT
ifneq ($(BOARD_DIR),)
include $(BOARD_DIR)/board.mk
endif
#
ifneq ($(BOARD_SERVER),)
SSH_START=ssh $(BOARD_USER)@$(BOARD_SERVER) '
SSH_END='
REMOTE_BUILD_DIR?=$(BOARD_USER)/$(notdir $(BUILD_DIR))
else
REMOTE_BUILD_DIR=$(BUILD_DIR)
endif
ifeq ($(BOARD_SERIAL_PORT),)
# Assume a serial port if not specified
BOARD_SERIAL_PORT=/dev/usb-uart
endif

running_system_upload:
	# Generate $(CORE)
	make clean setup CORE=$(CORE) BUILD_DIR=$(BUILD_DIR)
	# Compile userspace binaries
	nix-shell $(LINUX_SUBMODULE_DIR) --run 'make -C $(BUILD_DIR)/software/linux/user all'
	# Copy driver binaries to iob_system_linux buildroot
	for file in "$(CORE)_user_sysfs" "$(CORE)_user_dev" "$(CORE)_user_ioctl" "$(CORE)_tests_sysfs" "$(CORE)_tests_dev" "$(CORE)_tests_ioctl"; do\
		cp $(BUILD_DIR)/software/linux/user/$$file iob_system/iob_system_linux/software/buildroot/board/IObundle/iob-soc/rootfs-overlay/root/;\
	done
	# Compile kernel driver
	nix-shell $(LINUX_SUBMODULE_DIR) --run 'make -C $(LINUX_SUBMODULE_DIR) build-linux-drivers MODULE_NAME=$(CORE) MODULE_DRIVER_DIR=../../../../$(BUILD_DIR)/software/linux/drivers ROOTFS_OVERLAY_DIR=../../software/buildroot/board/IObundle/iob-soc/rootfs-overlay/drivers'
	# Copy built driver to build dir
	cp iob_system/iob_system_linux/software/buildroot/board/IObundle/iob-soc/rootfs-overlay/drivers/$(CORE).ko $(BUILD_DIR)/software/linux/drivers/
ifneq ($(BOARD_SERVER),)
	# Rsync build dir to remote machine
	rsync $(BOARD_SYNC_FLAGS) -avz --force --delete --exclude 'software/tb' $(BUILD_DIR)/ $(BOARD_USER)@$(BOARD_SERVER):$(REMOTE_BUILD_DIR)/
endif
	# Upload to running linux instance using lrzsz
	# NOTE: These commands dont use board_client.py to grab the FPGA board. May cause conflicts with shared FPGAs.
	# They dont grab the board, since its meant to be used with an already grabbed fpga running a linux instance.
	$(SSH_START) cd $(REMOTE_BUILD_DIR)/software/linux;\
	echo "rz -o /drivers" > $(BOARD_SERIAL_PORT) && sz -y drivers/$(CORE).ko < $(BOARD_SERIAL_PORT) > $(BOARD_SERIAL_PORT);\
	for file in "$(CORE)_user_sysfs" "$(CORE)_user_dev" "$(CORE)_user_ioctl" "$(CORE)_tests_sysfs" "$(CORE)_tests_dev" "$(CORE)_tests_ioctl"; do\
		echo "rz -o /root" > $(BOARD_SERIAL_PORT) && sz -y user/$$file < $(BOARD_SERIAL_PORT) > $(BOARD_SERIAL_PORT);\
	done;\
	echo "modprobe /drivers/$(CORE).ko" > $(BOARD_SERIAL_PORT) $(SSH_END)

.PHONY: running_system_upload
