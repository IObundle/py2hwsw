# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        #
        # Confs
        #
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "ADDR_W",
                "descr": "ADDR width",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "READ_BYTES",
                "descr": "",
                "type": "P",
                "val": "4",
                "min": "NA",
                "max": "NA",
            },
        ],
        #
        # Ports
        #
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "iob_s",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "IOb native subordinate interface",
            },
            {
                "name": "wb_m",
                "signals": {
                    "type": "wb",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "Wishbone manager interface",
            },
        ],
        #
        # Wires
        #
        "wires": [
            # Reg valid
            {
                "name": "valid_data_i",
                "descr": "valid intput wire",
                "signals": [
                    {"name": "iob_valid_i"},
                ],
            },
            {
                "name": "valid_data_o",
                "descr": "valid output wire",
                "signals": [
                    {"name": "iob_valid_r", "width": 1},
                ],
            },
            # Reg addr
            {
                "name": "addr_data_i",
                "descr": "addr intput wire",
                "signals": [
                    {"name": "iob_addr_i"},
                ],
            },
            {
                "name": "addr_data_o",
                "descr": "addr output wire",
                "signals": [
                    {"name": "iob_address_r", "width": "ADDR_W"},
                ],
            },
            # Reg data
            {
                "name": "data_data_i",
                "descr": "data intput wire",
                "signals": [
                    {"name": "iob_wdata_i"},
                ],
            },
            {
                "name": "data_data_o",
                "descr": "data output wire",
                "signals": [
                    {"name": "iob_wdata_r", "width": "DATA_W"},
                ],
            },
            # Reg we
            {
                "name": "we_data_i",
                "descr": "we intput wire",
                "signals": [
                    {"name": "wb_we", "width": 1},
                ],
            },
            {
                "name": "we_data_o",
                "descr": "we output wire",
                "signals": [
                    {"name": "wb_we_r", "width": 1},
                ],
            },
            # Reg strb
            {
                "name": "strb_data_i",
                "descr": "strb intput wire",
                "signals": [
                    {"name": "wb_select", "width": "DATA_W/8"},
                ],
            },
            {
                "name": "strb_data_o",
                "descr": "strb output wire",
                "signals": [
                    {"name": "wb_select_r", "width": "DATA_W/8"},
                ],
            },
            # Reg wb_data
            {
                "name": "wb_data_data_i",
                "descr": "wb_data intput wire",
                "signals": [
                    {"name": "wb_dat_i"},
                ],
            },
            {
                "name": "wb_data_data_o",
                "descr": "wb_data output wire",
                "signals": [
                    {"name": "wb_data_r", "width": "DATA_W"},
                ],
            },
            # Reg wb_ack
            {
                "name": "wb_ack_data_i",
                "descr": "wb_ack intput wire",
                "signals": [
                    {"name": "wb_ack_i"},
                ],
            },
            {
                "name": "wb_ack_data_o",
                "descr": "wb_ack output wire",
                "signals": [
                    {"name": "wb_ack_r", "width": 1},
                ],
            },
        ],
    }
    #
    # Subblocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_valid",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_rst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:iob_valid_i",
                        "rst_i:wb_ack_i",
                    ],
                ),
                "data_i": "valid_data_i",
                "data_o": "valid_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_addr",
            "parameters": {
                "DATA_W": "ADDR_W",
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:iob_valid_i",
                    ],
                ),
                "data_i": "addr_data_i",
                "data_o": "addr_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_data",
            "parameters": {
                "DATA_W": "DATA_W",
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:iob_valid_i",
                    ],
                ),
                "data_i": "data_data_i",
                "data_o": "data_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_we",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:iob_valid_i",
                    ],
                ),
                "data_i": "we_data_i",
                "data_o": "we_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_strb",
            "parameters": {
                "DATA_W": "DATA_W/8",
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:iob_valid_i",
                    ],
                ),
                "data_i": "strb_data_i",
                "data_o": "strb_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_wb_data",
            "parameters": {
                "DATA_W": "DATA_W",
                "RST_VAL": 0,
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "data_i": "wb_data_data_i",
                "data_o": "wb_data_data_o",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "iob_reg_wb_ack",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": 0,
            },
            "port_params": {
                "clk_en_rst_s": "cke_arst_rst_en",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:wb_ack_i",
                        "rst_i:iob_rready_i",
                    ],
                ),
                "data_i": "wb_ack_data_i",
                "data_o": "wb_ack_data_o",
            },
        },
    ]
    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
   // Logic
   assign wb_adr_o     = iob_valid_i ? iob_addr_i : iob_address_r;
   assign wb_datout_o  = iob_valid_i ? iob_wdata_i : iob_wdata_r;
   assign wb_sel_o     = iob_valid_i ? wb_select : wb_select_r;
   assign wb_we_o      = iob_valid_i ? wb_we : wb_we_r;
   assign wb_cyc_o     = iob_valid_i ? iob_valid_i : iob_valid_r;
   assign wb_stb_o     = wb_cyc_o;

   assign wb_select    = wb_we ? iob_wstrb_i : {READ_BYTES{1'b1}};
   assign wb_we        = |iob_wstrb_i;

   assign iob_rvalid_o = wb_ack_i ? wb_ack_i & (~wb_we_r) : wb_ack_r ;
   assign iob_rdata_o  = wb_ack_i ? wb_dat_i : wb_data_r;
   assign iob_ready_o  = wb_ack_i;
""",
        },
    ]

    return attributes_dict
