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
        ("axi_awaddr", "output", ADDR_W),
        ("axi_awprot", "output", PROT_W),
        ("axi_awvalid", "output", 1),
        ("axi_awready", "input", 1),
        ("axi_wdata", "output", DATA_W),
        ("axi_wstrb", "output", int(DATA_W / DATA_SECTION_W)),
        ("axi_wvalid", "output", 1),
        ("axi_wready", "input", 1),
        ("axi_bresp", "input", RESP_W),
        ("axi_bvalid", "input", 1),
        ("axi_bready", "output", 1),
        # AXI specific write
        ("axi_awid", "output", ID_W),
        ("axi_awlen", "output", LEN_W),
        ("axi_awsize", "output", SIZE_W),
        ("axi_awburst", "output", BURST_W),
        ("axi_awlock", "output", LOCK_W),
        ("axi_awcache", "output", CACHE_W),
        ("axi_awqos", "output", QOS_W),
        ("axi_wlast", "output", 1),
        ("axi_bid", "input", ID_W),
        # AXI-Lite Read
        ("axi_araddr", "output", ADDR_W),
        ("axi_arprot", "output", PROT_W),
        ("axi_arvalid", "output", 1),
        ("axi_arready", "input", 1),
        ("axi_rdata", "input", DATA_W),
        ("axi_rresp", "input", RESP_W),
        ("axi_rvalid", "input", 1),
        ("axi_rready", "output", 1),
        # AXI specific read
        ("axi_arid", "output", ID_W),
        ("axi_arlen", "output", LEN_W),
        ("axi_arsize", "output", SIZE_W),
        ("axi_arburst", "output", BURST_W),
        ("axi_arlock", "output", LOCK_W),
        ("axi_arcache", "output", CACHE_W),
        ("axi_arqos", "output", QOS_W),
        ("axi_rid", "input", ID_W),
        ("axi_rlast", "input", 1),
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
