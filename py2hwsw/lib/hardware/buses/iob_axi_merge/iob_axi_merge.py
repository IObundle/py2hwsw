# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["name"] = os.path.basename(__file__)
        py_params_dict["num_subordinates"] = 2

    assert "name" in py_params_dict, print(
        "Error: Missing name for generated merge module."
    )
    assert "num_subordinates" in py_params_dict, print(
        "Error: Missing number of subordinates for generated merge module."
    )

    NUM_SUBORDINATES = int(py_params_dict["num_subordinates"])
    # Number of bits required for subordinate selection
    NBITS = (NUM_SUBORDINATES - 1).bit_length()

    TRANSFER_COUNTER_DATA_W = py_params_dict.get("transfer_counter_data_w", 5)

    ADDR_W = int(py_params_dict["addr_w"]) if "addr_w" in py_params_dict else 32
    DATA_W = int(py_params_dict["data_w"]) if "data_w" in py_params_dict else 32
    # ID_W = int(py_params_dict["id_w"]) if "id_w" in py_params_dict else 1
    SIZE_W = int(py_params_dict["size_w"]) if "size_w" in py_params_dict else 3
    BURST_W = int(py_params_dict["burst_w"]) if "burst_w" in py_params_dict else 2
    LOCK_W = int(py_params_dict["lock_w"]) if "lock_w" in py_params_dict else 2
    CACHE_W = int(py_params_dict["cache_w"]) if "cache_w" in py_params_dict else 4
    # PROT_W = int(py_params_dict["prot_w"]) if "prot_w" in py_params_dict else 3
    QOS_W = int(py_params_dict["qos_w"]) if "qos_w" in py_params_dict else 4
    RESP_W = int(py_params_dict["resp_w"]) if "resp_w" in py_params_dict else 2
    # LEN_W = int(py_params_dict["len_w"]) if "len_w" in py_params_dict else 8
    DATA_SECTION_W = (
        int(py_params_dict["data_section_w"])
        if "data_section_w" in py_params_dict
        else 8
    )

    # Disble 'black' python formatter for this block
    # fmt: off
    axi_signals = [
        # --------------------------------------------------------------------------
        # Name         |Direction|Width                        |Ch Type |Registered|
        #
        # AXI-Lite Write
        #
        # AW Channel
        ("axi_awaddr",  "input",  ADDR_W,                       "write", False),
        # ("axi_awprot",  "input",  PROT_W,                       "write", False),
        ("axi_awvalid", "input",  1,                            "write", False),
        ("axi_awready", "output", 1,                            "write", False),
        # W Channel
        ("axi_wdata",   "input",  DATA_W,                       "write", False),
        ("axi_wstrb",   "input",  int(DATA_W / DATA_SECTION_W), "write", False),
        ("axi_wvalid",  "input",  1,                            "write", False),
        ("axi_wready",  "output", 1,                            "write", False),
        # B Channel
        ("axi_bresp",   "output", RESP_W,                       "write", True),
        ("axi_bvalid",  "output", 1,                            "write", True),
        ("axi_bready",  "input",  1,                            "write", True),
        #
        # AXI specific write
        #
        # AW Channel
        ("axi_awid",    "input",  "ID_W",                       "write", False),
        ("axi_awlen",   "input",  "LEN_W",                      "write", False),
        ("axi_awsize",  "input",  SIZE_W,                       "write", False),
        ("axi_awburst", "input",  BURST_W,                      "write", False),
        ("axi_awlock",  "input",  LOCK_W,                       "write", False),
        ("axi_awcache", "input",  CACHE_W,                      "write", False),
        ("axi_awqos",   "input",  QOS_W,                        "write", False),
        # W Channel
        ("axi_wlast",   "input",  1,                            "write", False),
        # B Channel
        ("axi_bid",     "output", "ID_W",                       "write", True),

        #
        # AXI-Lite Read
        #
        # AR Channel
        ("axi_araddr",  "input",  ADDR_W,                        "read", False),
        # ("axi_arprot",  "input",  PROT_W,                        "read", False),
        ("axi_arvalid", "input",  1,                             "read", False),
        ("axi_arready", "output", 1,                             "read", False),
        # R Channel
        ("axi_rdata",   "output", DATA_W,                        "read", True),
        ("axi_rresp",   "output", RESP_W,                        "read", True),
        ("axi_rvalid",  "output", 1,                             "read", True),
        ("axi_rready",  "input",  1,                             "read", True),
        #
        # AXI specific read
        #
        # AR Channel
        ("axi_arid",    "input",  "ID_W",                        "read", False),
        ("axi_arlen",   "input",  "LEN_W",                       "read", False),
        ("axi_arsize",  "input",  SIZE_W,                        "read", False),
        ("axi_arburst", "input",  BURST_W,                       "read", False),
        ("axi_arlock",  "input",  LOCK_W,                        "read", False),
        ("axi_arcache", "input",  CACHE_W,                       "read", False),
        ("axi_arqos",   "input",  QOS_W,                         "read", False),
        # R Channel
        ("axi_rid",     "output", "ID_W",                        "read", True),
        ("axi_rlast",   "output", 1,                             "read", True),
    ]
    # fmt: on

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
        #
        # AXI Parameters
        #
        "confs": [
            {
                "name": "ID_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI ID bus width",
            },
            {
                "name": "LEN_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "32",
                "descr": "AXI LEN bus width",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "iob_clk",
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
            "name": "m_m",
            "signals": {
                "type": "axi",
                "file_prefix": py_params_dict["name"] + "_m_",
                "prefix": "m_",
                "DATA_W": DATA_W,
                "ADDR_W": ADDR_W,
                "ID_W": "ID_W",
                "SIZE_W": SIZE_W,
                "BURST_W": BURST_W,
                "LOCK_W": LOCK_W,
                "CACHE_W": CACHE_W,
                # "PROT_W": PROT_W,
                "QOS_W": QOS_W,
                "RESP_W": RESP_W,
                "LEN_W": "LEN_W",
            },
            "descr": "Merge manager",
        },
    ]
    for port_idx in range(NUM_SUBORDINATES):
        attributes_dict["ports"].append(
            {
                "name": f"s_{port_idx}_s",
                "signals": {
                    "type": "axi",
                    "file_prefix": f"{py_params_dict['name']}_s{port_idx}_",
                    "prefix": f"s{port_idx}_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W - NBITS,
                    "ID_W": "ID_W",
                    "SIZE_W": SIZE_W,
                    "BURST_W": BURST_W,
                    "LOCK_W": LOCK_W,
                    "CACHE_W": CACHE_W,
                    # "PROT_W": PROT_W,
                    "QOS_W": QOS_W,
                    "RESP_W": RESP_W,
                    "LEN_W": "LEN_W",
                },
                "descr": "Merge subordinate interfaces",
            },
        )
    #
    # Wires
    #
    attributes_dict["buses"] = [
        # Busy read reg
        {
            "name": "busy_read_reg_en_rst",
            "descr": "Enable and reset signal for busy_read_reg",
            "signals": [
                {"name": "busy_read_reg_en", "width": 1},
                {"name": "busy_read_reg_rst", "width": 1},
            ],
        },
        {
            "name": "busy_read_reg_data_i",
            "descr": "Input of busy_read_reg",
            "signals": [
                {"name": "busy_read_reg_i", "width": 1},
            ],
        },
        {
            "name": "busy_read_reg_data_o",
            "descr": "Output of busy_read_reg",
            "signals": [
                {"name": "busy_read_reg_o", "width": 1},
            ],
        },
        # Active read transfer reg
        {
            "name": "active_transaction_read_reg_en_rst",
            "descr": "Enable and reset signal for active_transaction_read_reg",
            "signals": [
                {"name": "active_transaction_read_reg_en", "width": 1},
                {"name": "active_transaction_read_reg_rst", "width": 1},
            ],
        },
        {
            "name": "active_transaction_read_reg_data_i",
            "descr": "Input of active_transaction_read_reg",
            "signals": [
                {"name": "active_transaction_read_reg_i", "width": 1},
            ],
        },
        {
            "name": "active_transaction_read_reg_data_o",
            "descr": "Output of active_transaction_read_reg",
            "signals": [
                {"name": "active_transaction_read_reg_o", "width": 1},
            ],
        },
        # Read selection register signals
        {
            "name": "read_sel_reg_rst",
            "descr": "Enable and reset signal for read_sel_reg",
            "signals": [
                {"name": "rst_i"},
            ],
        },
        {
            "name": "read_sel_reg_data_i",
            "descr": "Input of read_sel_reg",
            "signals": [
                {"name": "read_sel", "width": NBITS},
            ],
        },
        {
            "name": "read_sel_reg_data_o",
            "descr": "Output of read_sel_reg",
            "signals": [
                {"name": "read_sel_reg", "width": NBITS},
            ],
        },
        {
            "name": "s_read_sel",
            "descr": "Select subordinate interface",
            "signals": [
                {"name": "read_sel"},
            ],
        },
        {
            "name": "s_read_sel_reg",
            "descr": "Registered select subordinate interface",
            "signals": [
                {"name": "read_sel_reg"},
            ],
        },
        # Busy write reg
        {
            "name": "busy_write_reg_en_rst",
            "descr": "Enable and reset signal for busy_write_reg",
            "signals": [
                {"name": "busy_write_reg_en", "width": 1},
                {"name": "busy_write_reg_rst", "width": 1},
            ],
        },
        {
            "name": "busy_write_reg_data_i",
            "descr": "Input of busy_write_reg",
            "signals": [
                {"name": "busy_write_reg_i", "width": 1},
            ],
        },
        {
            "name": "busy_write_reg_data_o",
            "descr": "Output of busy_write_reg",
            "signals": [
                {"name": "busy_write_reg_o", "width": 1},
            ],
        },
        # Allow write address signals
        {
            "name": "allow_write_address",
            "descr": "Signals to allow address valid/ready",
            "signals": [
                {"name": "wants_change_write_sel", "width": 1},
                {"name": "allow_write_address", "width": 1},
            ],
        },
        # Active write transaction acc
        {
            "name": "active_write_transaction_acc_en_rst",
            "descr": "Enable and reset signal for active_write_transaction_acc",
            "signals": [
                {"name": "active_write_transaction_acc_en", "width": 1},
                {"name": "rst_i"},
            ],
        },
        {
            "name": "active_write_transaction_acc_input",
            "descr": "Input of active_write_transaction_acc",
            "signals": [
                {
                    "name": "active_write_transaction_acc_input",
                    "width": TRANSFER_COUNTER_DATA_W,
                },
            ],
        },
        {
            "name": "active_write_transaction_count",
            "descr": "Output of active_write_transaction_acc",
            "signals": [
                {
                    "name": "active_write_transaction_count",
                    "width": TRANSFER_COUNTER_DATA_W,
                },
            ],
        },
        {
            "name": "active_write_transaction",
            "descr": "Check for any active write transactions",
            "signals": [
                {"name": "active_write_transaction", "width": 1},
            ],
        },
        {
            "name": "active_write_transaction_start_end",
            "descr": "Start and end signals of active write transaction",
            "signals": [
                {"name": "start_active_write_transaction", "width": 1},
                {"name": "end_active_write_transaction", "width": 1},
            ],
        },
        {
            "name": "full_active_write_transaction",
            "descr": "Check if active write accumulator is full",
            "signals": [
                {"name": "full_active_write_transaction", "width": 1},
            ],
        },
        # Allow write data
        {
            "name": "allow_write_data",
            "descr": "Signal to allow data valid/ready",
            "signals": [
                {"name": "allow_write_data", "width": 1},
            ],
        },
        # Pending write response acc
        {
            "name": "pending_write_response_acc_en_rst",
            "descr": "Enable and reset signal for pending_write_response_acc",
            "signals": [
                {"name": "pending_write_response_acc_en", "width": 1},
                {"name": "rst_i"},
            ],
        },
        {
            "name": "pending_write_response_acc_input",
            "descr": "Input of pending_write_response_acc",
            "signals": [
                {
                    "name": "pending_write_response_acc_input",
                    "width": TRANSFER_COUNTER_DATA_W,
                },
            ],
        },
        {
            "name": "pending_write_response_count",
            "descr": "Output of pending_write_response_acc",
            "signals": [
                {
                    "name": "pending_write_response_count",
                    "width": TRANSFER_COUNTER_DATA_W,
                },
            ],
        },
        {
            "name": "pending_write_response",
            "descr": "Check for any active write transactions",
            "signals": [
                {"name": "pending_write_response", "width": 1},
            ],
        },
        {
            "name": "pending_write_response_start_end",
            "descr": "Start and end signals of active write transaction",
            "signals": [
                {"name": "start_pending_write_response", "width": 1},
                {"name": "end_pending_write_response", "width": 1},
            ],
        },
        {
            "name": "full_pending_write_response",
            "descr": "Check if pending write accumulator is full",
            "signals": [
                {"name": "full_pending_write_response", "width": 1},
            ],
        },
        # Write selection register signals
        {
            "name": "write_sel_reg_rst",
            "descr": "Enable and reset signal for write_sel_reg",
            "signals": [
                {"name": "rst_i"},
            ],
        },
        {
            "name": "write_sel_reg_data_i",
            "descr": "Input of write_sel_reg",
            "signals": [
                {"name": "write_sel", "width": NBITS},
            ],
        },
        {
            "name": "write_sel_reg_data_o",
            "descr": "Output of write_sel_reg",
            "signals": [
                {"name": "write_sel_reg", "width": NBITS},
            ],
        },
        {
            "name": "s_write_sel",
            "descr": "Select subordinate interface",
            "signals": [
                {"name": "write_sel"},
            ],
        },
        {
            "name": "s_write_sel_reg",
            "descr": "Registered select subordinate interface",
            "signals": [
                {"name": "write_sel_reg"},
            ],
        },
        # Read priority encoder signals
        {
            "name": "read_sel_prio_enc_i",
            "descr": "Input of read priority encoder",
            "signals": [
                {"name": "mux_axi_arvalid", "width": f"{NUM_SUBORDINATES} * 1"},
            ],
        },
        {
            "name": "read_sel_prio_enc_o",
            "descr": "Output of read priority encoder",
            "signals": [
                {
                    "name": "read_sel_prio_enc_o",
                    "width": f"$clog2({NUM_SUBORDINATES}+1)",
                },
            ],
        },
        # Write priority encoder signals
        {
            "name": "write_sel_prio_enc_i",
            "descr": "Input of write priority encoder",
            "signals": [
                {"name": "mux_axi_awvalid", "width": f"{NUM_SUBORDINATES} * 1"},
            ],
        },
        {
            "name": "write_sel_prio_enc_o",
            "descr": "Output of write priority encoder",
            "signals": [
                {
                    "name": "write_sel_prio_enc_o",
                    "width": f"$clog2({NUM_SUBORDINATES}+1)",
                },
            ],
        },
    ]
    # Generate buses for muxers and demuxers
    for signal, direction, width, _, _ in axi_signals:
        if direction == "output":
            prefix = "m_"
            if signal in ["axi_arready", "axi_awready", "axi_wready"]:
                prefix = "demux_"
            # Demux signals
            attributes_dict["buses"] += [
                {
                    "name": "demux_" + signal + "_i",
                    "descr": f"Input of {signal} demux",
                    "signals": [
                        {
                            "name": prefix + signal + "_i",
                        },
                    ],
                },
                {
                    "name": "demux_" + signal + "_o",
                    "descr": f"Output of {signal} demux",
                    "signals": [
                        {
                            "name": "demux_" + signal,
                            "width": f"{NUM_SUBORDINATES} * {width}",
                        },
                    ],
                },
            ]
        else:  # input direction
            prefix = "m_"
            if signal in ["axi_arvalid", "axi_awvalid", "axi_wvalid"]:
                prefix = "mux_"
            # Mux signals
            attributes_dict["buses"] += [
                {
                    "name": "mux_" + signal + "_i",
                    "descr": f"Input of {signal} demux",
                    "signals": [
                        {
                            "name": "mux_" + signal,
                            "width": f"{NUM_SUBORDINATES} * {width}",
                        },
                    ],
                },
                {
                    "name": "mux_" + signal + "_o",
                    "descr": f"Output of {signal} demux",
                    "signals": [
                        {
                            "name": prefix + signal + "_o",
                        },
                    ],
                },
            ]

    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        # Read blocks
        {
            "core_name": "iob_reg",
            "instance_name": "busy_read_reg_re",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:busy_read_reg_en",
                        "rst_i:busy_read_reg_rst",
                    ],
                ),
                "data_i": "busy_read_reg_data_i",
                "data_o": "busy_read_reg_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "active_transaction_read_reg_re",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:active_transaction_read_reg_en",
                        "rst_i:active_transaction_read_reg_rst",
                    ],
                ),
                "data_i": "active_transaction_read_reg_data_i",
                "data_o": "active_transaction_read_reg_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "read_sel_reg_r",
            "parameters": {
                "DATA_W": NBITS,
                "RST_VAL": f"{NBITS}'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "rst_i:rst_i",
                    ],
                ),
                "data_i": "read_sel_reg_data_i",
                "data_o": "read_sel_reg_data_o",
            },
        },
        {
            "core_name": "iob_prio_enc",
            "instance_name": "read_sel_enc",
            "parameters": {
                "W": NUM_SUBORDINATES,
                "MODE": '"HIGH"',
            },
            "connect": {
                "unencoded_i": "read_sel_prio_enc_i",
                "encoded_o": "read_sel_prio_enc_o",
            },
        },
        # Write blocks
        {
            "core_name": "iob_reg",
            "instance_name": "busy_write_reg_re",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:busy_write_reg_en",
                        "rst_i:busy_write_reg_rst",
                    ],
                ),
                "data_i": "busy_write_reg_data_i",
                "data_o": "busy_write_reg_data_o",
            },
        },
        # Write blocks
        {
            "core_name": "iob_acc",
            "instance_name": "active_write_transaction_acc",
            "parameters": {
                "DATA_W": TRANSFER_COUNTER_DATA_W,
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "en_rst_i": "active_write_transaction_acc_en_rst",
                "incr_i": "active_write_transaction_acc_input",
                "data_o": "active_write_transaction_count",
            },
        },
        {
            "core_name": "iob_acc",
            "instance_name": "pending_write_response_acc",
            "parameters": {
                "DATA_W": TRANSFER_COUNTER_DATA_W,
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "en_rst_i": "pending_write_response_acc_en_rst",
                "incr_i": "pending_write_response_acc_input",
                "data_o": "pending_write_response_count",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "write_sel_reg_r",
            "parameters": {
                "DATA_W": NBITS,
                "RST_VAL": f"{NBITS}'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "rst_i:rst_i",
                    ],
                ),
                "data_i": "write_sel_reg_data_i",
                "data_o": "write_sel_reg_data_o",
            },
        },
        {
            "core_name": "iob_prio_enc",
            "instance_name": "write_sel_enc",
            "parameters": {
                "W": NUM_SUBORDINATES,
                "MODE": '"HIGH"',
            },
            "connect": {
                "unencoded_i": "write_sel_prio_enc_i",
                "encoded_o": "write_sel_prio_enc_o",
            },
        },
    ]
    # Generate muxers and demuxers
    for signal, direction, width, sig_type, registered in axi_signals:
        sel_signal_suffix = "_reg" if registered else ""
        if direction == "output":
            # Demuxers
            attributes_dict["subblocks"].append(
                {
                    "core_name": "iob_demux",
                    "instance_name": "iob_demux_" + signal,
                    "parameters": {
                        "DATA_W": width,
                        "N": NUM_SUBORDINATES,
                    },
                    "connect": {
                        "sel_i": f"s_{sig_type}_sel{sel_signal_suffix}",
                        "data_i": "demux_" + signal + "_i",
                        "data_o": "demux_" + signal + "_o",
                    },
                },
            )
        else:  # input direction
            # Muxers
            attributes_dict["subblocks"].append(
                {
                    "core_name": "iob_mux",
                    "instance_name": "iob_mux_" + signal,
                    "parameters": {
                        "DATA_W": width,
                        "N": NUM_SUBORDINATES,
                    },
                    "connect": {
                        "sel_i": f"s_{sig_type}_sel{sel_signal_suffix}",
                        "data_i": "mux_" + signal + "_i",
                        "data_o": "mux_" + signal + "_o",
                    },
                },
            )
    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": f"""
   //
   // Read
   //

   // Only switch managers when there is no current active transaction
   assign read_sel = busy_read_reg_o ? read_sel_reg : read_sel_prio_enc_o[{NBITS}-1:0];

   assign busy_read_reg_en = m_axi_arvalid_o & !busy_read_reg_o;
   assign busy_read_reg_rst = (m_axi_rlast_i & m_axi_rvalid_i & m_axi_rready_o) | rst_i;
   assign busy_read_reg_i = 1'b1;

   // Block address valid/ready signals of current manager if there is still an active transaction
   assign m_axi_arvalid_o = ~active_transaction_read_reg_o & mux_axi_arvalid_o;
   assign demux_axi_arready_i = ~active_transaction_read_reg_o & m_axi_arready_i;

   assign active_transaction_read_reg_en = m_axi_arvalid_o & m_axi_arready_i;
   assign active_transaction_read_reg_rst = busy_read_reg_rst;
   assign active_transaction_read_reg_i = 1'b1;

   //
   // Write
   //

   // NOTE: Current logic does not allow wvalid to be asserted before awvalid!
   //       If the wvalid comes before, the data will go to the currently selected manager_interface, and that may not be the intended destination (real destination will be given later by awvalid)

   // Only switch managers when there is no current active transaction
   assign write_sel = (busy_write_reg_o | active_write_transaction) ? write_sel_reg : write_sel_prio_enc_o[{NBITS}-1:0];

   assign busy_write_reg_en = m_axi_awvalid_o & !busy_write_reg_o;
   assign busy_write_reg_rst = end_pending_write_response;
   assign busy_write_reg_i = 1'b1;

   // Block address valid/ready signals of current manager if accumulator full or if another manager wants to write
   assign wants_change_write_sel = write_sel != write_sel_prio_enc_o;
   assign allow_write_address = ~(full_active_write_transaction | (active_write_transaction & wants_change_write_sel));
   assign m_axi_awvalid_o = allow_write_address & mux_axi_awvalid_o;
   assign demux_axi_awready_i = allow_write_address & m_axi_awready_i;

   assign start_active_write_transaction = m_axi_awvalid_o & m_axi_awready_i;
   assign end_active_write_transaction = end_pending_write_response;
   assign active_write_transaction = |active_write_transaction_count;
   assign full_active_write_transaction = &active_write_transaction_count;

   // iob_acc inputs
   assign active_write_transaction_acc_en = start_active_write_transaction ^ end_active_write_transaction;
   assign active_write_transaction_acc_input = start_active_write_transaction ? {TRANSFER_COUNTER_DATA_W}'d1 : -{TRANSFER_COUNTER_DATA_W}'d1;

   // Block data valid/ready signals of current manager if accumulator full or if another manager wants to write
   assign allow_write_data = ~(full_pending_write_response | (pending_write_response & wants_change_write_sel));
   assign m_axi_wvalid_o = allow_write_data & mux_axi_wvalid_o;
   assign demux_axi_wready_i = allow_write_data & m_axi_wready_i;

   assign start_pending_write_response = m_axi_wlast_o & m_axi_wvalid_o & m_axi_wready_i;
   assign end_pending_write_response = m_axi_bvalid_i & m_axi_bready_o;
   assign pending_write_response = |pending_write_response_count;
   assign full_pending_write_response = &pending_write_response_count;

   // iob_acc inputs
   assign pending_write_response_acc_en = start_pending_write_response ^ end_pending_write_response;
   assign pending_write_response_acc_input = start_pending_write_response ? {TRANSFER_COUNTER_DATA_W}'d1 : -{TRANSFER_COUNTER_DATA_W}'d1;
""",
        },
    ]

    verilog_code = ""
    # Connect muxer/demuxer inputs/outputs
    for signal, direction, width, _, _ in axi_signals:
        if direction == "output":
            # Connect demuxers outputs
            for port_idx in range(NUM_SUBORDINATES):
                verilog_code += f"""
   assign s{port_idx}_{signal}_o = demux_{signal}[{port_idx}*{width}+:{width}];
"""
        elif signal in ["axi_araddr", "axi_awaddr"]:
            # Connect address muxer inputs
            verilog_code += f"   assign mux_{signal} = {{"
            for port_idx in range(NUM_SUBORDINATES - 1, -1, -1):
                verilog_code += f"{{{NBITS}'d{port_idx}}}, s{port_idx}_{signal}_i, "
            verilog_code = verilog_code[:-2] + "};\n"
        else:  # Input direction
            # Connect muxer inputs
            verilog_code += f"   assign mux_{signal} = {{"
            for port_idx in range(NUM_SUBORDINATES - 1, -1, -1):
                verilog_code += f"s{port_idx}_{signal}_i, "
            verilog_code = verilog_code[:-2] + "};\n"
    # Create snippet with muxer and demuxer connections
    attributes_dict["snippets"] += [
        {
            "verilog_code": verilog_code,
        },
    ]

    return attributes_dict
