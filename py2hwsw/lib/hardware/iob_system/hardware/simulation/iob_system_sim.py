# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

bsp = [
    {"name": "BAUD", "type": "M", "val": "3000000"},
    {"name": "FREQ", "type": "M", "val": "100000000"},
    {"name": "DDR_DATA_W", "type": "M", "val": "32"},
    {"name": "DDR_ADDR_W", "type": "M", "val": "24"},
    {"name": "SIMULATION", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "version": "0.1",
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "F",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "F",
                "val": "8",
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
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "clk_en_rst",
            },
        },
        {
            "name": "uart_s",
            "descr": "Testbench uart csrs interface",
            "signals": {
                "type": "iob",
                "prefix": "uart_",
                "ADDR_W": 3,
            },
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["ports"] += [
            {
                "name": "ethernet_s",
                "descr": "Testbench ethernet csrs interface",
                "signals": {
                    "type": "iob",
                    "prefix": "ethernet_",
                },
            },
        ]

    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "rs232",
            "descr": "rs232 bus",
            "signals": {
                "type": "rs232",
            },
        },
        {
            "name": "rs232_invert",
            "descr": "Invert order of rs232 signals",
            "signals": [
                {"name": "rs232_txd"},
                {"name": "rs232_rxd"},
                {"name": "rs232_cts"},
                {"name": "rs232_rts"},
            ],
        },
    ]
    if params["use_extmem"]:
        attributes_dict["wires"] += [
            {
                "name": "axi",
                "descr": "AXI bus to connect SoC to interconnect",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "AXI_LEN_W",
                },
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["wires"] += [
            {
                "name": "eth_axi",
                "descr": "Ethernet AXI bus",
                "signals": {
                    "type": "axi",
                    "prefix": "eth_",
                },
            },
            {
                "name": "eth_mii_invert",
                "descr": "Invert order of signals in ethernet MII bus",
                "signals": [
                    {"name": "eth_MTxClk", "width": "1"},
                    {"name": "MRxDv"},
                    {"name": "MRxD"},
                    {"name": "MRxErr"},
                    {"name": "eth_MRxClk", "width": "1"},
                    {"name": "MTxEn"},
                    {"name": "MTxD"},
                    {"name": "MTxErr"},
                    {"name": "eth_MColl", "width": "1"},
                    {"name": "eth_MCrS", "width": "1"},
                    {"name": "eth_MDC", "width": "1"},
                    {"name": "eth_MDIO", "width": "1"},
                ],
            },
            {
                "name": "eth_int",
                "descr": "Ethernet interrupt",
                "signals": [
                    {"name": "eth_interrupt"},
                ],
            },
        ]
    #
    # Blocks
    #
    attributes_dict["blocks"] = [
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
                "clk_en_rst_s": "clk_en_rst_s",
                "rs232_m": "rs232",
            },
            "dest_dir": "hardware/common_src",
            "iob_system_params": params,
        },
    ]
    if params["use_extmem"]:
        attributes_dict["blocks"][-1]["connect"].update({"axi_m": "axi"})
    attributes_dict["blocks"] += [
        {
            "core_name": "iob_uart",
            "name": "iob_uart_iob",
            "instance_name": "uart_tb",
            "instance_description": "Testbench uart core",
            "csr_if": "iob",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "cbus_s": (
                    "uart_s",
                    [
                        "uart_iob_addr_i[3-1:2]",
                    ],
                ),
                "rs232_m": "rs232_invert",
            },
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["blocks"] += [
            {
                "core_name": "iob_eth",
                "instance_name": "eth_tb",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_en_rst": "clk_en_rst_s",
                    "iob": "ethernet",
                    "axi": "eth_axi",
                    "mii": "eth_mii_invert",
                    "interrupt": "eth_int",
                },
            },
        ]
    #
    # Snippets
    #
    attributes_dict["snippets"] = []
    if params["use_ethernet"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
    //ethernet clock: 4x slower than system clock
    reg [1:0] eth_cnt = 2'b0;
    reg       eth_clk;

    always @(posedge clk_i) begin
      eth_cnt <= eth_cnt + 1'b1;
      eth_clk <= eth_cnt[1];
    end

    // Set ethernet AXI inputs to low
    assign eth_axi_awready_i = 1'b0;
    assign eth_axi_wready_i  = 1'b0;
    assign eth_axi_bid_i     = {AXI_ID_W{1'b0}};
    assign eth_axi_bresp_i   = 2'b0;
    assign eth_axi_bvalid_i  = 1'b0;
    assign eth_axi_arready_i = 1'b0;
    assign eth_axi_rid_i     = {AXI_ID_W{1'b0}};
    assign eth_axi_rdata_i   = {AXI_DATA_W{1'b0}};
    assign eth_axi_rresp_i   = 2'b0;
    assign eth_axi_rlast_i   = 1'b0;
    assign eth_axi_rvalid_i  = 1'b0;

    // Connect ethernet MII signals
    assign eth_MTxClk       = eth_clk;
    assign eth_MRxClk       = eth_clk;
    assign eth_MColl        = 1'b0;
    assign eth_MCrS         = 1'b0;

""",
            },
        ]

    return attributes_dict
