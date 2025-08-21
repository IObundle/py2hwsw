# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = py_params_dict["iob_system_params"]

    # Size of RAM for ethernet's dma
    ETH_RAM_ADDR_W = 14

    tb_peripherals = ["iob_uart"]
    if params["use_ethernet"]:
        tb_peripherals += ["iob_eth", "eth_ram"]

    periph_sel_bits = (len(tb_peripherals) - 1).bit_length()
    periph_addr_w = 32 - periph_sel_bits

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
            "name": "tb_s",
            "descr": "Testbench iob interface",
            "signals": {
                "type": "iob",
                "ADDR_W": 32,
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
        {
            "name": "uart_cbus",
            "descr": "UART CSR bus",
            "signals": {
                "type": "iob",
                "prefix": "uart_",
                "ADDR_W": periph_addr_w,
            },
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
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "axi_ram_mem",
                "descr": "Connect axi_ram to 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": "AXI_ADDR_W - 2",
                },
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["wires"] += [
            {
                "name": "eth_cbus",
                "descr": "Ethernet CSR bus",
                "signals": {
                    "type": "iob",
                    "prefix": "eth_",
                    "ADDR_W": periph_addr_w,
                },
            },
            {
                "name": "eth_ram_iob",
                "descr": "IOB bus to access Ethernet's RAM",
                "signals": {
                    "type": "iob",
                    "ADDR_W": ETH_RAM_ADDR_W,
                },
            },
            {
                "name": "eth_ram_axi",
                "descr": "AXI bus to access Ethernet's RAM",
                "signals": {
                    "type": "axi",
                    "prefix": "eth_ram_",
                    "ADDR_W": ETH_RAM_ADDR_W,
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "eth_axi",
                "descr": "Ethernet AXI bus",
                "signals": {
                    "type": "axi",
                    "prefix": "eth_",
                    "ADDR_W": ETH_RAM_ADDR_W,
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "phy_rstn",
                "descr": "",
                "signals": [
                    {
                        "name": "phy_rstn",
                        "width": "1",
                        "descr": "Issuer ethernet reset signal for PHY.",
                    },
                ],
            },
            {
                "name": "tb_phy_rstn",
                "descr": "",
                "signals": [
                    {
                        "name": "tb_phy_rstn",
                        "width": "1",
                        "descr": "Testbench ethernet reset signal for PHY.",
                    },
                ],
            },
            {
                "name": "mii",
                "descr": "Ethernet MII interface",
                "signals": {
                    "type": "mii",
                },
            },
            {
                "name": "mii_invert",
                "descr": "Invert RX and TX signals of ethernet MII bus",
                "signals": [
                    {"name": "mii_tx_clk"},
                    {"name": "mii_rxd"},
                    {"name": "mii_rx_dv"},
                    {"name": "mii_rx_er"},
                    {"name": "mii_rx_clk"},
                    {"name": "mii_txd"},
                    {"name": "mii_tx_en"},
                    {"name": "mii_tx_er"},
                    {"name": "mii_crs"},
                    {"name": "mii_col"},
                    # Create new management signals for testbench eth
                    {"name": "tb_mii_mdio", "width": "1"},
                    {"name": "tb_mii_mdc", "width": "1"},
                ],
            },
            {
                "name": "eth_int",
                "descr": "Ethernet interrupt",
                "signals": [
                    {"name": "eth_interrupt"},
                ],
            },
            # Wires for AXI ram
            {
                "name": "merge_s_axi",
                "descr": "AXI subordinate bus for merge",
                "signals": {
                    "type": "axi",
                    "prefix": "intercon_s_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": 2,
                },
            },
            {
                "name": "merge_m_axi",
                "descr": "AXI manager bus for merge",
                "signals": {
                    "type": "axi",
                    "prefix": "intercon_m_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": 2,
                },
            },
            {
                "name": "eth_ram_mem",
                "descr": "Connect axi_ram to 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "prefix": "ext_mem_",
                },
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
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rs232_m": "rs232",
            },
            "dest_dir": "hardware/common_src",
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["subblocks"][-1]["connect"].update({"mii_io": "mii"})
        attributes_dict["subblocks"][-1]["connect"].update({"phy_rstn_o": "phy_rstn"})
    if params["use_extmem"]:
        attributes_dict["subblocks"][-1]["connect"].update({"axi_m": "axi"})
    if params["cpu"] == "none":
        attributes_dict["subblocks"][-1]["connect"].update({"iob_s": "iob_s"})
    # Only add tb pbus split if there are more than one peripheral
    if len(tb_peripherals) > 1:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_split",
                "name": "tb_pbus_split",
                "instance_name": "iob_pbus_split",
                "instance_description": "Split between testbench peripherals",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "split_reset",
                    "input_s": "tb_s",
                    "output_0_m": "uart_cbus",
                },
                "num_outputs": 1,
                "addr_w": 32,
            },
        ]
    # Connect ethernet and its RAM to pbus
    if params["use_ethernet"]:
        subordinate_num = attributes_dict["subblocks"][-1]["num_outputs"]
        attributes_dict["subblocks"][-1]["num_outputs"] += 2
        attributes_dict["subblocks"][-1]["connect"] |= {
            f"output_{subordinate_num}_m": "eth_cbus",
            f"output_{subordinate_num+1}_m": "eth_ram_iob",
        }
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_uart",
            "instance_name": "uart_tb",
            "instance_description": "Testbench uart core",
            "csr_if": "iob",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_csrs_cbus_s": ("uart_cbus", ["uart_iob_addr[2:0]"]),
                "rs232_m": "rs232_invert",
            },
        },
    ]
    if len(tb_peripherals) == 1:
        # Connect uart directly to tb_s port if there is no tb_pbus_split
        attributes_dict["subblocks"][-1]["connect"].update(
            {"iob_csrs_cbus_s": ("tb_s", ["iob_addr_i[2:0]"])}
        )
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
                    "HEXFILE": f'"{params["name"]}_firmware"',
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
                    "AXI_ADDR_W": ETH_RAM_ADDR_W,
                    "AXI_DATA_W": 32,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_csrs_cbus_s": ("eth_cbus", ["eth_iob_addr[11:0]"]),
                    "axi_m": "eth_axi",
                    "inta_o": "eth_int",
                    "phy_rstn_o": "phy_rstn",
                    "mii_io": "mii_invert",
                },
            },
            # Create AXI merge and RAM for ethernet
            {
                "core_name": "iob_iob2axi",
                "instance_name": "eth_iob2axi",
                "parameters": {
                    "ADDR_W": ETH_RAM_ADDR_W,
                    "DATA_W": 32,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_s": "eth_ram_iob",
                    "axi_m": "eth_ram_axi",
                },
            },
            {
                "core_name": "iob_axi_merge",
                "name": f"{params['name']}_eth_merge",
                "instance_name": f"eth_axi_merge",
                "instance_description": f"AXI merge for ETH RAM",
                "parameters": {
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "num_subordinates": 2,
                "addr_w": ETH_RAM_ADDR_W,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "rst_i",
                    "s_0_s": "eth_ram_axi",
                    "s_1_s": "eth_axi",
                    "m_m": f"eth_axi_ram",
                },
            },
            {
                "core_name": "iob_axi_ram",
                "instance_name": "eth_axi_ram_inst",
                "instance_description": "AXI RAM for ethernet",
                "parameters": {
                    "ID_WIDTH": "AXI_ID_W",
                    "ADDR_WIDTH": ETH_RAM_ADDR_W,
                    "DATA_WIDTH": 32,
                },
                "connect": {
                    "clk_i": "clk",
                    "rst_i": "rst",
                    "axi_s": "eth_axi_ram",
                    "external_mem_bus_m": "eth_ram_mem",
                },
            },
            {
                "core_name": "iob_ram_t2p_be",
                "instance_name": "eth_ram_t2p_be_inst",
                "instance_description": "ETH AXI RAM external memory",
                "parameters": {
                    "ADDR_W": ETH_RAM_ADDR_W - 2,
                    "DATA_W": 32,
                },
                "connect": {
                    "ram_t2p_be_s": "eth_ram_mem",
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
    assign mii_tx_clk       = eth_clk;
    assign mii_rx_clk       = eth_clk;
    assign mii_col          = 1'b0;
    assign mii_crs          = 1'b0;

""",
            },
        ]

    # Calculate and print testbench peripheral memory map
    print("------------------------------------------------------")
    print("Testbench memory map:")
    current_addr = 0
    for peripheral in tb_peripherals:
        print(
            f"[0x{current_addr:08x}-0x{(current_addr+(1<<periph_addr_w)-1):08x}]: {peripheral} ({periph_addr_w} bits)"
        )
        current_addr += 1 << periph_addr_w
    print("------------------------------------------------------")

    return attributes_dict
