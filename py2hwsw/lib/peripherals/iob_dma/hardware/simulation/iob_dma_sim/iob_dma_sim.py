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
                "val": "5",
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
            "name": "dma_s",
            "descr": "Testbench dma csrs interface",
            "signals": {
                "type": "iob",
                "ADDR_W": 5,
            },
        },
    ]
    #
    # Wires
    #
    attributes_dict["wires"] = [
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
            "name": "dma_cbus",
            "descr": "Testbench uart csrs bus",
            "signals": {
                "type": params["csr_if"],
                "prefix": "internal_",
                "ADDR_W": 5 - 2,  # Does not include 2 LSBs
            },
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
            "core_name": "iob_dma",
            "instance_name": "dma_inst",
            "instance_description": f"Unit Under Test (UUT) DMA instance with '{params['csr_if']}' interface.",
            "parameters": {
                "DATA_W": "DATA_W",
                "ADDR_W": "ADDR_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "csr_if": params["csr_if"],
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst",
                "iob_csrs_cbus_s": "dma_cbus",
                "dma_input_io": "dma_axis_out",
                "dma_output_io": "dma_axis_in",
                "axi_m": "axi_dma_ram",
            },
        },
        # TODO: connect AXI RAM
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
                #         "{axi_araddr, 2'b0}",
                #         "{axi_awaddr, 2'b0}",
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
    if params["csr_if"] == "wb":
        # "Wishbone" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2wishbone",
                "instance_name": "iob_iob2wishbone_coverter",
                "instance_description": "Convert IOb port from testbench into Wishbone interface for DMA CSRs bus",
                "parameters": {
                    "ADDR_W": 5 - 2,
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "wb_m": "dma_cbus",
                    "iob_s": (
                        "dma_s",
                        [
                            "iob_addr_i[5-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "apb":
        # "APB" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2apb",
                "instance_name": "iob_iob2apb_coverter",
                "instance_description": "Convert IOb port from testbench into APB interface for DMA CSRs bus",
                "parameters": {
                    "APB_ADDR_W": 5 - 2,
                    "APB_DATA_W": "DATA_W",
                    "ADDR_W": 5 - 2,
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "apb_m": "dma_cbus",
                    "iob_s": (
                        "dma_s",
                        [
                            "iob_addr_i[5-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "axil":
        # "AXI_Lite" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axil",
                "instance_name": "iob_iob2axil_coverter",
                "instance_description": "Convert IOb port from testbench into AXI-Lite interface for DMA CSRs bus",
                "parameters": {
                    "AXIL_ADDR_W": 5 - 2,
                    "AXIL_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axil_m": "dma_cbus",
                    "iob_s": (
                        "dma_s",
                        [
                            "iob_addr_i[5-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "axi":
        # "AXI" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axi",
                "instance_name": "iob_iob2axi_coverter",
                "instance_description": "Convert IOb port from testbench into AXI interface for DMA CSRs bus",
                "parameters": {
                    "ADDR_WIDTH": 5 - 2,
                    "DATA_WIDTH": "DATA_W",
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axi_m": (
                        "dma_cbus",
                        [
                            "axi_awlock_i[0]",
                            "axi_arlock_i[0]",
                        ],
                    ),
                    "iob_s": (
                        "dma_s",
                        [
                            "iob_addr_i[5-1:2]",
                        ],
                    ),
                },
            }
        )
    #
    # Snippets
    #
    attributes_dict["snippets"] = []
    snippet_code = """ """
    if params["csr_if"] == "iob":
        snippet_code += """
   // Directly connect cbus IOb port to internal IOb wires
   assign internal_iob_valid = iob_valid_i;
   assign internal_iob_addr = iob_addr_i[5-1:2]; // Ignore 2 LSBs
   assign internal_iob_wdata = iob_wdata_i;
   assign internal_iob_wstrb = iob_wstrb_i;
   assign internal_iob_rready = iob_rready_i;
   assign iob_rvalid_o = internal_iob_rvalid;
   assign iob_rdata_o = internal_iob_rdata;
   assign iob_ready_o = internal_iob_ready;
"""
    attributes_dict["snippets"] += [
        {"verilog_code": snippet_code},
    ]

    return attributes_dict
