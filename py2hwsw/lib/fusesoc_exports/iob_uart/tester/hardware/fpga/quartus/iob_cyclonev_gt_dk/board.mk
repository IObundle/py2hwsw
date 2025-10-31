# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

BOARD_SERVER=$(CYC5_SERVER)
BOARD_USER=$(CYC5_USER)
BOARD_SERIAL_PORT=$(CYC5_SERIAL_PORT)

VSRC+=$(FPGA_TOOL)/$(BOARD)/iob_reset_sync.v

ifeq ($(USE_EXTMEM),1)
VSRC+=$(FPGA_TOOL)/$(BOARD)/alt_ddr3.qsys
endif
