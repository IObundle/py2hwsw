# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # Check if should create a demonstation of this core
    if py_params_dict.get("demo", False):
        py_params_dict["name"] = os.path.basename(__file__)
        py_params_dict["num_inputs"] = 2

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

    attributes_dict = {
        "name": py_params_dict["name"],
        "generate_hw": True,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and async reset",
            },
            {
                "name": "reset_i",
                "descr": "Reset wire",
                "wires": [
                    {
                        "name": "rst_i",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "output_m",
                "wires": {
                    "type": "iob",
                    "file_prefix": py_params_dict["name"] + "_output_",
                    "prefix": "output_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W,
                },
                "descr": "Merge output",
            },
        ],
    }
    for port_idx in range(NUM_INPUTS):
        attributes_dict["ports"].append(
            {
                "name": f"input_{port_idx}_s",
                "wires": {
                    "type": "iob",
                    "file_prefix": f"{py_params_dict['name']}_input{port_idx}_",
                    "prefix": f"input{port_idx}_",
                    "DATA_W": DATA_W,
                    "ADDR_W": ADDR_W - NBITS,
                },
                "descr": "Merge input interfaces",
            },
        )
    attributes_dict["buses"] = [
        # Output selection wires
        {
            "name": "sel_reg_rst",
            "descr": "Enable and reset wire for sel_reg",
            "wires": [
                {"name": "rst_i"},
            ],
        },
        {
            "name": "sel_reg_data_i",
            "descr": "Input of sel_reg",
            "wires": [
                {"name": "sel", "width": NBITS},
            ],
        },
        {
            "name": "sel_reg_data_o",
            "descr": "Output of sel_reg",
            "wires": [
                {"name": "sel_reg", "width": NBITS},
            ],
        },
        {
            "name": "input_sel",
            "descr": "Select output interface",
            "wires": [
                {"name": "sel"},
            ],
        },
        {
            "name": "input_sel_reg",
            "descr": "Registered select output interface",
            "wires": [
                {"name": "sel_reg"},
            ],
        },
        # Mux wires
        {
            "name": "mux_valid_data_i",
            "descr": "Input of valid mux",
            "wires": [
                {"name": "mux_valid_input", "width": NUM_INPUTS},
            ],
        },
        {
            "name": "mux_valid_data_o",
            "descr": "Output of valid mux",
            "wires": [
                {"name": "output_iob_valid_o"},
            ],
        },
        {
            "name": "mux_addr_data_i",
            "descr": "Input of address mux",
            "wires": [
                {"name": "mux_addr_input", "width": NUM_INPUTS * ADDR_W},
            ],
        },
        {
            "name": "mux_addr_data_o",
            "descr": "Output of address mux",
            "wires": [
                {"name": "output_iob_addr_o"},
            ],
        },
        {
            "name": "mux_wdata_data_i",
            "descr": "Input of wdata mux",
            "wires": [
                {"name": "mux_wdata_input", "width": NUM_INPUTS * DATA_W},
            ],
        },
        {
            "name": "mux_wdata_data_o",
            "descr": "Output of wdata mux",
            "wires": [
                {"name": "output_iob_wdata_o"},
            ],
        },
        {
            "name": "mux_wstrb_data_i",
            "descr": "Input of wstrb mux",
            "wires": [
                {"name": "mux_wstrb_input", "width": NUM_INPUTS * int(DATA_W / 8)},
            ],
        },
        {
            "name": "mux_wstrb_data_o",
            "descr": "Output of wstrb mux",
            "wires": [
                {"name": "output_iob_wstrb_o"},
            ],
        },
        # Demux wires
        {
            "name": "demux_rdata_data_i",
            "descr": "Input of rdata demux",
            "wires": [
                {"name": "output_iob_rdata_i"},
            ],
        },
        {
            "name": "demux_rdata_data_o",
            "descr": "Output of rdata demux",
            "wires": [
                {"name": "demux_rdata_output", "width": NUM_INPUTS * DATA_W},
            ],
        },
        {
            "name": "demux_rvalid_data_i",
            "descr": "Input of rvalid demux",
            "wires": [
                {"name": "output_iob_rvalid_i"},
            ],
        },
        {
            "name": "demux_rvalid_data_o",
            "descr": "Output of rvalid demux",
            "wires": [
                {"name": "demux_rvalid_output", "width": NUM_INPUTS},
            ],
        },
        {
            "name": "demux_ready_data_i",
            "descr": "Input of ready demux",
            "wires": [
                {"name": "output_iob_ready_i"},
            ],
        },
        {
            "name": "demux_ready_data_o",
            "descr": "Output of ready demux",
            "wires": [
                {"name": "demux_ready_output", "width": NUM_INPUTS},
            ],
        },
        # Priority encoder wires
        {
            "name": "prio_enc_i",
            "descr": "Input of priority encoder",
            "wires": [
                {"name": "mux_valid_input"},
            ],
        },
        {
            "name": "prio_enc_o",
            "descr": "Output of priority encoder",
            "wires": [
                {"name": "sel"},
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
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel",
                "data_i": "mux_valid_data_i",
                "data_o": "mux_valid_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_addr",
            "parameters": {
                "DATA_W": ADDR_W,
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel",
                "data_i": "mux_addr_data_i",
                "data_o": "mux_addr_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_wdata",
            "parameters": {
                "DATA_W": DATA_W,
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel",
                "data_i": "mux_wdata_data_i",
                "data_o": "mux_wdata_data_o",
            },
        },
        {
            "core_name": "iob_mux",
            "instance_name": "iob_mux_wstrb",
            "parameters": {
                "DATA_W": int(DATA_W / 8),
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel",
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
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel_reg",
                "data_i": "demux_rdata_data_i",
                "data_o": "demux_rdata_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_rvalid",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_INPUTS,
            },
            "connect": {
                "sel_i": "input_sel_reg",
                "data_i": "demux_rvalid_data_i",
                "data_o": "demux_rvalid_data_o",
            },
        },
        {
            "core_name": "iob_demux",
            "instance_name": "iob_demux_ready",
            "parameters": {
                "DATA_W": 1,
                "N": NUM_INPUTS,
            },
            "connect": {
                # Ready selection must not be registered
                "sel_i": "input_sel",
                "data_i": "demux_ready_data_i",
                "data_o": "demux_ready_data_o",
            },
        },
        # priority encoder
        {
            "core_name": "iob_prio_enc",
            "instance_name": "sel_enc",
            "parameters": {
                "W": NUM_INPUTS,
                "MODE": '"HIGH"',
            },
            "connect": {
                "unencoded_i": "prio_enc_i",
                "encoded_o": "prio_enc_o",
            },
        },
    ]

    # Connect demuxer outputs
    verilog_code = ""
    verilog_outputs = []
    for port_idx in range(NUM_INPUTS):
        verilog_code += f"""
    assign input{port_idx}_iob_rdata_o = demux_rdata_output[{port_idx*DATA_W}+:{DATA_W}];
    assign input{port_idx}_iob_rvalid_o = demux_rvalid_output[{port_idx}+:1];
    assign input{port_idx}_iob_ready_o = demux_ready_output[{port_idx}+:1];
"""
        verilog_outputs.append(f"input{port_idx}_iob_rdata")
        verilog_outputs.append(f"input{port_idx}_iob_rvalid")
        verilog_outputs.append(f"input{port_idx}_iob_ready")
    verilog_code += "\n"
    # Connect muxer inputs
    for wire in ["valid", "addr", "wdata", "wstrb"]:
        verilog_code += f"    assign mux_{wire}_input = {{"
        for port_idx in range(NUM_INPUTS - 1, -1, -1):
            # Include padding bits for address
            if wire == "addr":
                verilog_code += f"{{{NBITS}{{1'b0}}}}, "
            verilog_code += f"input{port_idx}_iob_{wire}_i, "
        verilog_code = verilog_code[:-2] + "};\n"
        verilog_outputs.append(f"mux_{wire}_input")
    # Create snippet with demuxer and muxer connections
    attributes_dict["snippets"] = [
        {
            "verilog_code": verilog_code,
        },
    ]

    return attributes_dict
