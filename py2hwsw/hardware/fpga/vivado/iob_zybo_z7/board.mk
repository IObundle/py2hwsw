# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

BOARD_SERVER=$(Z7_SERVER)
BOARD_USER=$(Z7_USER)
BOARD_SERIAL_PORT=$(Z7_SERIAL_PORT)

FPGA_PROG = xsct vivado/zynq_prog.tcl $(FPGA_TOP) $(BOARD_DEVICE_ID) $(BOARD)

FPGA_EXTRA_DIRS = .gen
