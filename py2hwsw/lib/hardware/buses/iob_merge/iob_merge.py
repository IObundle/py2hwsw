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
        "Error: Missing number of subordinate interfaces for generated merge module."
    )

    NUM_SUBORDINATES = int(py_params_dict["num_subordinates"])
    # Number of bits required for input selection
    NBITS = (NUM_SUBORDINATES - 1).bit_length()

    ADDR_W = int(py_params_dict["addr_w"]) if "addr_w" in py_params_dict else 32
    DATA_W = int(py_params_dict["data_w"]) if "data_w" in py_params_dict else 32

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
        "ports": [
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
                "descr": "Merge manager interface",
                "signals": {
                    "type": "iob",
                    "prefix": "m_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W,
                },
            },
        ],
    }
    for port_idx in range(NUM_SUBORDINATES):
        attributes_dict["ports"].append(
            {
                "name": f"s_{port_idx}_s",
                "descr": "Merge subordinate interface",
                "signals": {
                    "type": "iob",
                    # "file_prefix": f"{py_params_dict['name']}_s{port_idx}_",
                    "prefix": f"s{port_idx}_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W - NBITS,
                },
            },
        )
    attributes_dict["wires"] = [
        # subordinate selection signals
        {
            "name": "sel_reg_data_i",
            "descr": "Input of sel_reg",
            "signals": [
                {"name": "sel", "width": NBITS},
            ],
        },
        {
            "name": "sel_reg_data_o",
            "descr": "Output of sel_reg",
            "signals": [
                {"name": "sel_reg", "width": NBITS},
            ],
        },
        {
            "name": "subordinate_sel",
            "descr": "Select subordinate interface",
            "signals": [
                {"name": "sel"},
            ],
        },
        {
            "name": "subordinate_sel_reg",
            "descr": "Registered select subordinate interface",
            "signals": [
                {"name": "sel_reg"},
            ],
        },
        # Mux signals
        {
            "name": "mux_valid_data_i",
            "descr": "Input of valid mux",
            "signals": [
                {"name": "mux_valid_input", "width": NUM_SUBORDINATES},
            ],
        },
        {
            "name": "mux_valid_data_o",
            "descr": "Output of valid mux",
            "signals": [
                {"name": "m_iob_valid_int", "width": 1},
            ],
        },
        {
            "name": "mux_addr_data_i",
            "descr": "Input of address mux",
            "signals": [
                {"name": "mux_addr_input", "width": NUM_SUBORDINATES * ADDR_W},
            ],
        },
        {
            "name": "mux_addr_data_o",
            "descr": "Output of address mux",
            "signals": [
                {"name": "m_iob_addr_o"},
            ],
        },
        {
            "name": "mux_wdata_data_i",
            "descr": "Input of wdata mux",
            "signals": [
                {"name": "mux_wdata_input", "width": NUM_SUBORDINATES * DATA_W},
            ],
        },
        {
            "name": "mux_wdata_data_o",
            "descr": "Output of wdata mux",
            "signals": [
                {"name": "m_iob_wdata_o"},
            ],
        },
        {
            "name": "mux_wstrb_data_i",
            "descr": "Input of wstrb mux",
            "signals": [
                {
                    "name": "mux_wstrb_input",
                    "width": NUM_SUBORDINATES * int(DATA_W / 8),
                },
            ],
        },
        {
            "name": "mux_wstrb_data_o",
            "descr": "Output of wstrb mux",
            "signals": [
                {"name": "m_iob_wstrb_o"},
            ],
        },
        # Demux signals
        {
            "name": "demux_rdata_data_i",
            "descr": "Input of rdata demux",
            "signals": [
                {"name": "m_iob_rdata_i"},
            ],
        },
        {
            "name": "demux_rdata_data_o",
            "descr": "Output of rdata demux",
            "signals": [
                {"name": "demux_rdata_manager", "width": NUM_SUBORDINATES * DATA_W},
            ],
        },
        {
            "name": "demux_rvalid_data_i",
            "descr": "Input of rvalid demux",
            "signals": [
                {"name": "m_iob_rvalid_i"},
            ],
        },
        {
            "name": "demux_rvalid_data_o",
            "descr": "Output of rvalid demux",
            "signals": [
                {"name": "demux_rvalid_manager", "width": NUM_SUBORDINATES},
            ],
        },
        {
            "name": "demux_ready_data_i",
            "descr": "Input of ready demux",
            "signals": [
                {"name": "m_iob_ready_int", "width": 1},
            ],
        },
        {
            "name": "demux_ready_data_o",
            "descr": "Output of ready demux",
            "signals": [
                {"name": "demux_ready_manager", "width": NUM_SUBORDINATES},
            ],
        },
        # Priority encoder signals
        {
            "name": "prio_enc_i",
            "descr": "Input of priority encoder",
            "signals": [
                {"name": "mux_valid_input"},
            ],
        },
        {
            "name": "prio_enc_o",
            "descr": "Output of priority encoder",
            "signals": [
                {"name": "prio_enc_o", "width": NUM_SUBORDINATES.bit_length()},
            ],
        },
    ]
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_reg",
            "instance_name": "sel_reg_r",
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
                "data_i": "sel_reg_data_i",
                "data_o": "sel_reg_data_o",
            },
        },
        # muxers
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_valid",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel",
                "data_i": "mux_valid_data_i",
                "data_o": "mux_valid_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_addr",
            "parameters": {
                "DATA_W": ADDR_W,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel",
                "data_i": "mux_addr_data_i",
                "data_o": "mux_addr_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_wdata",
            "parameters": {
                "DATA_W": DATA_W,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel",
                "data_i": "mux_wdata_data_i",
                "data_o": "mux_wdata_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_wstrb",
            "parameters": {
                "DATA_W": int(DATA_W / 8),
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel",
                "data_i": "mux_wstrb_data_i",
                "data_o": "mux_wstrb_data_o",
            },
        },
        # demuxers
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_rdata",
            "parameters": {
                "DATA_W": DATA_W,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel_reg",
                "data_i": "demux_rdata_data_i",
                "data_o": "demux_rdata_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_rvalid",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                "sel_i": "subordinate_sel_reg",
                "data_i": "demux_rvalid_data_i",
                "data_o": "demux_rvalid_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_ready",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_SUBORDINATES,
            },
            "connect": {
                # Ready selection must not be registered
                "sel_i": "subordinate_sel",
                "data_i": "demux_ready_data_i",
                "data_o": "demux_ready_data_o",
            },
        },
        # priority encoder
        {
            "core_name": "iob_prio_enc",
            "instance_name": "sel_enc",
            "parameters": {
                "W": NUM_SUBORDINATES,
                "MODE": '"HIGH"',
            },
            "connect": {
                "unencoded_i": "prio_enc_i",
                "encoded_o": "prio_enc_o",
            },
        },
    ]

    verilog_code = ""

    # Connect demuxer managers
    verilog_managers = []
    for port_idx in range(NUM_SUBORDINATES):
        verilog_code += f"""
    assign s{port_idx}_iob_rdata_o = demux_rdata_manager[{port_idx*DATA_W}+:{DATA_W}];
    assign s{port_idx}_iob_rvalid_o = demux_rvalid_manager[{port_idx}+:1];
    assign s{port_idx}_iob_ready_o = demux_ready_manager[{port_idx}+:1];
"""
        verilog_managers.append(f"s{port_idx}_iob_rdata")
        verilog_managers.append(f"s{port_idx}_iob_rvalid")
        verilog_managers.append(f"s{port_idx}_iob_ready")
    verilog_code += "\n"
    # Connect muxer inputs
    for signal in ["valid", "addr", "wdata", "wstrb"]:
        verilog_code += f"    assign mux_{signal}_input = {{"
        for port_idx in range(NUM_SUBORDINATES - 1, -1, -1):
            # Include padding bits for address
            if signal == "addr":
                verilog_code += f"{{{NBITS}{{1'b0}}}}, "
            verilog_code += f"s{port_idx}_iob_{signal}_i, "
        verilog_code = verilog_code[:-2] + "};\n"
        verilog_managers.append(f"mux_{signal}_input")

    # NOTE: Assigned 'sel' signal here, because it was causing an infinite loop when assigned in the FSM
    verilog_code += f"""
    assign sel = state == WAIT_VALID ? prio_enc_o[{NBITS}-1:0] : sel_reg;
"""

    # Create snippet with demuxer and muxer connections
    attributes_dict["snippets"] = [
        {
            "verilog_code": verilog_code,
        },
    ]

    #
    # FSM
    #
    attributes_dict["fsm"] = {
        "type": "fsm",
        "default_assignments": """
   // Default assignments
   // sel <- sel_reg;

   // Disallow handshake signals from going through
   m_iob_valid_o = 1'b0;
   m_iob_ready_int = 1'b0;
""",
        "state_descriptions": """
   WAIT_VALID: // Wait for valid data
      // Allow handshake signals to go through
      m_iob_valid_o = m_iob_valid_int;
      m_iob_ready_int = m_iob_ready_i;
"""
        + f"""\
      // Allow selector to be changed
      // Priority encoder may have 1 more bit to signal 'no input', but we don't use it for selection.
      // sel <- prio_enc_o[{NBITS}-1:0];
"""
        + """\
      if (m_iob_valid_o && ~m_iob_ready_i) begin
          // If not ready, wait for ready
         state_nxt = WAIT_READY;
      end else if (m_iob_valid_o && !m_iob_wstrb_o && ~m_iob_rvalid_i) begin
          // If read (and ready) and not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end

   WAIT_READY: // Wait for ready signal
      // Allow handshake signals to go through
      m_iob_valid_o = m_iob_valid_int;
      m_iob_ready_int = m_iob_ready_i;
      if (m_iob_ready_i && |m_iob_wstrb_o) begin
         // If write and ready, transaction complete
         state_nxt = WAIT_VALID;
      end else if (m_iob_ready_i && !m_iob_wstrb_o && m_iob_rvalid_i) begin
         // If read and ready and rvalid, transaction complete
         state_nxt = WAIT_VALID;
      end else if (m_iob_ready_i && !m_iob_wstrb_o) begin
         // If read and ready but not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end

   WAIT_RVALID: // Wait for read data
      if (m_iob_rvalid_i) begin
         state_nxt = WAIT_VALID;
      end
""",
    }

    return attributes_dict
