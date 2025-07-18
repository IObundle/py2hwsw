# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_iob_cyclonev_gt_dk",
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                "val": "1",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "D",
                "val": "4",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "D",
                "val": "28",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "D",
                "val": "32",
            },
            {
                "name": "BAUD",
                "descr": "UART baud rate",
                "type": "D",
                "val": "115200",
            },
            {
                "name": "FREQ",
                "descr": "Clock frequency",
                "type": "D",
                "val": "50000000",
            },
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "descr": "No read on write flag",
                "type": "D",
                "val": "1",
            },
            {
                "name": "INTEL",
                "descr": "Intel flag",
                "type": "D",
                "val": "1",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_rst_i",
            "descr": "Clock and reset",
            "wires": [
                {"name": "clk_i", "width": "1"},
                {"name": "resetn_i", "width": "1"},
            ],
        },
        {
            "name": "rs232_io",
            "descr": "Serial port",
            "wires": [
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
                "wires": [
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
                "wires": [
                    {"name": "rzqin_i", "width": "1"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["ports"] += [
            {
                "name": "mii_io",
                "descr": "MII ethernet interface",
                "wires": [
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
    # Buses
    #
    attributes_dict["buses"] = [
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "wires": [
                {"name": "clk_i"},
                {"name": "cke", "width": "1"},
                {"name": "arst", "width": "1"},
            ],
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "wires": [
                {"name": "rxd_i"},
                {"name": "txd_o"},
                {"name": "rs232_rts", "width": "1"},
                {"name": "high", "width": "1"},
            ],
        },
        {
            "name": "reset_sync_clk_rst",
            "descr": "Reset synchronizer inputs",
            "wires": [
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
            "wires": [
                {"name": "arst"},
            ],
        },
        {
            "name": "clk_i",
            "descr": "Clock wire",
            "wires": [
                {"name": "clk_i"},
            ],
        },
    ]

    if params["use_extmem"]:
        attributes_dict["buses"] += [
            {
                "name": "axi",
                "descr": "AXI interface to connect SoC to memory",
                "wires": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            # DDR3 ctrl
            {
                "name": "ddr3_ctr_clk_rst",
                "descr": "DDR3 controller clock and areset inputs",
                "wires": [
                    {"name": "clk_i"},
                    {"name": "resetn_i"},
                ],
            },
            {
                "name": "ddr3_ctr_general",
                "descr": "DDR3 controller general wires",
                "wires": [
                    {"name": "rzqin_i"},
                    {"name": "pll_locked"},
                    {"name": "init_done"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["buses"] += [
            # eth clock
            {
                "name": "rxclk_buf_io",
                "descr": "rxclkbuf io",
                "wires": [
                    {"name": "enet_rx_clk_i"},
                    {"name": "eth_clk", "width": "1"},
                ],
            },
            {
                "name": "ddio_out_clkbuf_io",
                "descr": "DDIO clock buffer io",
                "wires": [
                    {"name": "enet_resetn_inv", "width": "1"},
                    {"name": "low", "width": "1"},
                    {"name": "high"},
                    {"name": "eth_clk"},
                    {"name": "enet_gtx_clk_o"},
                ],
            },
            {
                "name": "phy",
                "descr": "PHY Interface Ports",
                "wires": [
                    {"name": "eth_MTxClk", "width": "1"},
                    {"name": "MTxEn", "width": "1"},
                    {"name": "MTxD", "width": "4"},
                    {"name": "MTxErr", "width": "1"},
                    {"name": "eth_MRxClk", "width": "1"},
                    {"name": "MRxDv", "width": "1"},
                    {"name": "MRxD", "width": "4"},
                    {"name": "MRxErr", "width": "1"},
                    {"name": "eth_MColl", "width": "1"},
                    {"name": "eth_MCrS", "width": "1"},
                    {"name": "MDC", "width": "1"},
                    {"name": "MDIO", "width": "1"},
                    {"name": "phy_rstn", "width": "1"},
                ],
            },
        ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": py_params_dict["issuer"]["original_name"],
            "instance_name": py_params_dict["issuer"]["original_name"],
            "instance_description": "IOb-SoC memory wrapper",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "MEM_NO_READ_ON_WRITE": "MEM_NO_READ_ON_WRITE",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst",
                "rs232_m": "rs232_int",
            },
            "dest_dir": "hardware/common_src",
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["subblocks"][-1]["connect"].update({"phy_io": "phy"})
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
                    "s0_axi_s": "axi",
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

    //MII
    assign eth_MRxClk = eth_clk;
    assign MRxD = {enet_rx_d3_i, enet_rx_d2_i, enet_rx_d1_i, enet_rx_d0_i};
    assign MRxDv = enet_rx_dv_i;
    //assign MRxErr = enet_rx_err_o;
    assign MRxErr = 1'b0;

    assign eth_MTxClk = eth_clk;
    assign {enet_tx_d3_o, enet_tx_d2_o, enet_tx_d1_o, enet_tx_d0_o} = MTxD;
    assign enet_tx_en_o = MTxEn;
    //assign enet_tx_err_o = MTxErr;

    assign enet_resetn_o = phy_rstn;

    assign eth_MColl = 1'b0;
    assign eth_MCrS = 1'b0;
""",
            },
        ]

    return attributes_dict
