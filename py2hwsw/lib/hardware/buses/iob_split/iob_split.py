# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["name"] = os.path.basename(__file__)
        py_params_dict["num_managers"] = 2

    assert "name" in py_params_dict, print(
        "Error: Missing name for generated split module."
    )
    assert "num_managers" in py_params_dict, print(
        "Error: Missing number of manager interfaces for generated split module."
    )

    NUM_MANAGERS = int(py_params_dict["num_managers"])
    # Number of bits required for output selection
    NBITS = (NUM_MANAGERS - 1).bit_length()

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
                "name": "s_s",
                "descr": "Split subordinate interface",
                "signals": {
                    "type": "iob",
                    "prefix": "s_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W,
                },
            },
        ],
    }
    for port_idx in range(NUM_MANAGERS):
        attributes_dict["ports"].append(
            {
                "name": f"m_{port_idx}_m",
                "descr": "Split manager interface",
                "signals": {
                    "type": "iob",
                    # "file_prefix": f"{py_params_dict['name']}_m{port_idx}_",
                    "prefix": f"m{port_idx}_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W - NBITS,
                },
            },
        )
    attributes_dict["wires"] = [
        # manager selection signals
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
            "name": "manager_sel",
            "descr": "Select manager interface",
            "signals": [
                {"name": "sel"},
            ],
        },
        {
            "name": "manager_sel_reg",
            "descr": "Registered select manager interface",
            "signals": [
                {"name": "sel_reg"},
            ],
        },
        # Demux signals
        {
            "name": "demux_valid_data_i",
            "descr": "Input of valid demux",
            "signals": [
                {"name": "s_iob_valid_int", "width": 1},
            ],
        },
        {
            "name": "demux_valid_data_o",
            "descr": "Output of valid demux",
            "signals": [
                {"name": "demux_valid_output", "width": NUM_MANAGERS},
            ],
        },
        {
            "name": "demux_addr_data_i",
            "descr": "Input of address demux",
            "signals": [
                {"name": "s_iob_addr_i"},
            ],
        },
        {
            "name": "demux_addr_data_o",
            "descr": "Output of address demux",
            "signals": [
                {"name": "demux_addr_output", "width": NUM_MANAGERS * ADDR_W},
            ],
        },
        {
            "name": "demux_wdata_data_i",
            "descr": "Input of wdata demux",
            "signals": [
                {"name": "s_iob_wdata_i"},
            ],
        },
        {
            "name": "demux_wdata_data_o",
            "descr": "Output of wdata demux",
            "signals": [
                {"name": "demux_wdata_output", "width": NUM_MANAGERS * DATA_W},
            ],
        },
        {
            "name": "demux_wstrb_data_i",
            "descr": "Input of wstrb demux",
            "signals": [
                {"name": "s_iob_wstrb_i"},
            ],
        },
        {
            "name": "demux_wstrb_data_o",
            "descr": "Output of wstrb demux",
            "signals": [
                {"name": "demux_wstrb_output", "width": NUM_MANAGERS * int(DATA_W / 8)},
            ],
        },
        # Mux signals
        {
            "name": "mux_rdata_data_i",
            "descr": "Input of rdata mux",
            "signals": [
                {"name": "mux_rdata_input", "width": NUM_MANAGERS * DATA_W},
            ],
        },
        {
            "name": "mux_rdata_data_o",
            "descr": "Output of rdata mux",
            "signals": [
                {"name": "s_iob_rdata_o"},
            ],
        },
        {
            "name": "mux_rvalid_data_i",
            "descr": "Input of rvalid mux",
            "signals": [
                {"name": "mux_rvalid_input", "width": NUM_MANAGERS},
            ],
        },
        {
            "name": "mux_rvalid_data_o",
            "descr": "Output of rvalid mux",
            "signals": [
                {"name": "s_iob_rvalid_o"},
            ],
        },
        {
            "name": "mux_ready_data_i",
            "descr": "Input of ready mux",
            "signals": [
                {"name": "mux_ready_input", "width": NUM_MANAGERS},
            ],
        },
        {
            "name": "mux_ready_data_o",
            "descr": "Output of ready mux",
            "signals": [
                {"name": "s_iob_ready_int", "width": 1},
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
        # Demuxers
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_valid",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel",
                "data_i": "demux_valid_data_i",
                "data_o": "demux_valid_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_addr",
            "parameters": {
                "DATA_W": ADDR_W,
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel",
                "data_i": "demux_addr_data_i",
                "data_o": "demux_addr_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_wdata",
            "parameters": {
                "DATA_W": DATA_W,
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel",
                "data_i": "demux_wdata_data_i",
                "data_o": "demux_wdata_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_wstrb",
            "parameters": {
                "DATA_W": int(DATA_W / 8),
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel",
                "data_i": "demux_wstrb_data_i",
                "data_o": "demux_wstrb_data_o",
            },
        },
        # Muxers
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_rdata",
            "parameters": {
                "DATA_W": DATA_W,
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel_reg",
                "data_i": "mux_rdata_data_i",
                "data_o": "mux_rdata_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_rvalid",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_MANAGERS,
            },
            "connect": {
                "sel_i": "manager_sel_reg",
                "data_i": "mux_rvalid_data_i",
                "data_o": "mux_rvalid_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_ready",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_MANAGERS,
            },
            "connect": {
                # Ready selection must not be registered
                "sel_i": "manager_sel",
                "data_i": "mux_ready_data_i",
                "data_o": "mux_ready_data_o",
            },
        },
    ]

    # Connect demuxers outputs
    verilog_code = ""
    for port_idx in range(NUM_MANAGERS):
        verilog_code += f"""
    assign m{port_idx}_iob_valid_o = demux_valid_output[{port_idx}+:1];
    assign m{port_idx}_iob_addr_o = demux_addr_output[{port_idx*ADDR_W}+:{ADDR_W-NBITS}];
    assign m{port_idx}_iob_wdata_o = demux_wdata_output[{port_idx*DATA_W}+:{DATA_W}];
    assign m{port_idx}_iob_wstrb_o = demux_wstrb_output[{port_idx*int(DATA_W/8)}+:{int(DATA_W/8)}];
"""
    verilog_code += "\n"
    # Connect muxer inputs
    for signal in ["rdata", "rvalid", "ready"]:
        verilog_code += f"    assign mux_{signal}_input = {{"
        for port_idx in range(NUM_MANAGERS - 1, -1, -1):
            verilog_code += f"m{port_idx}_iob_{signal}_i, "
        verilog_code = verilog_code[:-2] + "};\n"
    # Create snippet with muxer and demuxer connections
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
   sel = sel_reg;

   // Disallow handshake signals from going through
   s_iob_valid_int = 1'b0;
   s_iob_ready_o = 1'b0;
""",
        "state_descriptions": """
   WAIT_VALID: // Wait for valid data
      // Allow handshake signals to go through
      s_iob_valid_int = s_iob_valid_i;
      s_iob_ready_o = s_iob_ready_int;
"""
        + f"""\
      // Allow selector to be changed
      sel = s_iob_addr_i[{ADDR_W-1}-:{NBITS}];
"""
        + """\
      if (s_iob_valid_i && ~s_iob_ready_o) begin
          // If not ready, wait for ready
         state_nxt = WAIT_READY;
      end else if (s_iob_valid_i && !s_iob_wstrb_i && ~s_iob_rvalid_o) begin
          // If read (and ready) and not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end

   WAIT_READY: // Wait for ready signal
      // Allow handshake signals to go through
      s_iob_valid_int = s_iob_valid_i;
      s_iob_ready_o = s_iob_ready_int;
      if (s_iob_ready_o && |s_iob_wstrb_i) begin
         // If write and ready, transaction complete
         state_nxt = WAIT_VALID;
      end else if (s_iob_ready_o && !s_iob_wstrb_i && s_iob_rvalid_o) begin
         // If read and ready and rvalid, transaction complete
         state_nxt = WAIT_VALID;
      end else if (s_iob_ready_o && !s_iob_wstrb_i) begin
         // If read and ready but not rvalid, wait for rvalid
         state_nxt = WAIT_RVALID;
      end

   WAIT_RVALID: // Wait for read data
      if (s_iob_rvalid_o) begin
         state_nxt = WAIT_VALID;
      end
""",
    }

    return attributes_dict
