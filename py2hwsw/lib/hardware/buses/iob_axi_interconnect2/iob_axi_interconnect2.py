# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Each generated interconnect must have a unique name (can't have two verilog modules with same name).
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated axi interconnect module."
    )
    # Number of master interfaces (number of masters to connect to)
    N_MASTERS = (
        int(py_params_dict["num_masters"]) if "num_masters" in py_params_dict else 1
    )
    # Number of slave interfaces (number of masters to connect to)
    N_SLAVES = (
        int(py_params_dict["num_slaves"]) if "num_slaves" in py_params_dict else 1
    )

    attributes_dict = {
        "name": py_params_dict["name"],
        "version": "0.1",
        #
        # AXI Parameters
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
                "descr": "AXI ID bus width",
            },
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
                "descr": "AXI address bus width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "0",
                "min": "0",
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
    master_axi_ports = []
    for i in range(N_MASTERS):
        master_axi_ports += [
            {
                "name": f"m{i}_axi_m",
                "descr": f"Master {i} interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"m{i}_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ]
    slave_axi_ports = []
    for i in range(N_SLAVES):
        slave_axi_ports += [
            {
                "name": f"s{i}_axi_s",
                "descr": f"Slave {i} interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"s{i}_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ]
    attributes_dict["ports"] += slave_axi_ports + master_axi_ports
    #
    # Wires
    #
    attributes_dict["wires"] = []
    for i in range(N_SLAVES):
        for j in range(N_MASTERS):
            attributes_dict["wires"].append(
                {
                    "name": f"connect_s{i}_m{j}",
                    "descr": f"Connect split of slave {i} to merge of master {j}",
                    "signals": {
                        "type": "axi",
                        "prefix": f"s{i}_m{j}_",
                        "ID_W": "AXI_ID_W",
                        "ADDR_W": "AXI_ADDR_W",
                        "DATA_W": "AXI_DATA_W",
                    },
                }
            )
    #
    # Blocks
    #
    attributes_dict["blocks"] = []
    # Create axi_split blocks for each slave interface
    for i in range(N_SLAVES):
        split_master_port_connections = {}
        for j in range(N_MASTERS):
            split_master_port_connections[f"output_{j}_m"] = f"connect_s{i}_m{j}"

        attributes_dict["blocks"].append(
            {
                "core_name": "iob_axi_split",
                "instance_name": f"iob_axi_split_{i}",
                "instance_description": f"AXI split for slave {i}",
                "parameters": {},
                "connect": {
                    "clk_i": "clk_i",
                    "reset_i": "rst_i",
                    "input_s": f"s{i}_axi_s",
                    **split_master_port_connections,
                },
            }
        )
    # Create axi_merge blocks for each master interface
    for i in range(N_MASTERS):
        merge_slave_port_connections = {}
        for j in range(N_SLAVES):
            merge_slave_port_connections[f"input_{j}_s"] = f"connect_s{j}_m{i}"

        attributes_dict["blocks"].append(
            {
                "core_name": "iob_axi_merge",
                "instance_name": f"iob_axi_merge_{i}",
                "instance_description": f"AXI merge for master {i}",
                "parameters": {},
                "connect": {
                    "clk_i": "clk_i",
                    "reset_i": "rst_i",
                    **merge_slave_port_connections,
                    "output_m": f"m{i}_axi_m",
                },
            }
        )

    return attributes_dict
