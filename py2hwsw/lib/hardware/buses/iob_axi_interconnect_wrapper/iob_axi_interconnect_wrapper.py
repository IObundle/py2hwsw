# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

AXI_IN_SIGNAL_NAMES = [
    ("araddr", "AXI_ADDR_W"),
    ("arvalid", 1),
    ("rready", 1),
    ("arid", "AXI_ID_W"),
    ("arlen", 8),
    ("arsize", 3),
    ("arburst", 2),
    ("arlock", 1),
    ("arcache", 4),
    ("arqos", 4),
    ("awaddr", "AXI_ADDR_W"),
    ("awvalid", 1),
    ("wdata", "AXI_DATA_W"),
    ("wstrb", "AXI_DATA_W / 8"),
    ("wvalid", 1),
    ("bready", 1),
    ("awid", "AXI_ID_W"),
    ("awlen", 8),
    ("awsize", 3),
    ("awburst", 2),
    ("awlock", 1),
    ("awcache", 4),
    ("awqos", 4),
    ("wlast", 1),
]

AXI_OUT_SIGNAL_NAMES = [
    ("arready", 1),
    ("rdata", "AXI_DATA_W"),
    ("rresp", 2),
    ("rvalid", 1),
    ("rid", "AXI_ID_W"),
    ("rlast", 1),
    ("awready", 1),
    ("wready", 1),
    ("bresp", 2),
    ("bvalid", 1),
    ("bid", "AXI_ID_W"),
]


def setup(py_params_dict):
    """Wrapper for `axi_interconnect` core.
    Python parameters:
    - num_subordinates: number of subordinate interfaces
    - managers: dictionary with name and address width of each manager
    """
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["name"] = os.path.basename(__file__)

    # Each generated wrapper must have a unique name (can't have two verilog modules with same name).
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated interconnect wrapper module."
    )
    # Number of subordinate interfaces (number of managers to connect to)
    N_SUBORDINATES = (
        int(py_params_dict["num_subordinates"])
        if "num_subordinates" in py_params_dict
        else 1
    )
    # Dictionary with name and address width of each manager
    MANAGERS = (
        py_params_dict["managers"]
        if "managers" in py_params_dict
        else {"m0": "AXI_ADDR_W"}
    )

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
        #
        # AXI Parameters
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI ID bus width",
            },
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI address bus width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI data bus width",
            },
        ],
        #
        # Ports
        #
        "ports": [
            {
                "name": "clk_i",
                "descr": "Clock",
                "signals": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
        ],
    }
    subordinate_axi_ports = []
    for i in range(N_SUBORDINATES):
        subordinate_axi_ports += [
            {
                "name": f"s{i}_axi_s",
                "descr": f"Subordinate {i} interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"s{i}_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": 1,
                },
            },
        ]
    manager_axi_ports = []
    manager_addr_w_parameter = ""
    for name, width in MANAGERS.items():
        attributes_dict["confs"].append(
            {
                "name": f"{name.upper()}_ADDR_W",
                "type": "P",
                "val": width,
                "min": "1",
                "max": "32",
                "descr": f"{name.upper()} address bus width. Can be smaller than address range of manager, but not larger.",
            }
        )
        manager_axi_ports += [
            {
                "name": f"{name}_axi_m",
                "descr": f"Manager '{name}' axi interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"{name}_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": f"{name.upper()}_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": 1,
                },
            },
        ]
        try:
            width_str = "32'd" + str(int(width))
        except ValueError:
            width_str = width
        manager_addr_w_parameter = f"{width_str}," + manager_addr_w_parameter
    manager_addr_w_parameter = manager_addr_w_parameter[:-1]
    if len(MANAGERS) > 1:
        manager_addr_w_parameter = "{" + manager_addr_w_parameter + "}"
    attributes_dict["ports"] += subordinate_axi_ports + manager_axi_ports
    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "interconnect_s_axi",
            "descr": "AXI subordinate bus for interconnect",
            "signals": {
                "type": "axi",
                "prefix": "intercon_s_",
                "mult": N_SUBORDINATES,
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LOCK_W": 1,
            },
        },
        {
            "name": "interconnect_m_axi",
            "descr": "AXI manager bus for interconnect",
            "signals": {
                "type": "axi",
                "prefix": "intercon_m_",
                "mult": len(MANAGERS),
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LOCK_W": 1,
            },
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_axi_interconnect",
            "instance_name": "iob_axi_interconnect_core",
            "instance_description": "Interconnect core",
            "parameters": {
                "ID_WIDTH": "AXI_ID_W",
                "DATA_WIDTH": "AXI_DATA_W",
                "ADDR_WIDTH": "AXI_ADDR_W",
                "S_COUNT": N_SUBORDINATES,
                "M_COUNT": len(MANAGERS),
                "M_ADDR_WIDTH": manager_addr_w_parameter,
            },
            "connect": {
                "clk_i": "clk_i",
                "rst_i": "rst_i",
                "s_axi_s": "interconnect_s_axi",
                "m_axi_m": "interconnect_m_axi",
            },
        },
    ]

    # Connect all Subordinate AXI interfaces to interconnect
    verilog_code = "    // Connect all subordinate AXI interfaces to interconnect\n"
    for sig_name, _ in AXI_IN_SIGNAL_NAMES:
        assign_str = ""
        for port in subordinate_axi_ports:
            prefix = ""
            if "prefix" in port["signals"]:
                prefix = port["signals"]["prefix"]
            assign_str = f"{prefix}axi_{sig_name}_i, " + assign_str
        assign_str = assign_str[:-2]
        verilog_code += (
            f"    assign intercon_s_axi_{sig_name} = {{" + assign_str + "};\n"
        )

    for sig_name, sig_size in AXI_OUT_SIGNAL_NAMES:
        for idx, port in enumerate(subordinate_axi_ports):
            prefix = ""
            if "prefix" in port["signals"]:
                prefix = port["signals"]["prefix"]
            bit_select = ""
            if type(sig_size) is not int or sig_size > 1:
                bit_select = f"[{idx}*{sig_size}+:{sig_size}]"
            elif len(subordinate_axi_ports) > 1:
                bit_select = f"[{idx}]"
            verilog_code += f"    assign {prefix}axi_{sig_name}_o = intercon_s_axi_{sig_name}{bit_select}; \n"

    # Connect all Manager AXI interfaces to interconnect
    verilog_code += "    // Connect all manager AXI interfaces to interconnect\n"
    for sig_name, _ in AXI_OUT_SIGNAL_NAMES:
        assign_str = ""
        for manager_name in MANAGERS:
            prefix = f"{manager_name}_"
            assign_str = f"{prefix}axi_{sig_name}_i, " + assign_str
        assign_str = assign_str[:-2]
        verilog_code += (
            f"    assign intercon_m_axi_{sig_name} = {{" + assign_str + "};\n"
        )

    for sig_name, sig_size in AXI_IN_SIGNAL_NAMES:
        for idx, manager_name in enumerate(MANAGERS):
            prefix = f"{manager_name}_"
            output_size = sig_size
            if sig_name.endswith("addr"):
                output_size = f"{name.upper()}_ADDR_W"
            bit_select = ""
            if type(sig_size) is not int or sig_size > 1:
                bit_select = f"[{idx}*{sig_size}+:{output_size}]"
            elif len(manager_axi_ports) > 1:
                bit_select = f"[{idx}]"
            verilog_code += f"    assign {prefix}axi_{sig_name}_o = intercon_m_axi_{sig_name}{bit_select}; \n"

    attributes_dict["snippets"] = [
        {
            "verilog_code": verilog_code,
        }
    ]

    return attributes_dict
