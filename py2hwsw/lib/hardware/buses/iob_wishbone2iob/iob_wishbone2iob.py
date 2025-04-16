# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "ADDR width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "iob_m",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "IOb native manager interface",
            },
            {
                "name": "wb_s",
                "signals": {
                    "type": "wb",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "Wishbone subordinate interface",
            },
        ],
        "wires": [
            {
                "name": "valid_int",
                "descr": "valid_int wire",
                "signals": [
                    {"name": "valid_int", "width": 1},
                ],
            },
            {
                "name": "valid_r",
                "descr": "valid_r wire",
                "signals": [
                    {"name": "valid_r", "width": 1},
                ],
            },
            {
                "name": "rst_valid",
                "descr": "rst_valid wire",
                "signals": [
                    {"name": "rst_valid", "width": 1},
                ],
            },
            {
                "name": "wstrb",
                "descr": "wstrb wire",
                "signals": [
                    {"name": "wstrb", "width": "DATA_W/8"},
                ],
            },
            {
                "name": "wack",
                "descr": "wack wire",
                "signals": [
                    {"name": "wack", "width": 1},
                ],
            },
            {
                "name": "wack_r",
                "descr": "wack_r wire",
                "signals": [
                    {"name": "wack_r", "width": 1},
                ],
            },
            {
                "name": "wb_data_mask",
                "descr": "wb_data_mask wire",
                "signals": [
                    {"name": "wb_data_mask", "width": "DATA_W"},
                ],
            },
            # Busy reg
            {
                "name": "busy",
                "descr": "busy wire",
                "signals": [
                    {"name": "busy", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_wack",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "wack",
                    "data_o": "wack_r",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_valid",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:valid_int",
                            "rst_i:rst_valid",
                        ],
                    ),
                    "data_i": "valid_int",
                    "data_o": "valid_r",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_busy",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i:valid_int",
                            "rst_i:wb_ack_o",
                        ],
                    ),
                    "data_i": "valid_int",
                    "data_o": "busy",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   assign iob_valid_o = ~busy ? valid_int : valid_r;
   assign valid_int = wb_stb_i & wb_cyc_i & ~busy;
   assign rst_valid = iob_ready_i;

   assign iob_addr_o = wb_adr_i;
   assign iob_wdata_o = wb_datout_i;
   assign iob_wstrb_o = wstrb;
   assign wstrb = wb_we_i ? wb_sel_i : 4'h0;
   assign iob_rready_o = 1'b1;

   assign wb_dat_o = (iob_rdata_i) & (wb_data_mask);
   assign wb_data_mask = {{8{wb_sel_i[3]}}, {8{wb_sel_i[2]}}, {8{wb_sel_i[1]}}, {8{wb_sel_i[0]}}};

   assign wb_ack_o = wb_we_i ? iob_ready_i : iob_rvalid_i;
""",
            },
        ],
    }

    return attributes_dict
