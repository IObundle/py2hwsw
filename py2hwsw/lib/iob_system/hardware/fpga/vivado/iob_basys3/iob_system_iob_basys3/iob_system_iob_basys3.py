# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_iob_basys3",
        "generate_hw": True,
        #
        # Configuration
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                "val": "4",
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
                "descr": "AXI address bus width",
                "type": "D",
                "val": "NA" if params["use_extmem"] else "20",
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
                {"name": "clk_i", "width": "1"},
                {"name": "arst_i", "width": "1"},
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
            "name": "axi",
            "descr": "AXI interface to connect SoC to memory",
            "signals": {
                "type": "axi",
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        {
            "name": "memory_axi",
            "descr": "AXI bus to connect interconnect and memory",
            "signals": {
                "type": "axi",
                "prefix": "mem_",
                "ID_W": "AXI_ID_W",
                "LEN_W": "AXI_LEN_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LOCK_W": 1 if params["use_extmem"] else 2,
            },
        },
    ]

    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            # IOb-SoC Memory Wrapper
            "core_name": py_params_dict["issuer"]["original_name"],
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
                "axi_m": "axi",
            },
            "dest_dir": "hardware/common_src",
        },
        {
            "core_name": "iob_xilinx_axi_interconnect",
            "instance_name": "axi_async_bridge",
            "instance_description": "Interconnect instance",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_rst_s": "intercon_clk_rst",
                "m0_clk_rst_io": "intercon_m0_clk_rst",
                "m0_axi_m": "memory_axi",
                "s0_clk_rst_io": "intercon_s0_clk_rst",
                "s0_axi_s": "axi",
            },
            "num_subordinates": 1,
        },
        {
            "core_name": "iob_axi_ram",
            "instance_name": "ddr_model_mem",
            "instance_description": "DDR model memory",
            "parameters": {
                "ID_WIDTH": "AXI_ID_W",
                "ADDR_WIDTH": "AXI_ADDR_W",
                "DATA_WIDTH": "AXI_DATA_W",
            },
            "connect": {
                "clk_i": "clk",
                "rst_i": "arst",
                "axi_s": "memory_axi",
            },
        },
    ]

    if params["init_mem"]:
        attributes_dict["subblocks"][-1]["parameters"].update(
            {
                "FILE": f'"{params["name"]}_firmware"',
            }
        )

    return attributes_dict
