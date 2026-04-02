# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

BOARD_SERVER=$(Z7_SERVER)
BOARD_USER=$(Z7_USER)
BOARD_SERIAL_PORT=$(Z7_SERIAL_PORT)

FPGA_PROG = xsct vivado/zynq_prog.tcl $(FPGA_TOP) $(BOARD_DEVICE_ID) $(BOARD)
