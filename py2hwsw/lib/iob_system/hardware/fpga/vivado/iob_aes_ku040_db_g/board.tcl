# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

set PART xcku040-fbva676-1-c
set_property part $PART [current_project]

if { $USE_EXTMEM > 0 } {

    proc generate_subordinate_config_lines {num_subordinates} {
        for {set i 0} {$i < $num_subordinates} {incr i} {
            set subordinate_number [format "%02d" $i]
            set_property "CONFIG.S${subordinate_number}_AXI_IS_ACLK_ASYNC" 1 [get_ips axi_interconnect_0]
            set_property "CONFIG.S${subordinate_number}_AXI_READ_FIFO_DEPTH" 32 [get_ips axi_interconnect_0]
            set_property "CONFIG.S${subordinate_number}_AXI_WRITE_FIFO_DEPTH" 32 [get_ips axi_interconnect_0]
        }
    }

    read_verilog vivado/$BOARD/iob_xilinx_axi_interconnect.v

    if { ![file isdirectory "./ip"]} {
        file mkdir ./ip
    }

    #async interconnect MIG<->Cache
    if { [file isdirectory "./ip/axi_interconnect_0"] } {
        read_ip ./ip/axi_interconnect_0/axi_interconnect_0.xci
        report_property [get_files ./ip/axi_interconnect_0/axi_interconnect_0.xci]
    } else {

        create_ip -name axi_interconnect -vendor xilinx.com -library ip -version 1.7 -module_name axi_interconnect_0 -dir ./ip -force

        set_property CONFIG.NUM_SLAVE_PORTS 1 [get_ips axi_interconnect_0]
        set_property CONFIG.AXI_ADDR_WIDTH 28 [get_ips axi_interconnect_0]
        set_property CONFIG.ACLK_PERIOD 5000 [get_ips axi_interconnect_0]
        set_property CONFIG.INTERCONNECT_DATA_WIDTH 32 [get_ips axi_interconnect_0]
        set_property CONFIG.M00_AXI_IS_ACLK_ASYNC 1 [get_ips axi_interconnect_0]
        set_property CONFIG.M00_AXI_WRITE_FIFO_DEPTH 32 [get_ips axi_interconnect_0]
        set_property CONFIG.M00_AXI_READ_FIFO_DEPTH 32 [get_ips axi_interconnect_0]

        generate_subordinate_config_lines 1

        generate_target all [get_files ./ip/axi_interconnect_0/axi_interconnect_0.xci]

        report_property [get_ips axi_interconnect_0]
        report_property [get_files ./ip/axi_interconnect_0/axi_interconnect_0.xci]
        exec sed -i s/100/5/g ip/axi_interconnect_0/axi_interconnect_0_ooc.xdc
        synth_ip [get_files ./ip/axi_interconnect_0/axi_interconnect_0.xci]

    }

    read_verilog vivado/$BOARD/iob_xilinx_ddr4_ctrl.v


    if { [file isdirectory "./ip/ddr4_0"] } {
        read_ip ./ip/ddr4_0/ddr4_0.xci
        report_property [get_files ./ip/ddr4_0/ddr4_0.xci]
    } else {

        create_ip -name ddr4 -vendor xilinx.com -library ip -version 2.2 -module_name ddr4_0 -dir ./ip -force

        set_property -dict \
        [list \
             CONFIG.C0.DDR4_TimePeriod {1250} \
             CONFIG.C0.DDR4_InputClockPeriod {4000} \
             CONFIG.C0.DDR4_CLKOUT0_DIVIDE {5} \
             CONFIG.C0.DDR4_MemoryPart {EDY4016AABG-DR-F} \
             CONFIG.C0.DDR4_DataWidth {32} \
             CONFIG.C0.DDR4_AxiSelection {true} \
             CONFIG.C0.DDR4_CasLatency {11} \
             CONFIG.C0.DDR4_CasWriteLatency {11} \
             CONFIG.C0.DDR4_AxiDataWidth {32} \
             CONFIG.C0.DDR4_AxiAddressWidth {30} \
             CONFIG.ADDN_UI_CLKOUT1_FREQ_HZ {100} \
             CONFIG.C0.BANK_GROUP_WIDTH {1}] [get_ips ddr4_0]

        generate_target all [get_files ./ip/ddr4_0/ddr4_0.xci]

        report_property [get_ips ddr4_0]
        report_property [get_files ./ip/ddr4_0/ddr4_0.xci]

        synth_ip [get_files ./ip/ddr4_0/ddr4_0.xci]
    }

    read_xdc vivado/$BOARD/ddr.xdc

} else { # USE_EXTMEM == 0
    read_verilog vivado/$BOARD/iob_xilinx_clock_wizard.v
    read_verilog vivado/$BOARD/iob_clock_wizard.v
    read_verilog vivado/$BOARD/iob_reset_sync.v
}

if { $USE_ETHERNET > 0 } {
    read_verilog vivado/$BOARD/iob_xilinx_ibufg.v
    read_verilog vivado/$BOARD/iob_xilinx_oddre1.v

    read_xdc vivado/$BOARD/eth.sdc
}

if {[file exists "vivado/$BOARD/auto_board.sdc"]} {
    read_xdc vivado/$BOARD/auto_board.sdc
}
