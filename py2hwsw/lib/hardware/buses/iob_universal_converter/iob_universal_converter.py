# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """Universal converter. Convert interface of subordinate port into interface of manager port, based on interface types given in python parameters"""
    params = {
        # Type of interfaces
        "manager_if": "iob",
        "subordinate_if": "iob",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    # Set a default name for generated verilog if name was not provided by python parameters
    if "name" not in params:
        params["name"] = (
            f"iob_universal_converter_{params['subordinate_if']}_{params['manager_if']}"
        )

    attributes_dict = {
        "name": params["name"],
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
    }
    # Add AXI parameters if needed
    if params["subordinate_if"] == "axi" or params["manager_if"] == "axi":
        attributes_dict["confs"] += [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": 1,
                "min": 1,
                "max": 32,
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": 8,
                "min": 1,
                "max": 8,
            },
        ]
    #
    # Ports
    #
    attributes_dict["ports"] = []
    # IOb to IOb converter does not need clk interface
    if params["subordinate_if"] != "iob" or params["manager_if"] != "iob":
        attributes_dict["ports"].append(
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "iob_clk"},
            }
        )

    attributes_dict["ports"] += [
        {
            "name": "s_s",
            "descr": "Subordinate port",
            "signals": {
                "type": params["subordinate_if"],
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
    ]
    # Append ID_W and LEN_W when using AXI interfaces
    if params["subordinate_if"] == "axi":
        attributes_dict["ports"][-2]["signals"] |= {
            "ID_W": "AXI_ID_W",
            "LEN_W": "AXI_LEN_W",
        }
    if params["manager_if"] == "axi":
        attributes_dict["ports"][-1]["signals"] |= {
            "ID_W": "AXI_ID_W",
            "LEN_W": "AXI_LEN_W",
        }
    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "internal_iob",
            "descr": "Internal IOb wire",
            "signals": {
                "type": "iob",
                "ADDR_W": "ADDR_W",
                "DATA_W": "DATA_W",
            },
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = []
    # Subordinate interface converters
    if params["subordinate_if"] == "wb":
        # "Wishbone" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_wishbone2iob",
                "instance_name": "iob_wishbone2iob_converter",
                "instance_description": "Convert Wishbone from subordinate port into IOb interface for internal wire",
                "parameters": {
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "wb_s": "s_s",
                    "iob_m": "internal_iob",
                },
            }
        )
    elif params["subordinate_if"] == "apb":
        # "APB" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_apb2iob",
                "instance_name": "iob_apb2iob_converter",
                "instance_description": "Convert APB from subordinate port into IOb interface for internal wire",
                "parameters": {
                    "APB_ADDR_W": "ADDR_W",
                    "APB_DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "apb_s": "s_s",
                    "iob_m": "internal_iob",
                },
            }
        )
    elif params["subordinate_if"] == "axil":
        # "AXI_Lite" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_axil2iob",
                "instance_name": "iob_axil2iob_converter",
                "instance_description": "Convert AXI-Lite from subordinate port into IOb interface for internal wire",
                "parameters": {
                    "AXIL_ADDR_W": "ADDR_W",
                    "AXIL_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axil_s": "s_s",
                    "iob_m": "internal_iob",
                },
            }
        )
    elif params["subordinate_if"] == "axi":
        # "AXI" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_axi2iob",
                "instance_name": "iob_axi2iob_converter",
                "instance_description": "Convert AXI from subordinate port into IOb interface for internal wire",
                "parameters": {
                    "ADDR_WIDTH": "ADDR_W",
                    "DATA_WIDTH": "DATA_W",
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axi_s": (
                        "s_s",
                        [
                            "axi_awlock_i[0]",
                            "axi_arlock_i[0]",
                        ],
                    ),
                    "iob_m": "internal_iob",
                },
            }
        )
    # Manager interface converters
    if params["manager_if"] == "wb":
        # "Wishbone" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2wishbone",
                "instance_name": "iob_iob2wishbone_converter",
                "instance_description": "Convert IOb from internal wire into Wishbone interface for manager port",
                "parameters": {
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "internal_iob",
                    "wb_m": "m_m",
                },
            }
        )
    elif params["manager_if"] == "apb":
        # "APB" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2apb",
                "instance_name": "iob_iob2apb_converter",
                "instance_description": "Convert IOb from internal wire into APB interface for manager port",
                "parameters": {
                    "APB_ADDR_W": "ADDR_W",
                    "APB_DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "internal_iob",
                    "apb_m": "m_m",
                },
            }
        )
    elif params["manager_if"] == "axil":
        # "AXI_Lite" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axil",
                "instance_name": "iob_iob2axil_converter",
                "instance_description": "Convert IOb from internal wire into AXI-Lite interface for manager port",
                "parameters": {
                    "AXIL_ADDR_W": "ADDR_W",
                    "AXIL_DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "internal_iob",
                    "axil_m": "m_m",
                },
            }
        )
    elif params["manager_if"] == "axi":
        # "AXI" interface
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axi",
                "instance_name": "iob_iob2axi_converter",
                "instance_description": "Convert IOb from internal wire into AXI interface for manager port",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "internal_iob",
                    "axi_m": (
                        "m_m",
                        [
                            "axi_awlock_i[0]",
                            "axi_arlock_i[0]",
                        ],
                    ),
                },
            }
        )
    #
    # Snippets
    #
    snippet_code = ""
    attributes_dict["snippets"] = []
    if params["subordinate_if"] == "iob":
        # "IOb" interface
        snippet_code += """
   // Directly connect subordinate IOb port to intetnal IOb wire
   assign iob_valid = iob_valid_i;
   assign iob_addr = iob_addr_i;
   assign iob_wdata = iob_wdata_i;
   assign iob_wstrb = iob_wstrb_i;
   assign iob_rvalid_o = iob_rvalid;
   assign iob_rdata_o = iob_rdata;
   assign iob_ready_o = iob_ready;
"""
    if params["manager_if"] == "iob":
        # "IOb" interface
        snippet_code += """
   // Directly connect internal IOb wire to manager IOb port
   assign iob_valid_o = iob_valid;
   assign iob_addr_o = iob_addr;
   assign iob_wdata_o = iob_wdata;
   assign iob_wstrb_o = iob_wstrb;
   assign iob_rvalid = iob_rvalid_i;
   assign iob_rdata = iob_rdata_i;
   assign iob_ready = iob_ready_i;
"""
    attributes_dict["snippets"] += [
        {"verilog_code": snippet_code},
    ]

    return attributes_dict
