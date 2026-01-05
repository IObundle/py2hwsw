# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = {
        # Type of interface for CSR bus
        "csr_if": "iob",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "confs": [
            # DMA parameters
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "32",
            },
            {
                "name": "ADDR_W",
                "descr": "Address bus width",
                "type": "P",
                "val": "7",
            },
            # DMA External memory interface
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "14",
                "min": "1",
                "max": "32",
                "descr": "AXI address width",
            },
            {
                "name": "AXI_LEN_W",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "8",
                "descr": "AXI len width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
                "descr": "AXI data width",
            },
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "AXI ID width",
            },
            {
                "name": "WLEN_W",
                "type": "P",
                "val": "12",
                "min": "1",
                "max": "AXI_ADDR_W",
                "descr": "Write length width",
            },
            {
                "name": "RLEN_W",
                "type": "P",
                "val": "12",
                "min": "1",
                "max": "AXI_ADDR_W",
                "descr": "Read length width",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "iob_clk",
            },
        },
        {
            "name": "pbus_s",
            "descr": "Testbench dma sim wrapper csrs interface",
            "signals": {
                "type": "iob",
                "ADDR_W": 7,
            },
        },
    ]
    #
    # Wires
    #
    attributes_dict["wires"] = [
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
            "name": "axistream_out_csrs",
            "descr": "axistream_out CSRs interface",
            "signals": {
                "type": "iob",
                "prefix": "axistream_out_csrs_",
                "ADDR_W": 5,
            },
        },
        # Other
        {
            "name": "dma_csrs",
            "descr": "dma CSRs interface",
            "signals": {
                "type": "iob",
                "prefix": "dma_csrs_",
                "ADDR_W": 5,
            },
        },
        {
            "name": "axi_dma_ram",
            "descr": "DMA <-> AXI RAM connection wires",
            "signals": {
                "type": "axi",
                "ADDR_W": "AXI_ADDR_W",
            },
        },
        {
            "name": "clk",
            "descr": "Clock signal",
            "signals": [
                {"name": "clk_i"},
            ],
        },
        {
            "name": "rst",
            "descr": "Reset signal",
            "signals": [
                {"name": "arst_i"},
            ],
        },
        {
            "name": "dma_axis_out",
            "descr": "AXIS OUT <-> DMA connection wires",
            "signals": [
                {"name": "axis_out_tdata", "width": "AXI_DATA_W"},
                {"name": "axis_out_tvalid", "width": "1"},
                {"name": "axis_out_tready", "width": "1"},
            ],
        },
        {
            "name": "dma_axis_in",
            "descr": "AXIS IN <-> DMA connection wires",
            "signals": [
                {"name": "axis_in_tdata", "width": "AXI_DATA_W"},
                {"name": "axis_in_tvalid", "width": "1"},
                {"name": "axis_in_tready", "width": "1"},
            ],
        },
        {
            "name": "axi_ram_mem",
            "descr": "Connect axi_ram to 'iob_ram_t2p_be' memory",
            "signals": {
                "type": "ram_t2p_be",
                "ADDR_W": "AXI_ADDR_W - 2",
                "prefix": "ext_mem_",
            },
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_axistream_in",
            "instance_name": "axistream_in0",
            "instance_description": "AXIS IN test instrument",
            "parameters": {
                "ADDR_W": "(ADDR_W-2)",
                "DATA_W": "DATA_W",
                "TDATA_W": "DATA_W",
                "FIFO_ADDR_W": "AXI_ADDR_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "interrupt_o": "axistream_in_interrupt",
                "axistream_io": "axistream_in_axis",
                "sys_axis_io": "dma_axis_in",
                "csrs_cbus_s": "axistream_in_csrs",
            },
        },
        {
            "core_name": "iob_axistream_out",
            "instance_name": "axistream_out0",
            "instance_description": "AXIS OUT test instrument",
            "parameters": {
                "ADDR_W": "(ADDR_W-2)",
                "DATA_W": "DATA_W",
                "TDATA_W": "DATA_W",
                "FIFO_ADDR_W": "AXI_ADDR_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "interrupt_o": "axistream_out_interrupt",
                "axistream_io": "axistream_out_axis",
                "sys_axis_io": "dma_axis_out",
                "csrs_cbus_s": "axistream_out_csrs",
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
                "s_s": "pbus_s",
                "m_0_m": "axistream_in_csrs",
                "m_1_m": "axistream_out_csrs",
                "m_2_m": "dma_csrs",
            },
            "num_managers": 3,
            "addr_w": 7,
        },
        {
            "core_name": "iob_dma",
            "instance_name": "dma_inst",
            "instance_description": "Unit Under Test (UUT) DMA instance.",
            "parameters": {
                "DATA_W": "DATA_W",
                "ADDR_W": "(ADDR_W-2)",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "csr_if": "iob",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst",
                "csrs_cbus_s": "dma_csrs",
                "dma_input_io": "dma_axis_in",
                "dma_output_io": "dma_axis_out",
                "axi_m": "axi_dma_ram",
            },
        },
        {
            "core_name": "iob_axi_ram",
            "instance_name": "axi_ram_inst",
            "instance_description": "AXI RAM test instrument to connect to DMA",
            "parameters": {
                "ID_WIDTH": "AXI_ID_W",
                "ADDR_WIDTH": "AXI_ADDR_W",
                "DATA_WIDTH": "AXI_DATA_W",
            },
            "connect": {
                "clk_i": "clk",
                "rst_i": "rst",
                "axi_s": "axi_dma_ram",
                # "axi_s": (
                #     "axi",
                #     [
                #         "{1'b0, axi_arlock}",
                #         "{1'b0, axi_awlock}",
                #     ],
                # ),
                "external_mem_bus_m": "axi_ram_mem",
            },
        },
        {
            "core_name": "iob_ram_t2p_be",
            "instance_name": "iob_ram_t2p_be_inst",
            "instance_description": "AXI RAM external memory",
            "parameters": {
                "ADDR_W": "AXI_ADDR_W - 2",
                "DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "ram_t2p_be_s": "axi_ram_mem",
            },
        },
    ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = []
    snippet_code = """ """
    snippet_code += """
    assign axis_clk = clk_i;
    assign axis_cke = cke_i;
    assign axis_arst = arst_i;
"""
    attributes_dict["snippets"] += [
        {"verilog_code": snippet_code},
    ]

    return attributes_dict
