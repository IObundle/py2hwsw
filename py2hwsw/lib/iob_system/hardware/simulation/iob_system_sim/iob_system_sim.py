# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                "val": "4",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "D",
                "val": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "D",
                "val": params["mem_addr_w"],
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
                "val": "3000000",
            },
            {
                "name": "FREQ",
                "descr": "Clock frequency",
                "type": "D",
                "val": "100000000",
            },
            {
                "name": "SIMULATION",
                "descr": "Simulation flag",
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
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "iob_clk",
            },
        },
        {
            "name": "uart_s",
            "descr": "Testbench uart csrs interface",
            "signals": {
                "type": "iob",
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
                    "ADDR_W": 12,
                },
            },
        ]
    if params["cpu"] == "none":
        attributes_dict["ports"] += [
            {
                "name": "iob_s",
                "descr": "Direct control of system peripherals csrs",
                "signals": {
                    "type": "iob",
                    "prefix": "pbus_",
                    "ADDR_W": 3,
                },
            },
        ]

    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "clk",
            "descr": "Clock signal",
            "signals": [
                {"name": "clk_i"},
            ],
        },
        {
            "name": "rst",
            "descr": "Reset signal",
            "signals": [
                {"name": "arst_i"},
            ],
        },
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
                    "LOCK_W": 1,
                },
            },
            {
                "name": "axi_ram_mem",
                "descr": "Connect axi_ram to 'iob_ram_t2p_be' memory",
                "signals": {"type": "ram_t2p_be", "prefix": "ext_mem_"},
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
                "name": "phy",
                "descr": "PHY Interface Ports",
                "signals": [
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
            {
                "name": "eth_phy_invert",
                "descr": "Invert order of signals in ethernet MII bus",
                "signals": [
                    {"name": "eth_MTxClk"},
                    {"name": "MRxDv"},
                    {"name": "MRxD"},
                    {"name": "MRxErr"},
                    {"name": "eth_MRxClk"},
                    {"name": "MTxEn"},
                    {"name": "MTxD"},
                    {"name": "MTxErr"},
                    {"name": "eth_MColl"},
                    {"name": "eth_MCrS"},
                    {"name": "eth_MDC", "width": "1"},
                    {"name": "eth_MDIO", "width": "1"},
                    {"name": "eth_phy", "width": "1"},
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
    attributes_dict["subblocks"] = [
        {
            "core_name": py_params_dict["instantiator"]["original_name"],
            "instance_name": py_params_dict["instantiator"]["original_name"],
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
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["subblocks"][-1]["connect"].update({"phy_io": "phy"})
    if params["use_extmem"]:
        attributes_dict["subblocks"][-1]["connect"].update({"axi_m": "axi"})
    if params["cpu"] == "none":
        attributes_dict["subblocks"][-1]["connect"].update({"iob_s": "iob_s"})
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_uart",
            "instance_name": "uart_tb",
            "instance_description": "Testbench uart core",
            "csr_if": "iob",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_csrs_cbus_s": (
                    "uart_s",
                    [
                        "iob_addr_i[3-1:2]",
                    ],
                ),
                "rs232_m": "rs232_invert",
            },
        },
    ]
    if params["use_extmem"]:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_axi_ram",
                "instance_name": "ddr_model_mem",
                "instance_description": "External memory",
                "parameters": {
                    "ID_WIDTH": "AXI_ID_W",
                    "ADDR_WIDTH": "AXI_ADDR_W",
                    "DATA_WIDTH": "AXI_DATA_W",
                },
                "connect": {
                    "clk_i": "clk",
                    "rst_i": "rst",
                    "axi_s": (
                        "axi",
                        [
                            "{axi_araddr, 2'b0}",
                            "{axi_awaddr, 2'b0}",
                            "{1'b0, axi_arlock}",
                            "{1'b0, axi_awlock}",
                        ],
                    ),
                    "external_mem_bus_m": "axi_ram_mem",
                },
            },
            {
                "core_name": "iob_ram_t2p_be",
                "instance_name": "iob_ram_t2p_be_inst",
                "parameters": {
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "ram_t2p_be_s": "axi_ram_mem",
                },
            },
        ]
        if params["init_mem"] and not params["use_intmem"]:
            attributes_dict["subblocks"][-1]["parameters"].update(
                {
                    "HEXFILE": f'"{params["name"]}_firmware.hex"',
                }
            )
    if params["use_ethernet"]:
        attributes_dict["subblocks"] += [
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
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_csrs_cbus_s": (
                        "ethernet_s",
                        [
                            "ethernet_iob_addr_i[12-1:2]",
                        ],
                    ),
                    "axi_m": "eth_axi",
                    "inta_o": "eth_int",
                    "phy_io": "eth_phy_invert",
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
    assign eth_axi_awready = 1'b0;
    assign eth_axi_wready  = 1'b0;
    assign eth_axi_bid     = {AXI_ID_W{1'b0}};
    assign eth_axi_bresp   = 2'b0;
    assign eth_axi_bvalid  = 1'b0;
    assign eth_axi_arready = 1'b0;
    assign eth_axi_rid     = {AXI_ID_W{1'b0}};
    assign eth_axi_rdata   = {AXI_DATA_W{1'b0}};
    assign eth_axi_rresp   = 2'b0;
    assign eth_axi_rlast   = 1'b0;
    assign eth_axi_rvalid  = 1'b0;

    // Connect ethernet MII signals
    assign eth_MTxClk       = eth_clk;
    assign eth_MRxClk       = eth_clk;
    assign eth_MColl        = 1'b0;
    assign eth_MCrS         = 1'b0;

""",
            },
        ]

    return attributes_dict
