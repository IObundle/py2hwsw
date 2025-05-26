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
    CONFIG.PCW_USE_S_AXI_GP0 {1} \
    CONFIG.PCW_IRQ_F2P_INTR {1} \
    CONFIG.PCW_EN_CLK0_PORT {1} \
    CONFIG.PCW_EN_RST0_PORT {1} \
    CONFIG.PCW_PRESET_BANK0_VOLTAGE {LVCMOS33} \
    CONFIG.PCW_GPIO_EMIO_GPIO_ENABLE {0} \
    CONFIG.PCW_GPIO_MIO_GPIO_ENABLE {1} \
    CONFIG.PCW_GPIO_MIO_GPIO_IO {MIO} \
    CONFIG.PCW_UART0_PERIPHERAL_ENABLE {0} \
    CONFIG.PCW_UART1_PERIPHERAL_ENABLE {1} \
    CONFIG.PCW_UART1_UART1_IO {EMIO} \
] [get_ips processing_system7_0]

generate_target all [get_files ./ip/processing_system7_0/processing_system7_0.xci]

read_xdc ./ip/processing_system7_0/processing_system7_0.xdc

synth_ip [get_files ./ip/processing_system7_0/processing_system7_0.xci]

