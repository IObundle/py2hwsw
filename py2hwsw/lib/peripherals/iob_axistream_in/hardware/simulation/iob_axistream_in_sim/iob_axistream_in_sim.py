# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "board_list": [],
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "32",
                "max": "32",
                "descr": "CPU data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "10",
                "min": "NA",
                "max": "32",
                "descr": "Address bus width",
            },
            {
                "name": "AXIS_FIFO_ADDR_W",
                "type": "P",
                "val": "10",
                "min": "NA",
                "max": "32",
                "descr": "FIFO address width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "pbus_s",
                "descr": "Testbench peripherals CSRs interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": 6,
                },
            },
        ],
        "buses": [
            {
                "name": "split_reset",
                "descr": "Reset signal for iob_split components",
                "signals": [
                    {"name": "arst_i"},
                ],
            },
            # AXISTREAM IN
            {
                "name": "axistream_in_interrupt",
                "descr": "Interrupt signal",
                "signals": [
                    {
                        "name": "axistream_in_interrupt",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "axistream_in_axis",
                "descr": "AXI Stream interface signals",
                "signals": [
                    {
                        "name": "axis_clk",
                        "width": "1",
                        "descr": "Clock.",
                    },
                    {
                        "name": "axis_cke",
                        "width": "1",
                        "descr": "Clock enable",
                    },
                    {
                        "name": "axis_arst",
                        "width": "1",
                        "descr": "Asynchronous and active high reset.",
                    },
                    {
                        "name": "axis_tdata",
                        "width": "DATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "axis_tvalid",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axis_tready",
                        "width": "1",
                        "descr": "Ready.",
                    },
                    {
                        "name": "axis_tlast",
                        "width": "1",
                        "descr": "Last word.",
                    },
                ],
            },
            {
                "name": "axistream_in_sys_axis",
                "descr": "System AXI Stream interface.",
                "signals": [
                    {
                        "name": "axistream_in_sys_tdata",
                        "width": "DATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "axistream_in_sys_tvalid",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axistream_in_sys_tready",
                        "width": "1",
                        "descr": "Ready.",
                    },
                ],
            },
            {
                "name": "axistream_in_csrs",
                "descr": "axistream_in CSRs interface",
                "signals": {
                    "type": "iob",
                    "prefix": "axistream_in_csrs_",
                    "ADDR_W": 5,
                },
            },
            # AXISTREAM OUT
            {
                "name": "axistream_out_interrupt",
                "descr": "Interrupt signal",
                "signals": [
                    {
                        "name": "axistream_out_interrupt",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "axistream_out_axis",
                "descr": "AXI Stream interface signals",
                "signals": [
                    {
                        "name": "axis_clk",
                        "width": "1",
                        "descr": "Clock.",
                    },
                    {
                        "name": "axis_cke",
                        "width": "1",
                        "descr": "Clock enable",
                    },
                    {
                        "name": "axis_arst",
                        "width": "1",
                        "descr": "Asynchronous and active high reset.",
                    },
                    {
                        "name": "axis_tdata",
                        "width": "DATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "axis_tvalid",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axis_tready",
                        "width": "1",
                        "descr": "Ready.",
                    },
                    {
                        "name": "axis_tlast",
                        "width": "1",
                        "descr": "Last word.",
                    },
                ],
            },
            {
                "name": "axistream_out_sys_axis",
                "descr": "System AXI Stream interface.",
                "signals": [
                    {
                        "name": "axistream_out_sys_tdata",
                        "width": "DATA_W",
                        "descr": "Data.",
                    },
                    {
                        "name": "axistream_out_sys_tvalid",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axistream_out_sys_tready",
                        "width": "1",
                        "descr": "Ready.",
                    },
                ],
            },
            {
                "name": "axistream_out_csrs",
                "descr": "axistream_out CSRs interface",
                "signals": {
                    "type": "iob",
                    "prefix": "axistream_out_csrs_",
                    "ADDR_W": 5,
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_axistream_in",
                "instance_name": "axistream_in0",
                "instance_description": "Unit Under Test (UUT)",
                "parameters": {
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                    "TDATA_W": "DATA_W",
                    "FIFO_ADDR_W": "AXIS_FIFO_ADDR_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistream_in_interrupt",
                    "axistream_io": "axistream_in_axis",
                    "sys_axis_io": "axistream_in_sys_axis",
                    "iob_csrs_cbus_s": "axistream_in_csrs",
                },
            },
            {
                "core_name": "iob_axistream_out",
                "instance_name": "axistream_out0",
                "instance_description": "Unit Under Test (UUT)",
                "parameters": {
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                    "TDATA_W": "DATA_W",
                    "FIFO_ADDR_W": "AXIS_FIFO_ADDR_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistream_out_interrupt",
                    "axistream_io": "axistream_out_axis",
                    "sys_axis_io": "axistream_out_sys_axis",
                    "iob_csrs_cbus_s": "axistream_out_csrs",
                },
            },
            {
                "core_name": "iob_split",
                "name": "tb_pbus_split",
                "instance_name": "iob_pbus_split",
                "instance_description": "Split between testbench peripherals",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "split_reset",
                    "input_s": "pbus_s",
                    "output_0_m": "axistream_in_csrs",
                    "output_1_m": "axistream_out_csrs",
                },
                "num_outputs": 2,
                "addr_w": 6,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign axis_clk = clk_i;
    assign axis_cke = cke_i;
    assign axis_arst = arst_i;

    // Connect unused inputs to zero
    assign axistream_in_sys_tready = 1'b0;
    assign axistream_out_sys_tvalid = 1'b0;
    assign axistream_out_sys_tdata = {DATA_W{1'b0}};
""",
            },
        ],
    }

    return attributes_dict
