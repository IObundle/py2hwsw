# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# Copied from py2 'board.py'
bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "50000000"},
    {"name": "IOB_MEM_NO_READ_ON_WRITE", "type": "M", "val": "1"},
    {"name": "DDR_DATA_W", "type": "M", "val": "32"},
    {"name": "DDR_ADDR_W", "type": "M", "val": "28"},
    {"name": "INTEL", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_cyclonev_gt_dk",
        "version": "0.1",
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "F",
                "val": "1",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "F",
                "val": "4",
                "min": "1",
                "max": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "F",
                "val": "`DDR_ADDR_W",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "F",
                "val": "`DDR_DATA_W",
                "min": "1",
                "max": "32",
            },
        ]
        + bsp,
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_rst_i",
            "descr": "Clock and reset",
            "signals": [
                {"name": "clk_i", "width": "1"},
                {"name": "resetn_i", "width": "1"},
            ],
        },
        {
            "name": "rs232_io",
            "descr": "Serial port",
            "signals": [
                {"name": "txd_o", "width": "1"},
                {"name": "rxd_i", "width": "1"},
            ],
        },
    ]
    if params["use_extmem"]:
        attributes_dict["ports"] += [
            {
                "name": "ddr3_io",
                "descr": "External DDR3 memory interface",
                "signals": [
                    {"name": "ddr3b_a_o", "width": "14"},
                    {"name": "ddr3b_ba_o", "width": "3"},
                    {"name": "ddr3b_rasn_o", "width": "1"},
                    {"name": "ddr3b_casn_o", "width": "1"},
                    {"name": "ddr3b_wen_o", "width": "1"},
                    {"name": "ddr3b_dm_o", "width": "2"},
                    {"name": "ddr3b_dq_io", "width": "16"},
                    {"name": "ddr3b_clk_n_o", "width": "1"},
                    {"name": "ddr3b_clk_p_o", "width": "1"},
                    {"name": "ddr3b_cke_o", "width": "1"},
                    {"name": "ddr3b_csn_o", "width": "1"},
                    {"name": "ddr3b_dqs_n_io", "width": "2"},
                    {"name": "ddr3b_dqs_p_io", "width": "2"},
                    {"name": "ddr3b_odt_o", "width": "1"},
                    {"name": "ddr3b_resetn_o", "width": "1"},
                ],
            },
            {
                "name": "rzqin_i",
                "descr": "",
                "signals": [
                    {"name": "rzqin_i", "width": "1"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["ports"] += [
            {
                "name": "mii_io",
                "descr": "MII ethernet interface",
                "signals": [
                    {"name": "enet_resetn_o", "width": "1"},
                    {"name": "enet_rx_clk_i", "width": "1"},
                    {"name": "enet_gtx_clk_o", "width": "1"},
                    {"name": "enet_rx_d0_i", "width": "1"},
                    {"name": "enet_rx_d1_i", "width": "1"},
                    {"name": "enet_rx_d2_i", "width": "1"},
                    {"name": "enet_rx_d3_i", "width": "1"},
                    {"name": "enet_rx_dv_i", "width": "1"},
                    # {"name": "enet_rx_err_o", "width": "1"},
                    {"name": "enet_tx_d0_o", "width": "1"},
                    {"name": "enet_tx_d1_o", "width": "1"},
                    {"name": "enet_tx_d2_o", "width": "1"},
                    {"name": "enet_tx_d3_o", "width": "1"},
                    {"name": "enet_tx_en_o", "width": "1"},
                    # {"name": "enet_tx_err_o", "width": "1"},
                ],
            },
        ]

    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "signals": [
                {"name": "clk_i"},
                {"name": "cke", "width": "1"},
                {"name": "arst", "width": "1"},
            ],
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "signals": [
                {"name": "rxd_i"},
                {"name": "txd_o"},
                {"name": "rs232_rts", "width": "1"},
                {"name": "high", "width": "1"},
            ],
        },
        {
            "name": "reset_sync_clk_rst",
            "descr": "Reset synchronizer inputs",
            "signals": [
                {"name": "clk_i"},
                {
                    "name": "rst_int" if params["use_extmem"] else "resetn_inv",
                    "width": "1",
                },
            ],
        },
        {
            "name": "reset_sync_arst_out",
            "descr": "Reset synchronizer output",
            "signals": [
                {"name": "arst"},
            ],
        },
        {
            "name": "clk_i",
            "descr": "Clock signal",
            "signals": [
                {"name": "clk_i"},
            ],
        },
    ]

    if params["use_extmem"]:
        attributes_dict["wires"] += [
            {
                "name": "axi",
                "descr": "AXI interface to connect SoC to memory",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            # DDR3 ctrl
            {
                "name": "ddr3_ctr_clk_rst",
                "descr": "DDR3 controller clock and areset inputs",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "resetn_i"},
                ],
            },
            {
                "name": "ddr3_ctr_general",
                "descr": "DDR3 controller general signals",
                "signals": [
                    {"name": "rzqin_i"},
                    {"name": "pll_locked"},
                    {"name": "init_done"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["wires"] += [
            # eth clock
            {
                "name": "rxclk_buf_io",
                "descr": "rxclkbuf io",
                "signals": [
                    {"name": "enet_rx_clk"},
                    {"name": "eth_clk", "width": "1"},
                ],
            },
            {
                "name": "ddio_out_clkbuf_io",
                "descr": "DDIO clock buffer io",
                "signals": [
                    {"name": "enet_resetn_inv", "width": "1"},
                    {"name": "low", "width": "1"},
                    {"name": "high"},
                    {"name": "eth_clk"},
                    {"name": "enet_gtx_clk"},
                ],
            },
        ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_system_mwrap",
            "instance_name": "iob_system_mwrap",
            "instance_description": "IOb-SoC memory wrapper",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst",
                "rs232_m": "rs232_int",
            },
            "dest_dir": "hardware/common_src",
            "iob_system_params": params,
        },
    ]
    if params["use_extmem"]:
        attributes_dict["subblocks"][-1]["connect"].update({"axi_m": "axi"})
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_reset_sync",
            "instance_name": "rst_sync",
            "instance_description": "Reset synchronizer",
            "connect": {
                "clk_rst_s": "reset_sync_clk_rst",
                "arst_o": "reset_sync_arst_out",
            },
        },
    ]
    if params["use_extmem"]:
        # DDR3 controller
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_altera_alt_ddr3",
                "instance_name": "ddr3_ctrl",
                "instance_description": "DDR3 controller",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_rst_i": "ddr3_ctr_clk_rst",
                    "general_io": "ddr3_ctr_general",
                    "ddr3_io": "ddr3_io",
                    "s0_axi_s": (
                        "axi",
                        [
                            "{axi_araddr, 2'b0}",
                            "{axi_awaddr, 2'b0}",
                        ],
                    ),
                },
            },
        ]
    if params["use_ethernet"]:
        # Eth clock
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_altera_clk_buf_altclkctrl",
                "instance_name": "rxclk_buf",
                "instance_description": "RX clock buffer",
                "connect": {
                    "io_io": "rxclk_buf_io",
                },
            },
            {
                "core_name": "iob_altera_ddio_out_clkbuf",
                "instance_name": "ddio_out_clkbuf_inst",
                "instance_description": "DDIO out clock buffer",
                "connect": {
                    "io_io": "ddio_out_clkbuf_io",
                },
            },
        ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
    // General connections
    assign high = 1'b1;
    assign cke = 1'b1;
""",
        },
    ]
    if params["use_extmem"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
    assign rst_int = ~resetn_i | ~pll_locked | ~init_done;
""",
            },
        ]
    else:  # Not use_extmem
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
    assign resetn_inv = ~resetn_i;
""",
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
    // Ethernet connections
    assign low = 1'b0;
    assign enet_resetn_inv = ~enet_resetn_o;
""",
            },
        ]

    return attributes_dict
