# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set PART xc7z010clg400-1
set_property part $PART [current_project]

if { ![file isdirectory "./ip"]} {
    file mkdir ./ip
}

# Create and configure Zynq PS
create_ip -name processing_system7 -vendor xilinx.com -library ip -version 5.5 -module_name processing_system7_0 -dir ./ip -force

set_property -dict [list \
    CONFIG.PCW_EN_CLK0_PORT {1} \
    CONFIG.PCW_EN_RST0_PORT {1} \
    CONFIG.PCW_USE_M_AXI_GP0 {0} \
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100.0}\
   ] [get_ips processing_system7_0]
#    CONFIG.PCW_USE_S_AXI_GP0 {1} \
generate_target all [get_files ./ip/processing_system7_0/processing_system7_0.xci]
synth_ip [get_files ./ip/processing_system7_0/processing_system7_0.xci]

