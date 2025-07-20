# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["name"] = os.path.basename(__file__)

    # Each generated interconnect must have a unique name (can't have two verilog modules with same name).
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated axi interconnect module."
    )
    # Number of manager interfaces (number of managers to connect to)
    N_MANAGERS = (
        int(py_params_dict["num_managers"]) if "num_managers" in py_params_dict else 1
    )
    # Number of subordinate interfaces (number of managers to connect to)
    N_SUBORDINATES = (
        int(py_params_dict["num_subordinates"])
        if "num_subordinates" in py_params_dict
        else 1
    )

    # Number of bits required for manager interface selection (each output of split)
    M_SELECT_NBITS = (N_MANAGERS - 1).bit_length()
    # Number of bits required for subordinate interface selection (each input of merge)
    S_SELECT_NBITS = (N_SUBORDINATES - 1).bit_length()

    axi_iob_params = {
        "addr_w": 32,
        "data_w": 32,
        # "id_w": 1,
        "size_w": 3,
        "burst_w": 2,
        "lock_w": 2,
        "cache_w": 4,
        # "prot_w": 3,
        "qos_w": 4,
        "resp_w": 2,
        # "len_w": 8,
        "data_section_w": 8,
    }
    for param in axi_iob_params:
        if param in py_params_dict:
            axi_iob_params[param] = int(py_params_dict[param])

    # Same dictionary but with all keys in upper case
    AXI_IOB_PARAMS = {i.upper(): v for i, v in axi_iob_params.items()}

    axi_verilog_params = {
        "ID_W": 1,
        "LEN_W": 1,
    }
    # Dictionary maps verilog paramters to ones with same name of interconnect
    AXI_VERILOG_PARAMS_MAP = {i: i for i in axi_verilog_params}

    # Address width for merge output
    # This width is equal to width of internal buses plus the merge input selection bits (that will be later ignored)
    MERGE_OUTPUT_WIDTH = axi_iob_params["addr_w"] - M_SELECT_NBITS + S_SELECT_NBITS

    axi_wires = [
        # AXI-Lite Write
        ("axi_awaddr", "input", axi_iob_params["addr_w"], "write"),
        # ("axi_awprot", "input", axi_iob_params["prot_w"], "write"),
        ("axi_awvalid", "input", 1, "write"),
        ("axi_awready", "output", 1, "write"),
        ("axi_wdata", "input", axi_iob_params["data_w"], "write"),
        (
            "axi_wstrb",
            "input",
            int(axi_iob_params["data_w"] / axi_iob_params["data_section_w"]),
            "write",
        ),
        ("axi_wvalid", "input", 1, "write"),
        ("axi_wready", "output", 1, "write"),
        ("axi_bresp", "output", axi_iob_params["resp_w"], "write"),
        ("axi_bvalid", "output", 1, "write"),
        ("axi_bready", "input", 1, "write"),
        # AXI specific write
        ("axi_awid", "input", "ID_W", "write"),
        ("axi_awlen", "input", "LEN_W", "write"),
        ("axi_awsize", "input", axi_iob_params["size_w"], "write"),
        ("axi_awburst", "input", axi_iob_params["burst_w"], "write"),
        ("axi_awlock", "input", axi_iob_params["lock_w"], "write"),
        ("axi_awcache", "input", axi_iob_params["cache_w"], "write"),
        ("axi_awqos", "input", axi_iob_params["qos_w"], "write"),
        ("axi_wlast", "input", 1, "write"),
        ("axi_bid", "output", "ID_W", "write"),
        # AXI-Lite Read
        ("axi_araddr", "input", axi_iob_params["addr_w"], "read"),
        # ("axi_arprot", "input", axi_iob_params["prot_w"], "read"),
        ("axi_arvalid", "input", 1, "read"),
        ("axi_arready", "output", 1, "read"),
        ("axi_rdata", "output", axi_iob_params["data_w"], "read"),
        ("axi_rresp", "output", axi_iob_params["resp_w"], "read"),
        ("axi_rvalid", "output", 1, "read"),
        ("axi_rready", "input", 1, "read"),
        # AXI specific read
        ("axi_arid", "input", "ID_W", "read"),
        ("axi_arlen", "input", "LEN_W", "read"),
        ("axi_arsize", "input", axi_iob_params["size_w"], "read"),
        ("axi_arburst", "input", axi_iob_params["burst_w"], "read"),
        ("axi_arlock", "input", axi_iob_params["lock_w"], "read"),
        ("axi_arcache", "input", axi_iob_params["cache_w"], "read"),
        ("axi_arqos", "input", axi_iob_params["qos_w"], "read"),
        ("axi_rid", "output", "ID_W", "read"),
        ("axi_rlast", "output", 1, "read"),
    ]

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
    }
    #
    # Confs
    #
    attributes_dict["confs"] = []
    for param, default_val in axi_verilog_params.items():
        attributes_dict["confs"].append(
            {
                "name": param,
                "type": "P",
                "val": default_val,
                "min": "0",
                "max": "32",
                "descr": f"AXI {param[:-2]} bus width",
            }
        )
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "wires": {
                "type": "iob_clk",
            },
            "descr": "Clock, clock enable and async reset",
        },
        {
            "name": "rst_i",
            "descr": "Synchronous reset",
            "wires": [
                {
                    "name": "rst_i",
                    "width": 1,
                },
            ],
        },
    ]
    for i in range(N_MANAGERS):
        attributes_dict["ports"].append(
            {
                "name": f"m{i}_axi_m",
                "descr": f"Manager {i} interface",
                "wires": {
                    "type": "axi",
                    "prefix": f"m{i}_",
                    **AXI_VERILOG_PARAMS_MAP,
                    **AXI_IOB_PARAMS,
                },
            }
        )
    for i in range(N_SUBORDINATES):
        attributes_dict["ports"].append(
            {
                "name": f"s{i}_axi_s",
                "descr": f"Subordinate {i} interface",
                "wires": {
                    "type": "axi",
                    "prefix": f"s{i}_",
                    **AXI_VERILOG_PARAMS_MAP,
                    **AXI_IOB_PARAMS,
                },
            }
        )
    #
    # Buses
    #
    attributes_dict["buses"] = []
    for i in range(N_SUBORDINATES):
        for j in range(N_MANAGERS):
            attributes_dict["buses"].append(
                {
                    "name": f"connect_s{i}_m{j}",
                    "descr": f"Connect split of subordinate {i} to merge of manager {j}",
                    "wires": {
                        "type": "axi",
                        "prefix": f"s{i}_m{j}_",
                        **AXI_VERILOG_PARAMS_MAP,
                        **AXI_IOB_PARAMS,
                    }
                    | {"ADDR_W": axi_iob_params["addr_w"] - M_SELECT_NBITS},
                }
            )
    # Buses for output for merges
    for i in range(N_MANAGERS):
        attributes_dict["buses"].append(
            {
                "name": f"merge_{i}_output",
                "descr": f"Output of merge {i}",
                "wires": {
                    "type": "axi",
                    "prefix": f"merge_{i}_",
                    **AXI_VERILOG_PARAMS_MAP,
                    **AXI_IOB_PARAMS,
                }
                | {"ADDR_W": MERGE_OUTPUT_WIDTH},
            }
        )
    #
    # Blocks
    #
    attributes_dict["subblocks"] = []
    # Create axi_split blocks for each subordinate interface
    for i in range(N_SUBORDINATES):
        split_manager_port_connections = {}
        for j in range(N_MANAGERS):
            split_manager_port_connections[f"m_{j}_m"] = f"connect_s{i}_m{j}"

        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_axi_split",
                "name": f"{py_params_dict['name']}_split",
                "instance_name": f"iob_axi_split_{i}",
                "instance_description": f"AXI split for subordinate {i}",
                "parameters": AXI_VERILOG_PARAMS_MAP,
                "num_managers": N_MANAGERS,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    "s_s": f"s{i}_axi_s",
                    **split_manager_port_connections,
                },
                **axi_iob_params,
            }
        )
    # Create axi_merge blocks for each manager interface
    for i in range(N_MANAGERS):
        merge_subordinate_port_connections = {}
        for j in range(N_SUBORDINATES):
            merge_subordinate_port_connections[f"s_{j}_s"] = f"connect_s{j}_m{i}"

        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_axi_merge",
                "name": f"{py_params_dict['name']}_merge",
                "instance_name": f"iob_axi_merge_{i}",
                "instance_description": f"AXI merge for manager {i}",
                "parameters": AXI_VERILOG_PARAMS_MAP,
                "num_subordinates": N_SUBORDINATES,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    **merge_subordinate_port_connections,
                    "m_m": f"merge_{i}_output",
                },
                **axi_iob_params,
            }
            | {"addr_w": MERGE_OUTPUT_WIDTH},
        )
    #
    # Snippets
    #
    snippet_code = ""
    # Connect merge outputs to manager interfaces
    for i in range(N_MANAGERS):
        # Connect all wires except for address ones
        for wire, direction, _, _ in axi_wires:
            if wire in ["axi_awaddr", "axi_araddr"]:
                continue
            if direction == "input":
                snippet_code += f"""\
   assign m{i}_{wire}_o = merge_{i}_{wire};
"""
            else:  # Direction is output
                snippet_code += f"""\
   assign merge_{i}_{wire} = m{i}_{wire}_i;
"""
        # Connect address wires, ignoring most significant bits
        snippet_code += f"""\
   assign m{i}_axi_awaddr_o = {{ {{{M_SELECT_NBITS}{{1'b0}}}}, merge_{i}_axi_awaddr[{axi_iob_params["addr_w"] - M_SELECT_NBITS}-1:0]}};
   assign m{i}_axi_araddr_o = {{ {{{M_SELECT_NBITS}{{1'b0}}}}, merge_{i}_axi_araddr[{axi_iob_params["addr_w"] - M_SELECT_NBITS}-1:0]}};
"""

    attributes_dict["snippets"] = [
        {
            "verilog_code": snippet_code,
        },
    ]

    return attributes_dict
