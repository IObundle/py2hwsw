# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os

# Add iob-system scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from iob_system_utils import update_params, iob_system_scripts


def setup(py_params_dict):
    params = {
        "name": "iob_system",
        "init_mem": True,
        "use_extmem": False,
        "use_ethernet": False,
        "addr_w": 32,
        "data_w": 32,
        "mem_addr_w": 24,
        "bootrom_addr_w": 12,
        "fw_addr": 0,
        "fw_addr_w": 15,
    }

    update_params(params, py_params_dict)

    attributes_dict = {
        "name": params["name"],
        "version": "0.7",
        "is_system": True,
        "board_list": ["aes_ku040_db_g"],
        "confs": [
            # macros
            {  # Needed for testbench
                "name": "ADDR_W",
                "descr": "Address bus width",
                "type": "M",
                "val": params["addr_w"],
                "min": "1",
                "max": "32",
            },
            {  # Needed for testbench
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "M",
                "val": params["data_w"],
                "min": "1",
                "max": "32",
            },
            {  # Needed for makefile and software
                "name": "INIT_MEM",
                "descr": "Enable MUL and DIV CPU instructions",
                "type": "M",
                "val": params["init_mem"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for makefile and software
                "name": "USE_EXTMEM",
                "descr": "Enable MUL and DIV CPU instructions",
                "type": "M",
                "val": params["use_extmem"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for testbench
                "name": "USE_ETHERNET",
                "descr": "Enable ethernet connections",
                "type": "M",
                "val": params["use_ethernet"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for software
                "name": "MEM_ADDR_W",
                "descr": "Memory bus address width",
                "type": "M",
                "val": params["mem_addr_w"],
                "min": "0",
                "max": "32",
            },
            {  # Needed for software
                "name": "FW_ADDR",
                "descr": "Firmware address",
                "type": "M",
                "val": params["fw_addr"],
                "min": "0",
                "max": "32",
            },
            {  # Needed for software
                "name": "FW_ADDR_W",
                "descr": "Firmware address",
                "type": "M",
                "val": params["fw_addr_w"],
                "min": "0",
                "max": "32",
            },
            {  # Needed for testbench
                "name": "RST_POL",
                "descr": "Reset polarity.",
                "type": "M",
                "val": "1",
                "min": "0",
                "max": "1",
            },
            {  # Needed for software and makefiles
                "name": "BOOTROM_ADDR_W",
                "descr": "Bootloader ROM address width (byte addressable). Includes a pre-bootloader that uses the first 128 bytes. Bootloader starts at address 0x80 of this ROM.",
                "type": "M",
                "val": params["bootrom_addr_w"],
                "min": "1",
                "max": "32",
            },
            # mandatory parameters (do not change them!)
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "F",
                "val": "0",
                "min": "0",
                "max": "32",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "F",
                "val": params["mem_addr_w"],
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "F",
                "val": params["data_w"],
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "F",
                "val": "4",
                "min": "1",
                "max": "4",
            },
        ],
    }
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "clk_en_rst",
            },
        },
        {
            "name": "rom_bus_io",
            "descr": "Ports for connection with ROM memory",
            "signals": [
                {
                    "name": "boot_rom_valid_o",
                    "width": "1",
                },
                {
                    "name": "boot_rom_addr_o",
                    "width": params["bootrom_addr_w"] - 2,
                },
                {
                    "name": "boot_rom_rdata_i",
                    "width": params["data_w"],
                },
            ],
        },
        {
            "name": "int_mem_axi_m",
            "descr": "AXI master interface for internal memory",
            "signals": {
                "type": "axi",
                "prefix": "int_mem_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": f"{params['fw_addr_w']}-2",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
                "LOCK_W": 1,
            },
        },
    ]
    if params["use_extmem"]:
        attributes_dict["ports"] += [
            {
                "name": "axi_m",
                "descr": "AXI master interface for DDR memory",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W-2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "AXI_LEN_W",
                },
            },
        ]
    attributes_dict["ports"] += [
        # Peripheral IO ports
        {
            "name": "rs232_m",
            "descr": "iob-system uart interface",
            "signals": {
                "type": "rs232",
            },
        },
        # NOTE: Add ports for peripherals here
    ]

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
            "name": "split_reset",
            "descr": "Reset signal for iob_split components",
            "signals": [
                {"name": "arst_i"},
            ],
        },
        {
            "name": "cpu_ibus",
            "descr": "CPU instruction bus",
            "signals": {
                "type": "axi",
                "prefix": "cpu_i_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": params["addr_w"] - 2,
                "DATA_W": params["data_w"],
                "LEN_W": "AXI_LEN_W",
                "LOCK_W": "1",
            },
        },
        {
            "name": "cpu_dbus",
            "descr": "CPU data bus",
            "signals": {
                "type": "axi",
                "prefix": "cpu_d_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": params["addr_w"] - 2,
                "DATA_W": params["data_w"],
                "LEN_W": "AXI_LEN_W",
                "LOCK_W": "1",
            },
        },
        {
            "name": "interrupts",
            "descr": "System interrupts",
            "signals": [
                {"name": "interrupts", "width": 32},
            ],
        },
        {
            "name": "unused_interconnect_bits",
            "descr": "Wires to connect to unused output bits of interconnect",
            "signals": [
                {"name": "unused_m0_araddr_bits", "width": (params["addr_w"] - 2) - 13},
                {"name": "unused_m0_awaddr_bits", "width": (params["addr_w"] - 2) - 13},
                {"name": "unused_m1_araddr_bits", "width": (params["addr_w"] - 2) - 22},
                {"name": "unused_m1_awaddr_bits", "width": (params["addr_w"] - 2) - 22},
                {"name": "unused_m2_araddr_bits", "width": (params["addr_w"] - 2) - 28},
                {"name": "unused_m2_awaddr_bits", "width": (params["addr_w"] - 2) - 28},
                {"name": "unused_m3_araddr_bits", "width": (params["addr_w"] - 2) - 28},
                {"name": "unused_m3_awaddr_bits", "width": (params["addr_w"] - 2) - 28},
            ],
        },
        {
            "name": "bootrom_cbus",
            "descr": "iob-system boot controller data interface",
            "signals": {
                "type": "axi",
                "prefix": "bootrom_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": params["addr_w"] - 2 - 2,
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
                "LOCK_W": "1",
            },
        },
        {
            "name": "axi_periphs_cbus",
            "descr": "AXI bus for peripheral CSRs",
            "signals": {
                "type": "axi",
                "prefix": "periphs_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": params["addr_w"] - 2 - 2,
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        {
            "name": "iob_periphs_cbus",
            "descr": "AXI-Lite bus for peripheral CSRs",
            "signals": {
                "type": "iob",
                "prefix": "periphs_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": params["addr_w"] - 2 - 2,
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        # Peripheral cbus wires added automatically
        # NOTE: Add other peripheral wires here
    ]
    if not params["use_extmem"]:
        attributes_dict["wires"] += [
            {
                "name": "axi_m",
                "descr": "Unused AXI master interface (for use_extmem=0)",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"] - 2,
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ]
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_vexriscv",
            "instance_name": "cpu",
            "instance_description": "RISC-V CPU instance",
            "parameters": {
                "AXI_ID_W": "1",
                "AXI_ADDR_W": params["addr_w"],
                "AXI_DATA_W": params["data_w"],
                "AXI_LEN_W": "AXI_LEN_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst",
                "i_bus_m": (
                    "cpu_ibus",
                    [
                        "cpu_i_axi_arid[0]",
                        "cpu_i_axi_rid[0]",
                        "cpu_i_axi_awid[0]",
                        "cpu_i_axi_bid[0]",
                    ],
                ),
                "d_bus_m": (
                    "cpu_dbus",
                    [
                        "cpu_d_axi_arid[0]",
                        "cpu_d_axi_rid[0]",
                        "cpu_d_axi_awid[0]",
                        "cpu_d_axi_bid[0]",
                    ],
                ),
                "plic_interrupts_i": "interrupts",
                "plic_cbus_s": (
                    "plic_cbus",
                    ["plic_cbus_iob_addr[22-2-1:0]"],
                ),
                "clint_cbus_s": (
                    "clint_cbus",
                    ["clint_cbus_iob_addr[16-2-1:0]"],
                ),
            },
        },
        {
            "core_name": "iob_axi_interconnect2",
            "name": params["name"] + "_axi_interconnect",
            "instance_name": "iob_axi_interconnect",
            "instance_description": "AXI interconnect instance",
            "parameters": {
                "ID_W": "AXI_ID_W",
                "LEN_W": "AXI_LEN_W",
                # "INT_MEM_ADDR_W": f"{params['fw_addr_w']} - 2",
                # "MEM_ADDR_W": "AXI_ADDR_W - 2",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst",
                "s0_axi_s": "cpu_ibus",
                "s1_axi_s": "cpu_dbus",
                "m0_axi_m": (
                    "int_mem_axi_m",
                    [
                        "{unused_m0_araddr_bits, int_mem_axi_araddr_o}",
                        "{unused_m0_awaddr_bits, int_mem_axi_awaddr_o}",
                    ],
                ),
                "m1_axi_m": (
                    "axi_m",
                    (
                        [
                            "{unused_m1_araddr_bits, axi_araddr_o}",
                            "{unused_m1_awaddr_bits, axi_awaddr_o}",
                            "axi_arlock_o[0]",
                            "axi_awlock_o[0]",
                        ]
                        if params["use_extmem"]
                        else []
                    ),
                ),
                "m2_axi_m": (
                    "bootrom_cbus",
                    [
                        "{unused_m2_araddr_bits, bootrom_axi_araddr}",
                        "{unused_m2_awaddr_bits, bootrom_axi_awaddr}",
                    ],
                ),
                "m3_axi_m": (
                    "axi_periphs_cbus",
                    [
                        "{unused_m3_araddr_bits, periphs_axi_araddr}",
                        "{unused_m3_awaddr_bits, periphs_axi_awaddr}",
                        "periphs_axi_awlock[0]",
                        "periphs_axi_arlock[0]",
                    ],
                ),
            },
            "addr_w": params["addr_w"] - 2,
            "data_w": params["data_w"],
            "lock_w": 1,
            "num_slaves": 2,
            "num_masters": 4,
        },
    ]
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_bootrom",
            "instance_name": "bootrom",
            "instance_description": "Boot ROM peripheral",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "cbus_s": (
                    "bootrom_cbus",
                    [
                        f"bootrom_axi_araddr[{params['bootrom_addr_w']+1}-2-1:0]",
                        "bootrom_axi_arid[0]",
                        "bootrom_axi_rid[0]",
                        "{1'b0, bootrom_axi_arlock}",
                        f"bootrom_axi_awaddr[{params['bootrom_addr_w']+1}-2-1:0]",
                        "bootrom_axi_awid[0]",
                        "bootrom_axi_bid[0]",
                        "{1'b0, bootrom_axi_awlock}",
                    ],
                ),
                "ext_rom_bus_io": "rom_bus_io",
            },
            "bootrom_addr_w": params["bootrom_addr_w"],
            "soc_name": params["name"],
        },
        {
            "core_name": "iob_axi2iob",
            "instance_name": "periphs_axi2iob",
            "instance_description": "Convert AXI to AXI lite for CLINT",
            "parameters": {
                "AXI_ID_WIDTH": "AXI_ID_W",
                "ADDR_WIDTH": params["addr_w"] - 2 - 2,
                "DATA_WIDTH": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "axi_s": (
                    "axi_periphs_cbus",
                    [
                        "periphs_axi_arlock[0]",
                        "periphs_axi_awlock[0]",
                    ],
                ),
                "iob_m": "iob_periphs_cbus",
            },
        },
        {
            "core_name": "iob_split",
            "name": params["name"] + "_pbus_split",
            "instance_name": "iob_pbus_split",
            "instance_description": "Split between peripherals",
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "reset_i": "split_reset",
                "input_s": "iob_periphs_cbus",
                # Peripherals cbus connections added automatically
            },
            "num_outputs": 0,  # Num outputs configured automatically
            "addr_w": params["addr_w"] - 2 - 2,
        },
        # Peripherals
        {
            "core_name": "iob_uart",
            "instance_name": "UART0",
            "instance_description": "UART peripheral",
            "peripheral_addr_w": 3,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
                "rs232_m": "rs232_m",
            },
        },
        {
            "core_name": "iob_timer",
            "instance_name": "TIMER0",
            "instance_description": "Timer peripheral",
            "peripheral_addr_w": 4,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
            },
        },
        # NOTE: Instantiate other peripherals here, using the 'peripheral_addr_w' flag
        #
        # Modules that need to be setup, but are not instantiated directly inside
        # 'iob_system' Verilog module
        # Testbench
        {
            "core_name": "iob_tasks",
            "instance_name": "iob_tasks_inst",
            "instantiate": False,
            "dest_dir": "hardware/simulation/src",
        },
    ]
    attributes_dict["superblocks"] = [
        # Memory wrapper
        {
            "core_name": "iob_system_mwrap",
            "instance_name": "iob_system_mwrap",
            "iob_system_params": params,
            "superblocks": [
                # Synthesis module (needed for macros)
                {
                    "core_name": "iob_system_syn",
                    "instance_name": "iob_system_syn",
                    "dest_dir": "hardware/syn/src",
                    "iob_system_params": params,
                },
                # Simulation wrapper
                {
                    "core_name": "iob_system_sim",
                    "instance_name": "iob_system_sim",
                    "dest_dir": "hardware/simulation/src",
                    "iob_system_params": params,
                },
                # FPGA wrappers added automatically
            ],
        },
    ]
    attributes_dict["sw_modules"] = [
        # Software modules
        {
            "core_name": "iob_printf",
            "instance_name": "iob_printf_inst",
        },
    ]
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
   //assign interrupts = {{30{1'b0}}, uart_interrupt_o, 1'b0};
   assign interrupts = {{30{1'b0}}, 1'b0, 1'b0};
"""
        }
    ]
    if not params["use_extmem"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
   // Connect inputs of unused external memory AXI interface to zero
   assign axi_arready = 'b0;
   assign axi_rdata = 'b0;
   assign axi_rresp = 'b0;
   assign axi_rvalid = 'b0;
   assign axi_rid = 'b0;
   assign axi_rlast = 'b0;
   assign axi_awready = 'b0;
   assign axi_wready = 'b0;
   assign axi_bresp = 'b0;
   assign axi_bvalid = 'b0;
   assign axi_bid = 'b0;
"""
            }
        ]

    iob_system_scripts(attributes_dict, params, py_params_dict)

    return attributes_dict
