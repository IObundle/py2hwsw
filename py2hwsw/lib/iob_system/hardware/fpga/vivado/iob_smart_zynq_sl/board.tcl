# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set PART xc7z020clg484-1

# Create a temporary project for Zynq (required for BD)
if { [current_project -quiet] == "" } {
    create_project -force -part $PART iob_smart_zynq_sl ./iob_smart_zynq_sl
} else {
    set_property part $PART [current_project]
}

# Create Block Design with PS7
if { [get_files system.bd] == "" } {
    create_bd_design "system"
    create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

    # Configure PS with settings from smart_zynq_sl
    # (Note: These settings should match the ones in zynq_fpga_demo/scripts/build.tcl)
    set_property -dict [list \
        CONFIG.PCW_CRYSTAL_PERIPHERAL_FREQMHZ {33.333333} \
        CONFIG.PCW_UIPARAM_DDR_PARTNO {MT41K256M16 RE-125} \
        CONFIG.PCW_UIPARAM_DDR_BUS_WIDTH {16 Bit} \
        CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {50} \
        CONFIG.PCW_USE_M_AXI_GP0 {0} \
        CONFIG.PCW_USE_S_AXI_HP0 {1} \
        CONFIG.PCW_S_AXI_HP0_DATA_WIDTH {32} \
        CONFIG.PCW_QSPI_PERIPHERAL_ENABLE {1} \
        CONFIG.PCW_SD0_PERIPHERAL_ENABLE {1} \
        CONFIG.PCW_UART0_PERIPHERAL_ENABLE {1} \
        CONFIG.PCW_UART0_UART0_IO {EMIO} \
        CONFIG.PCW_GPIO_EMIO_GPIO_WIDTH {4} \
        CONFIG.PCW_GPIO_EMIO_GPIO_ENABLE {1} \
    ] [get_bd_cells processing_system7_0]

    # Expose interfaces and ports
    make_bd_intf_pins_external [get_bd_intf_pins processing_system7_0/DDR]
    make_bd_intf_pins_external [get_bd_intf_pins processing_system7_0/FIXED_IO]
    make_bd_pins_external [get_bd_pins processing_system7_0/FCLK_CLK0]
    make_bd_pins_external [get_bd_pins processing_system7_0/FCLK_RESET0_N]
    make_bd_pins_external [get_bd_pins processing_system7_0/GPIO_O]
    make_bd_pins_external [get_bd_pins processing_system7_0/GPIO_I]
    make_bd_pins_external [get_bd_pins processing_system7_0/UART0_RX]
    make_bd_pins_external [get_bd_pins processing_system7_0/UART0_TX]

    # Add AXI HP0 connections if needed, or just let the top module handle them
    # In this generic setup, we'll expose the S_AXI_HP0 port
    make_bd_intf_pins_external [get_bd_intf_pins processing_system7_0/S_AXI_HP0]
    connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins processing_system7_0/S_AXI_HP0_ACLK]

    # Assign address segment for HP0
    assign_bd_address [get_bd_addr_segs {processing_system7_0/S_AXI_HP0/HP0_DDR_LOWOCM }]

    # Rename ports to match what's expected in the top module wrapper
    set_property name DDR [get_bd_intf_ports DDR_0]
    set_property name FIXED_IO [get_bd_intf_ports FIXED_IO_0]
    set_property name FCLK_CLK0 [get_bd_ports FCLK_CLK0_0]
    set_property name FCLK_RESET0_N [get_bd_ports FCLK_RESET0_N_0]
    set_property name S_AXI_HP0 [get_bd_intf_ports S_AXI_HP0_0]

    # Associate clock and set frequency for S_AXI_HP0
    set_property CONFIG.ASSOCIATED_BUSIF {S_AXI_HP0} [get_bd_ports FCLK_CLK0]
    set_property name GPIO_O [get_bd_ports GPIO_O_0]
    set_property name GPIO_I [get_bd_ports GPIO_I_0]
    set_property name UART0_RX [get_bd_ports UART0_RX_0]
    set_property name UART0_TX [get_bd_ports UART0_TX_0]

    validate_bd_design
    save_bd_design
    generate_target all [get_files system.bd]
    set wrapper_path [make_wrapper -files [get_files system.bd] -top]
    read_verilog $wrapper_path
}

if { $USE_ETHERNET > 0 } {
    read_verilog vivado/$BOARD/iob_xilinx_ibufg.v
    read_verilog vivado/$BOARD/iob_xilinx_oddr.v

    if {[file exists "vivado/$BOARD/iob_eth_dev.sdc"]} {
        read_xdc vivado/$BOARD/iob_eth_dev.sdc
    }
}

if {[file exists "vivado/$BOARD/auto_board.sdc"]} {
    read_xdc vivado/$BOARD/auto_board.sdc
}
