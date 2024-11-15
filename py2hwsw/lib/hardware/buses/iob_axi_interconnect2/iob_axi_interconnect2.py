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

    axi_python_params = {
        "addr_w": 32,
        "data_w": 32,
        # "id_w": 1,
        "size_w": 3,
        "burst_w": 2,
        "lock_w": 2,
        "cache_w": 4,
        "prot_w": 3,
        "qos_w": 4,
        "resp_w": 2,
        # "len_w": 8,
        "data_selection_w": 8,
    }
    for param in axi_python_params:
        if param in py_params_dict:
            axi_python_params[param] = int(py_params_dict[param])

    # Same dictionary but with all keys in upper case
    AXI_PYTHON_PARAMS = {i.upper(): v for i, v in axi_python_params.items()}

    axi_verilog_params = {
        "ID_W": 0,
        "LEN_W": 0,
    }
    # Dictionary maps verilog paramters to ones with same name of interconnect
    AXI_VERILOG_PARAMS_MAP = {i: i for i in axi_verilog_params}

    attributes_dict = {
        "name": py_params_dict["name"],
        "version": "0.1",
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
    ]
    for i in range(N_MASTERS):
        attributes_dict["ports"].append(
            {
                "name": f"m{i}_axi_m",
                "descr": f"Master {i} interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"m{i}_",
                    **AXI_VERILOG_PARAMS_MAP,
                    **AXI_PYTHON_PARAMS,
                },
            }
        )
    for i in range(N_SLAVES):
        attributes_dict["ports"].append(
            {
                "name": f"s{i}_axi_s",
                "descr": f"Slave {i} interface",
                "signals": {
                    "type": "axi",
                    "prefix": f"s{i}_",
                    **AXI_VERILOG_PARAMS_MAP,
                    **AXI_PYTHON_PARAMS,
                },
            }
        )
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
                        **AXI_VERILOG_PARAMS_MAP,
                        **AXI_PYTHON_PARAMS,
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
                "parameters": AXI_VERILOG_PARAMS_MAP,
                "connect": {
                    "clk_i": "clk_i",
                    "reset_i": "rst_i",
                    "input_s": f"s{i}_axi_s",
                    **split_master_port_connections,
                },
                **axi_python_params,
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
                "parameters": AXI_VERILOG_PARAMS_MAP,
                "connect": {
                    "clk_i": "clk_i",
                    "reset_i": "rst_i",
                    **merge_slave_port_connections,
                    "output_m": f"m{i}_axi_m",
                },
                **axi_python_params,
            }
        )

    return attributes_dict
