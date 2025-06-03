# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """Convert 'iob' subordinate port into manager port of specified type in 'manager_if' python parameter."""
    params = {
        # Type of interface for manager bus
        "manager_if": "iob",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "ADDR_W",
                "descr": "",
                "type": "P",
                "val": 1,
                "min": 1,
                "max": 32,
            },
            {
                "name": "DATA_W",
                "descr": "",
                "type": "P",
                "val": 32,
                "min": 1,
                "max": 32,
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "iob_clk"},
            },
            {
                "name": "iob_s",
                "descr": "Subordinate IOb interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "m_m",
                "descr": "Manager port",
                "signals": {
                    "type": params["manager_if"],
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
    }
    #
    # Blocks
    #
    if params["manager_if"] == "wb":
        # "Wishbone" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2wishbone",
                "instance_name": "iob_iob2wishbone_coverter",
                "instance_description": "Convert IOb port from subordinate port into Wishbone interface for manager port",
                "parameters": {
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "wb_m": "m_m",
                    "iob_s": "iob_s",
                },
            }
        )
    elif params["manager_if"] == "apb":
        # "APB" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2apb",
                "instance_name": "iob_iob2apb_coverter",
                "instance_description": "Convert IOb port from subordinate port into APB interface for manager port",
                "parameters": {
                    "APB_ADDR_W": "ADDR_W",
                    "APB_DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "apb_m": "m_m",
                    "iob_s": "iob_s",
                },
            }
        )
    elif params["manager_if"] == "axil":
        # "AXI_Lite" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axil",
                "instance_name": "iob_iob2axil_coverter",
                "instance_description": "Convert IOb port from subordinate port into AXI-Lite interface for manager port",
                "parameters": {
                    "AXIL_ADDR_W": "ADDR_W",
                    "AXIL_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axil_m": "m_m",
                    "iob_s": "iob_s",
                },
            }
        )
    elif params["manager_if"] == "axi":
        # "AXI" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axi",
                "instance_name": "iob_iob2axi_coverter",
                "instance_description": "Convert IOb port from subordinate port into AXI interface for manager port",
                "parameters": {
                    "ADDR_WIDTH": "ADDR_W",
                    "DATA_WIDTH": "DATA_W",
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axi_m": (
                        "m_m",
                        [
                            "axi_awlock_i[0]",
                            "axi_arlock_i[0]",
                        ],
                    ),
                    "iob_s": "iob_s",
                },
            }
        )
    #
    # Snippets
    #
    snippet_code = ""
    attributes_dict["snippets"] = []
    if params["manager_if"] == "iob":
        # "IOb" interface
        snippet_code += """
   // Directly connect subordinate IOb port to manager IOb port
   assign iob_valid_o = iob_valid_i;
   assign iob_addr_o = iob_addr_i;
   assign iob_wdata_o = iob_wdata_i;
   assign iob_wstrb_o = iob_wstrb_i;
   assign iob_rready_o = iob_rready_i;
   assign iob_rvalid_o = iob_rvalid_i;
   assign iob_rdata_o = iob_rdata_i;
   assign iob_ready_o = iob_ready_i;
"""
    attributes_dict["snippets"] += [
        {"verilog_code": snippet_code},
    ]

    return attributes_dict
