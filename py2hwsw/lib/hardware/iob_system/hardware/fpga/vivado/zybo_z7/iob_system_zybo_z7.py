# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# Copied from py2 'board.py'
bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "100000000"},
    {"name": "DDR_DATA_W", "type": "M", "val": "32"},
    {"name": "DDR_ADDR_W", "type": "M", "val": "30"},
    {"name": "XILINX", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_zybo_z7",
        "version": "0.1",
        #
        # Configuration
        #
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
                "val": "`DDR_ADDR_W" if params["use_extmem"] else "20",
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
                {"name": "arst_i", "width": "1"},
            ],
        },
        {
            "name": "rs232",
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
            "name": "ps_clk_arstn",
            "descr": "Clock and reset",
            "signals": [
                {"name": "ps_clk", "width": "1"},
                {"name": "ps_arstn", "width": "1"},
            ],
        },
        {
            "name": "ps_clk_rst",
            "descr": "Clock and reset",
            "signals": {
                "type": "clk_rst",
            },
        },
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "clk_en_rst",
            },
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "signals": {
                "type": "rs232",
            },
        },
        {
            "name": "intercon_m_clk_rst",
            "descr": "AXI interconnect clock and reset inputs",
            "signals": {
                "type": "clk_rst",
                "prefix": "intercon_m_",
            },
        },
        {
            "name": "ps_axi",
            "descr": "AXI bus to connect interconnect and memory",
            "signals": {
                "type": "axi",
                "prefix": "mem_",
                "ID_W": "AXI_ID_W",
                "LEN_W": "AXI_LEN_W",
                "ADDR_W": "AXI_ADDR_W - 2",
                "DATA_W": "AXI_DATA_W",
                "LOCK_W": 1,
            },
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
        ]

    #
    # Blocks
    #
    attributes_dict["blocks"] = [
        {
            # IOb-SoC Memory Wrapper
            "core_name": "iob_system_mwrap",
            "instance_name": "iob_system_mwrap",
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
            "iob_system_params": params,
        },
    ]
    if params["use_extmem"]:
        attributes_dict["blocks"][-1]["connect"].update({"axi_m": "axi"})
        attributes_dict["blocks"] += [
            {
                "core_name": "iob_xilinx_axi_interconnect",
                "instance_name": "axi_async_bridge",
                "instance_description": "Interconnect instance",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W - 2",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_rst_s": "ps_clk_rst",
                    "m0_clk_rst": "intercon_m_clk_rst",
                    "m0_axi_m": "ps_axi",
                    "s0_clk_rst": "ps_clk_rst",
                    "s0_axi_s": "axi",
                },
                "num_slaves": 1,
            },
        ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
            // General connections
            assign cke = 1'b1;
            assign arst = ~ps_arstn;
            assign ps_arst = ~ps_arstn;
            """,
        },
    ]

    return attributes_dict
