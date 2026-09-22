# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

import os


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_iob_zcu104",
        "generate_hw": True,
        #
        # Configuration
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                # The PS HP port has a 6 bit ID
                "val": "6" if params["use_extmem"] else "4",
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
                "descr": "AXI address bus width. The iob_system crossbar gives extmem a quarter of the 32 bit space, so 2**30 byte-addresses reach 1 GiB of the board's 2 GB PS DDR4.",
                "type": "D",
                "val": "30" if params["use_extmem"] else params["mem_addr_w"],
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
                "val": "100000000",
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
            "name": "clk_rst_i",
            "descr": "Clock and reset",
            "signals": [
                {"name": "c0_sys_clk_clk_p_i", "width": "1"},
                {"name": "c0_sys_clk_clk_n_i", "width": "1"},
                {"name": "areset_i", "width": "1"},
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
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "signals": [
                {"name": "rxd_i"},
                {"name": "txd_o"},
                {"name": "rs232_rts", "width": "1"},
                {"name": "low", "width": "1"},
            ],
        },
    ]
    attributes_dict["wires"] += [
        {
            "name": "clk_wizard_out",
            "descr": "Connect clock wizard outputs to iob-system clock and reset",
            "signals": [
                {"name": "clk"},
                (
                    {"name": "pll_arst", "width": "1"}
                    if params["use_extmem"]
                    else {"name": "arst"}
                ),
            ],
        },
    ]
    if params["use_extmem"]:
        attributes_dict["wires"] += [
            {"name": "rst_n", "signals": [{"name": "rst_n", "width": 1}]},
            {
                "name": "axi",
                "descr": "AXI interface to connect SoC to the PS memory port",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ]

    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core": py_params_dict["issuer"]["original_name"],
            "instance_name": py_params_dict["issuer"]["original_name"],
            "instance_description": "IOb-SoC instance",
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
        },
    ]
    if params["use_extmem"]:
        attributes_dict["subblocks"][-1]["connect"].update({"axi_m": "axi"})
    # Clock wizard
    attributes_dict["subblocks"] += [
        {
            "core": "iob_xilinx_clock_wizard",
            "instance_name": "clk_125_to_100_MHz",
            "instance_description": "PLL to generate system clock",
            "parameters": {
                "OUTPUT_PER": 10,
                "INPUT_PER": 8,
                "CLKFBOUT_MULT": 8,
            },
            "connect": {
                "clk_rst_i": "clk_rst_i",
                "clk_rst_o": "clk_wizard_out",
            },
        },
    ]

    #
    # Snippets
    #
    verilog_snippet = """
    // General connections
    assign low = 1'b0;
    assign cke = 1'b1;
"""
    if params["use_extmem"]:
        verilog_snippet += """
    assign arst = pll_arst | ~rst_n;

    localparam PS_ADDR_W = 49;

    system_wrapper ps_inst (
        .saxihp0_fpd_aclk(clk),
        .pl_resetn0(rst_n),

        .S_AXI_HP0_FPD_awaddr({{(PS_ADDR_W - AXI_ADDR_W) {1'b0}}, axi_awaddr}),
        .S_AXI_HP0_FPD_awid(axi_awid),
        .S_AXI_HP0_FPD_awlen(axi_awlen),
        .S_AXI_HP0_FPD_awsize(axi_awsize),
        .S_AXI_HP0_FPD_awburst(axi_awburst),
        .S_AXI_HP0_FPD_awlock(axi_awlock),
        .S_AXI_HP0_FPD_awcache(axi_awcache),
        .S_AXI_HP0_FPD_awprot(3'b000),
        .S_AXI_HP0_FPD_awqos(axi_awqos),
        .S_AXI_HP0_FPD_awuser(1'b0),
        .S_AXI_HP0_FPD_awvalid(axi_awvalid),
        .S_AXI_HP0_FPD_awready(axi_awready),

        .S_AXI_HP0_FPD_wdata(axi_wdata),
        .S_AXI_HP0_FPD_wstrb(axi_wstrb),
        .S_AXI_HP0_FPD_wlast(axi_wlast),
        .S_AXI_HP0_FPD_wvalid(axi_wvalid),
        .S_AXI_HP0_FPD_wready(axi_wready),

        .S_AXI_HP0_FPD_bid(axi_bid),
        .S_AXI_HP0_FPD_bresp(axi_bresp),
        .S_AXI_HP0_FPD_bvalid(axi_bvalid),
        .S_AXI_HP0_FPD_bready(axi_bready),

        .S_AXI_HP0_FPD_araddr({{(PS_ADDR_W - AXI_ADDR_W) {1'b0}}, axi_araddr}),
        .S_AXI_HP0_FPD_arid(axi_arid),
        .S_AXI_HP0_FPD_arlen(axi_arlen),
        .S_AXI_HP0_FPD_arsize(axi_arsize),
        .S_AXI_HP0_FPD_arburst(axi_arburst),
        .S_AXI_HP0_FPD_arlock(axi_arlock),
        .S_AXI_HP0_FPD_arcache(axi_arcache),
        .S_AXI_HP0_FPD_arprot(3'b000),
        .S_AXI_HP0_FPD_arqos(axi_arqos),
        .S_AXI_HP0_FPD_aruser(1'b0),
        .S_AXI_HP0_FPD_arvalid(axi_arvalid),
        .S_AXI_HP0_FPD_arready(axi_arready),

        .S_AXI_HP0_FPD_rid(axi_rid),
        .S_AXI_HP0_FPD_rdata(axi_rdata),
        .S_AXI_HP0_FPD_rresp(axi_rresp),
        .S_AXI_HP0_FPD_rlast(axi_rlast),
        .S_AXI_HP0_FPD_rvalid(axi_rvalid),
        .S_AXI_HP0_FPD_rready(axi_rready)
    );
"""
    attributes_dict["snippets"] = [{"verilog_code": verilog_snippet}]

    # Create system clock constraint
    assert py_params_dict["build_dir"], "build_dir not set!"
    fpga_folder = os.path.join(
        py_params_dict["build_dir"],
        "hardware/fpga/vivado/iob_zcu104",
    )
    os.makedirs(fpga_folder, exist_ok=True)
    with open(os.path.join(fpga_folder, "auto_board.sdc"), "w") as f:
        f.write(
            """\
# This file was automatically generated by the iob_system_iob_zcu104.py script.

## System Clock
create_clock -name "clk" -period 8.0 [get_ports {c0_sys_clk_clk_p_i}]
"""
        )

    return attributes_dict
