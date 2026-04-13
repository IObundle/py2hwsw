# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_iob_smart_zynq_sl",
        "generate_hw": True,
        #
        # Configuration
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                "val": "6",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "D",
                "val": "8",
                "min": "1",
                "max": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width. 2**29 byte-addresses for 512 MiB of DDR3 memory.",
                "type": "D",
                "val": "29",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "D",
                "val": "32",
                "min": "1",
                "max": "32",
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
                "name": "XILINX",
                "descr": "xilinx flag",
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
            "name": "ddr_io",
            "descr": "Zynq DDR pins",
            "signals": [
                {"name": "ddr_addr_io", "width": "15"},
                {"name": "ddr_ba_io", "width": "3"},
                {"name": "ddr_cas_n_io", "width": "1"},
                {"name": "ddr_ck_n_io", "width": "1"},
                {"name": "ddr_ck_p_io", "width": "1"},
                {"name": "ddr_cke_io", "width": "1"},
                {"name": "ddr_cs_n_io", "width": "1"},
                {"name": "ddr_dm_io", "width": "4"},
                {"name": "ddr_dq_io", "width": "32"},
                {"name": "ddr_dqs_n_io", "width": "4"},
                {"name": "ddr_dqs_p_io", "width": "4"},
                {"name": "ddr_odt_io", "width": "1"},
                {"name": "ddr_ras_n_io", "width": "1"},
                {"name": "ddr_reset_n_io", "width": "1"},
                {"name": "ddr_we_n_io", "width": "1"},
            ],
        },
        {
            "name": "fixed_io",
            "descr": "Zynq Fixed IO pins",
            "signals": [
                {"name": "fixed_io_ddr_vrn_io", "width": "1"},
                {"name": "fixed_io_ddr_vrp_io", "width": "1"},
                {"name": "fixed_io_mio_io", "width": "54"},
                {"name": "fixed_io_ps_clk_io", "width": "1"},
                {"name": "fixed_io_ps_porb_io", "width": "1"},
                {"name": "fixed_io_ps_srstb_io", "width": "1"},
            ],
        },
        {
            "name": "board_peripherals_io",
            "descr": "Board Peripherals",
            "signals": [
                {"name": "led_o", "width": "2"},
                {"name": "key_i", "width": "2"},
                {"name": "uart_rxd_i", "width": "1"},
                {"name": "uart_txd_o", "width": "1"},
            ],
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["ports"] += [
            {
                "name": "mii_io",
                "descr": "Ethernet interface",
                "signals": [
                    {"name": "mii_rx_clk_i", "width": "1"},
                    {"name": "mii_rxd_i", "width": "4"},
                    {"name": "mii_rx_dv_i", "width": "1"},
                    {"name": "mii_rx_er_i", "width": "1"},
                    {"name": "mii_tx_clk_o", "width": "1"},
                    {"name": "mii_txd_o", "width": "4"},
                    {"name": "mii_tx_en_o", "width": "1"},
                    {"name": "mii_mdc_o", "width": "1"},
                    {"name": "mii_mdio_io", "width": "1"},
                    {"name": "mii_crs_i", "width": "1"},
                    {"name": "mii_col_i", "width": "1"},
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
            "signals": {
                "type": "iob_clk",
            },
        },
        {"name": "rst_n", "signals": [{"name": "rst_n", "width": 1}]},
        {
            "name": "ps_uart",
            "descr": "PS UART signals",
            "signals": [
                {"name": "ps_uart_rx", "width": "1"},
                {"name": "ps_uart_tx", "width": "1"},
            ],
        },
        {
            "name": "ps_gpio",
            "descr": "PS GPIO signals",
            "signals": [
                {"name": "ps_gpio_o", "width": "64"},
                {"name": "ps_gpio_i", "width": "64"},
            ],
        },
        {
            "name": "axi",
            "descr": "AXI interface to connect SoC to PS DDR",
            "signals": {
                "type": "axi",
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
                "PROT_W": 3,
                "LOCK_W": 1,
            },
        },
        {
            "name": "uut_rs232",
            "descr": "Uart interface for UUT",
            "signals": {
                "type": "rs232",
                "prefix": "uut_",
            },
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["wires"] += [
            {
                "name": "rxclk_buf_io",
                "descr": "IBUFG io",
                "signals": [
                    {"name": "mii_rx_clk_i"},
                    {"name": "eth_clk", "width": "1"},
                ],
            },
            {
                "name": "oddr_io",
                "descr": "ODDR io",
                "signals": [
                    {"name": "eth_clk"},
                    {"name": "high", "width": "1"},
                    {"name": "low", "width": "1"},
                    {"name": "mii_tx_clk_o"},
                ],
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
                "name": "mii",
                "descr": "Ethernet MII interface for UUT",
                "signals": {
                    "type": "mii",
                    "prefix": "uut_",
                },
            },
        ]

    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            # IOb-SoC instance
            "core_name": py_params_dict["issuer"]["original_name"],
            "instance_name": py_params_dict["issuer"]["original_name"],
            "instance_description": "IOb-System instance",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "8",  # SoC expects AXI4
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst",
                "rs232_m": "uut_rs232",
            },
            "dest_dir": "hardware/common_src",
        },
    ]
    if params["use_extmem"]:
        attributes_dict["subblocks"][-1]["connect"].update({"axi_m": "axi"})
    if params["use_ethernet"]:
        attributes_dict["subblocks"][-1]["connect"].update({"mii_io": "mii"})
        attributes_dict["subblocks"][-1]["connect"].update({"phy_rstn_o": "phy_rstn"})
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_xilinx_ibufg",
                "instance_name": "rxclk_buf",
                "connect": {
                    "io_io": "rxclk_buf_io",
                },
            },
            {
                "core_name": "iob_xilinx_oddr",
                "instance_name": "txclk_oddr",
                "connect": {
                    "io_io": "oddr_io",
                },
            },
        ]

    #
    # Snippets
    #
    verilog_snippet = """
    // Connect board's LEDs and KEYs to PS7 GPIO.
    assign led_o = ps_gpio_o[1:0];
    assign ps_gpio_i = {62'b0, key_i};
    
    // Connect clk_en_rst sources
    assign cke = 1'b1;
    assign arst = ~rst_n;

    // Connect iob_system uart flow control
    assign uut_rs232_cts = 1'b1;
    // uut_rs232_rts floating

    // For now, UART pins can be connected to either iob_system or PS7. Select one below.
    // Connect iob_system uart
    assign uut_rs232_rxd = uart_rxd_i;
    assign uart_txd_o = uut_rs232_txd;
    // Connect PS7 uart
    // assign ps_uart_rx = uart_rxd_i;
    // assign uart_txd_o = ps_uart_tx;

    // Instantiate Zynq Block Design Wrapper
    system_wrapper ps_inst (
        .DDR_addr(ddr_addr_io),
        .DDR_ba(ddr_ba_io),
        .DDR_cas_n(ddr_cas_n_io),
        .DDR_ck_n(ddr_ck_n_io),
        .DDR_ck_p(ddr_ck_p_io),
        .DDR_cke(ddr_cke_io),
        .DDR_cs_n(ddr_cs_n_io),
        .DDR_dm(ddr_dm_io),
        .DDR_dq(ddr_dq_io),
        .DDR_dqs_n(ddr_dqs_n_io),
        .DDR_dqs_p(ddr_dqs_p_io),
        .DDR_odt(ddr_odt_io),
        .DDR_ras_n(ddr_ras_n_io),
        .DDR_reset_n(ddr_reset_n_io),
        .DDR_we_n(ddr_we_n_io),
        .FIXED_IO_ddr_vrn(fixed_io_ddr_vrn_io),
        .FIXED_IO_ddr_vrp(fixed_io_ddr_vrp_io),
        .FIXED_IO_mio(fixed_io_mio_io),
        .FIXED_IO_ps_clk(fixed_io_ps_clk_io),
        .FIXED_IO_ps_porb(fixed_io_ps_porb_io),
        .FIXED_IO_ps_srstb(fixed_io_ps_srstb_io),
        
        .FCLK_CLK0(clk),
        .FCLK_RESET0_N(rst_n),
        
        .S_AXI_HP0_awaddr({3'b0, axi_awaddr}),
        .S_AXI_HP0_awid(axi_awid),
        .S_AXI_HP0_awlen(axi_awlen[3:0]),
        .S_AXI_HP0_awsize(axi_awsize),
        .S_AXI_HP0_awburst(axi_awburst),
        .S_AXI_HP0_awlock({1'b0, axi_awlock}),
        .S_AXI_HP0_awcache(axi_awcache),
        .S_AXI_HP0_awprot(axi_awprot),
        .S_AXI_HP0_awqos(axi_awqos),
        .S_AXI_HP0_awvalid(axi_awvalid),
        .S_AXI_HP0_awready(axi_awready),
        .S_AXI_HP0_wdata(axi_wdata),
        .S_AXI_HP0_wstrb(axi_wstrb),
        .S_AXI_HP0_wlast(axi_wlast),
        .S_AXI_HP0_wid(axi_awid), // Zynq HP ports use awid for wid
        .S_AXI_HP0_wvalid(axi_wvalid),
        .S_AXI_HP0_wready(axi_wready),
        .S_AXI_HP0_bid(axi_bid),
        .S_AXI_HP0_bresp(axi_bresp),
        .S_AXI_HP0_bvalid(axi_bvalid),
        .S_AXI_HP0_bready(axi_bready),
        .S_AXI_HP0_araddr({3'b0, axi_araddr}),
        .S_AXI_HP0_arid(axi_arid),
        .S_AXI_HP0_arlen(axi_arlen[3:0]),
        .S_AXI_HP0_arsize(axi_arsize),
        .S_AXI_HP0_arburst(axi_arburst),
        .S_AXI_HP0_arlock({1'b0, axi_arlock}),
        .S_AXI_HP0_arcache(axi_arcache),
        .S_AXI_HP0_arprot(axi_arprot),
        .S_AXI_HP0_arqos(axi_arqos),
        .S_AXI_HP0_arvalid(axi_arvalid),
        .S_AXI_HP0_arready(axi_arready),
        .S_AXI_HP0_rid(axi_rid),
        .S_AXI_HP0_rdata(axi_rdata),
        .S_AXI_HP0_rresp(axi_rresp),
        .S_AXI_HP0_rlast(axi_rlast),
        .S_AXI_HP0_rvalid(axi_rvalid),
        .S_AXI_HP0_rready(axi_rready),
        
        .GPIO_O(ps_gpio_o),
        .GPIO_I(ps_gpio_i),
        .UART0_RX(ps_uart_rx),
        .UART0_TX(ps_uart_tx)
    );
"""
    if not params["use_extmem"]:
        verilog_snippet += """
    // Connect unused AXI inputs to zero
    assign axi_awid = 'b0;
    assign axi_awaddr = 'b0;
    assign axi_awprot = 'b0;
    assign axi_awlen = 'b0;
    assign axi_awsize = 'd2; // 4 byte data transfer
    assign axi_awburst = 'b0;
    assign axi_awlock = 'b0;
    assign axi_awcache = 'b0;
    assign axi_awqos = 'b0;
    assign axi_awvalid = 'b0;
    assign axi_wstrb = 'b0;
    assign axi_wdata = 'b0;
    assign axi_wlast = 'd1; // All bursts are single transfers: always the last burst
    assign axi_wvalid = 'b0;
    assign axi_bready = 'b0;
    assign axi_arid = 'b0;
    assign axi_araddr = 'b0;
    assign axi_arprot = 'b0;
    assign axi_arlen = 'b0;
    assign axi_arsize = 'd2; // 4 byte data transfer
    assign axi_arburst = 'b0;
    assign axi_arlock = 'b0;
    assign axi_arcache = 'b0;
    assign axi_arqos = 'b0;
    assign axi_arvalid = 'b0;
    assign axi_rready = 'b0;
"""
    if params["use_ethernet"]:
        verilog_snippet += """
    // Ethernet connections
    assign high = 1'b1;
    assign low = 1'b0;

    // Use mii_rx_clk_i buffered clock (eth_clk) for internal MII and external mii_tx_clk_i
    assign uut_mii_rx_clk = eth_clk;
    assign uut_mii_tx_clk = eth_clk;

    // Connect internal MII data/control to external ports
    assign uut_mii_rxd = mii_rxd_i;
    assign uut_mii_rx_dv = mii_rx_dv_i;
    assign uut_mii_rx_er = mii_rx_er_i;

    assign mii_txd_o = uut_mii_txd;
    assign mii_tx_en_o = uut_mii_tx_en;

    assign mii_mdc_o = uut_mii_mdc;
    assign mii_mdio_io = uut_mii_mdio;

    assign uut_mii_crs = mii_crs_i;
    assign uut_mii_col = mii_col_i;

    assign phy_rstn = ~arst; // PHY reset
"""

    attributes_dict["snippets"] = [{"verilog_code": verilog_snippet}]

    # Create system clock constraint
    assert py_params_dict["build_dir"], "build_dir not set!"
    fpga_folder = os.path.join(
        py_params_dict["build_dir"],
        "hardware/fpga/vivado/iob_smart_zynq_sl",
    )
    os.makedirs(fpga_folder, exist_ok=True)
    with open(os.path.join(fpga_folder, "auto_board.sdc"), "w") as f:
        f.write(
            """\
# This file was automatically generated by the iob_system_iob_smart_zynq_sl.py script.

# Clock groups
set_clock_groups -asynchronous -group {clk_fpga_0} -group {mii_rx_clk_i}
"""
        )

    return attributes_dict
