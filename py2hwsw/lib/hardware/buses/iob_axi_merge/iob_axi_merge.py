# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated merge module."
    )
    assert "num_inputs" in py_params_dict, print(
        "Error: Missing number of inputs for generated merge module."
    )

    NUM_INPUTS = int(py_params_dict["num_inputs"])
    # Number of bits required for input selection
    NBITS = (NUM_INPUTS - 1).bit_length()

    ADDR_W = int(py_params_dict["addr_w"]) if "addr_w" in py_params_dict else 32
    DATA_W = int(py_params_dict["data_w"]) if "data_w" in py_params_dict else 32
    ID_W = int(py_params_dict["id_w"]) if "id_w" in py_params_dict else 1
    SIZE_W = int(py_params_dict["size_w"]) if "size_w" in py_params_dict else 3
    BURST_W = int(py_params_dict["burst_w"]) if "burst_w" in py_params_dict else 2
    LOCK_W = int(py_params_dict["lock_w"]) if "lock_w" in py_params_dict else 2
    CACHE_W = int(py_params_dict["cache_w"]) if "cache_w" in py_params_dict else 4
    PROT_W = int(py_params_dict["prot_w"]) if "prot_w" in py_params_dict else 3
    QOS_W = int(py_params_dict["qos_w"]) if "qos_w" in py_params_dict else 4
    RESP_W = int(py_params_dict["resp_w"]) if "resp_w" in py_params_dict else 2
    LEN_W = int(py_params_dict["len_w"]) if "len_w" in py_params_dict else 8
    DATA_SECTION_W = (
        int(py_params_dict["data_section_w"])
        if "data_section_w" in py_params_dict
        else 8
    )

    axi_signals = [
        # AXI-Lite Write
        ("axi_awaddr", "input", ADDR_W, "write"),
        ("axi_awprot", "input", PROT_W, "write"),
        ("axi_awvalid", "input", 1, "write"),
        ("axi_awready", "output", 1, "write"),
        ("axi_wdata", "input", DATA_W, "write"),
        ("axi_wstrb", "input", int(DATA_W / DATA_SECTION_W), "write"),
        ("axi_wvalid", "input", 1, "write"),
        ("axi_wready", "output", 1, "write"),
        ("axi_bresp", "output", RESP_W, "write"),
        ("axi_bvalid", "output", 1, "write"),
        ("axi_bready", "input", 1, "write"),
        # AXI specific write
        ("axi_awid", "input", ID_W, "write"),
        ("axi_awlen", "input", LEN_W, "write"),
        ("axi_awsize", "input", SIZE_W, "write"),
        ("axi_awburst", "input", BURST_W, "write"),
        ("axi_awlock", "input", LOCK_W, "write"),
        ("axi_awcache", "input", CACHE_W, "write"),
        ("axi_awqos", "input", QOS_W, "write"),
        ("axi_wlast", "input", 1, "write"),
        ("axi_bid", "output", ID_W, "write"),
        # AXI-Lite Read
        ("axi_araddr", "input", ADDR_W, "read"),
        ("axi_arprot", "input", PROT_W, "read"),
        ("axi_arvalid", "input", 1, "read"),
        ("axi_arready", "output", 1, "read"),
        ("axi_rdata", "output", DATA_W, "read"),
        ("axi_rresp", "output", RESP_W, "read"),
        ("axi_rvalid", "output", 1, "read"),
        ("axi_rready", "input", 1, "read"),
        # AXI specific read
        ("axi_arid", "input", ID_W, "read"),
        ("axi_arlen", "input", LEN_W, "read"),
        ("axi_arsize", "input", SIZE_W, "read"),
        ("axi_arburst", "input", BURST_W, "read"),
        ("axi_arlock", "input", LOCK_W, "read"),
        ("axi_arcache", "input", CACHE_W, "read"),
        ("axi_arqos", "input", QOS_W, "read"),
        ("axi_rid", "output", ID_W, "read"),
        ("axi_rlast", "output", 1, "read"),
    ]

    attributes_dict = {
        "name": py_params_dict["name"],
        "version": "0.1",
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "clk_en_rst",
            },
            "descr": "Clock, clock enable and async reset",
        },
        {
            "name": "reset_i",
            "descr": "Reset signal",
            "signals": [
                {
                    "name": "rst_i",
                    "width": "1",
                },
            ],
        },
        {
            "name": "output_m",
            "signals": {
                "type": "axi",
                "file_prefix": py_params_dict["name"] + "_output_",
                "prefix": "output_",
                "DATA_W": DATA_W,
                "ADDR_W": ADDR_W,
                "ID_W": ID_W,
                "SIZE_W": SIZE_W,
                "BURST_W": BURST_W,
                "LOCK_W": LOCK_W,
                "CACHE_W": CACHE_W,
                "PROT_W": PROT_W,
                "QOS_W": QOS_W,
                "RESP_W": RESP_W,
                "LEN_W": LEN_W,
            },
            "descr": "Merge output",
        },
    ]
    for port_idx in range(NUM_INPUTS):
        attributes_dict["ports"].append(
            {
                "name": f"input_{port_idx}_s",
                "signals": {
                    "type": "axi",
                    "file_prefix": f"{py_params_dict['name']}_input{port_idx}_",
                    "prefix": f"input{port_idx}_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W - NBITS,
                    "ID_W": ID_W,
                    "SIZE_W": SIZE_W,
                    "BURST_W": BURST_W,
                    "LOCK_W": LOCK_W,
                    "CACHE_W": CACHE_W,
                    "PROT_W": PROT_W,
                    "QOS_W": QOS_W,
                    "RESP_W": RESP_W,
                    "LEN_W": LEN_W,
                },
                "descr": "Merge input interfaces",
            },
        )
    #
    # Wires
    #
    # TODO: Fix below #######################

    return attributes_dict
