# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os

# Add iob-system scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from iob_system_utils import convert_params_dict, update_params, iob_system_scripts


def setup(py_params_dict):
    params = {
        "name": ("iob_system", "Name of the generated System"),
        "init_mem": (True, "If should initialize memories from data in .hex files"),
        "use_intmem": (True, "If should include an internal memory"),
        "use_extmem": (False, "If should use external memory (usually DDR)"),
        "use_bootrom": (True, "If should include a bootrom"),
        "use_peripherals": (True, "If should include peripherals"),
        "use_ethernet": (False, "If should setup ethernet ports and testbenches"),
        "addr_w": (32, "CPU address width"),
        "data_w": (32, "CPU data width"),
        "mem_addr_w": (18, "Memory address width"),
        "bootrom_addr_w": (12, "Bootrom address width"),
        "fw_baseaddr": (0, "Firmware base address"),
        "fw_addr_w": (18, "Firmware address width"),
        "include_tester": (True, "If should include a tester system"),
        "include_snippet": (True, "If should include default system snippet"),
        "cpu": (
            "iob_vexriscv",
            """CPU selection.
        If set to "none", the iob_system will export an `iob_s` port for an external
        CPU. This port will give direct access to the system's peripherals. The internal
        memories and crossbar will be removed.""",
        ),
        "system_attributes": (
            {},
            "Core dictionary with attributes to override/append to the ones of iob_system. Usually passed by child cores to add their own components.",
        ),
    }

    # Converts dictionary tuple values into single values without description
    # And creates "python_parameters" list attribute for py2hwsw documentation
    python_parameters_attribute = convert_params_dict(params)

    # Update parameters values with ones given in python parameters
    update_params(params, py_params_dict)

    if params["cpu"] == "none":
        params["use_intmem"] = False
        params["use_extmem"] = False
        params["use_bootrom"] = False

    num_xbar_managers = 0
    for param_name in ["use_intmem", "use_extmem", "use_bootrom", "use_peripherals"]:
        if params[param_name]:
            num_xbar_managers += 1
    xbar_sel_w = (num_xbar_managers - 1).bit_length()

    attributes_dict = {
        "name": params["name"],
        "generate_hw": True,
        "is_system": True,
        "board_list": ["iob_aes_ku040_db_g", "iob_zybo_z7", "iob_cyclonev_gt_dk"],
        "python_parameters": python_parameters_attribute,
        "title": "IOb-System",
        "description": "System-on-Chip (SoC) template",
        "confs": [
            # macros
            {  # Needed for testbench
                "name": "ADDR_W",
                "descr": "Testbench address bus width.",
                "type": "M",
                "val": params["addr_w"],
                "min": "1",
                "max": "32",
            },
            {  # Needed for testbench
                "name": "DATA_W",
                "descr": "Testbench data bus width.",
                "type": "M",
                "val": params["data_w"],
                "min": "1",
                "max": "32",
            },
            {  # Needed for makefile and software
                "name": "INIT_MEM",
                "descr": "Select if memory is pre-initialized with firmware. Otherwise bootloader will request a firmware transfer and load it into memory.",
                "type": "M",
                "val": params["init_mem"],
                "min": "0",
                "max": "1",
            },
            {  # May be used by software
                "name": "USE_INTMEM",
                "descr": "Enable internal memory support.",
                "type": "M",
                "val": params["use_intmem"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for makefile and software
                "name": "USE_EXTMEM",
                "descr": "Enable external memory support.",
                "type": "M",
                "val": params["use_extmem"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for testbench
                "name": "USE_ETHERNET",
                "descr": "Updates system wrappers, testbenches, scripts, and makefiles to support ethernet.",
                "type": "M",
                "val": params["use_ethernet"],
                "min": "0",
                "max": "1",
            },
            {  # Needed for software and makefiles
                "name": "MEM_ADDR_W",
                "descr": "External memory bus address width.",
                "type": "M",
                "val": params["mem_addr_w"],
                "min": "0",
                "max": "32",
            },
            {  # Needed for software
                "name": "FW_BASEADDR",
                "descr": "Firmware address",
                "type": "M",
                "val": params["fw_baseaddr"],
                "min": "0",
                "max": "0x7FFFFFFF",
            },
            {  # Needed for software
                "name": "FW_ADDR_W",
                "descr": "Width of address space reserved for Firmware.",
                "type": "M",
                "val": params["fw_addr_w"],
                "min": "0",
                "max": "32",
            },
            {  # Needed for testbench
                "name": "RST_POL",
                "descr": "Reset signal polarity.",
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
                "type": "D",
                "val": "1",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "D",
                "val": params["mem_addr_w"],
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "D",
                "val": params["data_w"],
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "D",
                "val": "4",
                "min": "1",
                "max": "4",
            },
            #
            # False-parameters for generated memories
            #
            # BOOTROM
            {
                "name": "BOOTROM_MEM_HEXFILE",
                "descr": "Bootloader file name",
                "type": "D",
                "val": f'"{params["name"]}_bootrom"',
                "min": "NA",
                "max": "NA",
            },
            # INTERNAL MEMORY
            {
                "name": "EXT_MEM_HEXFILE",
                "descr": "Firmware file name",
                "type": "D",
                "val": f'"{params["name"]}_firmware"',
                "min": "NA",
                "max": "NA",
            },
        ],
    }
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "iob_clk",
            },
        },
    ]
    if params["use_bootrom"]:
        attributes_dict["ports"] += [
            {
                "name": "rom_bus_m",
                "descr": "Ports for connection with boot ROM memory",
                "signals": {
                    "type": "rom_sp",
                    "prefix": "bootrom_mem_",
                    "ADDR_W": params["bootrom_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]
    if params["use_intmem"]:
        attributes_dict["ports"] += [
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": params["mem_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]
    if params["use_extmem"]:
        attributes_dict["ports"] += [
            {
                "name": "axi_m",
                "descr": "AXI manager interface for DDR memory",
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
    if params["use_peripherals"]:
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
    if params["cpu"] == "none":
        attributes_dict["ports"] += [
            {
                "name": "iob_s",
                "descr": "IOb subordinate interface for external CPU. Gives direct access to system peripherals",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ]

    attributes_dict["wires"] = [
        {
            "name": "interrupts",
            "descr": "System interrupts",
            "signals": [
                {"name": "interrupts", "width": 32},
            ],
        },
    ]
    if params["cpu"] != "none":
        # Crossbar wires
        attributes_dict["wires"] += [
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
                "name": "cpu_ibus",
                "descr": "CPU instruction bus",
                "signals": {
                    "type": "axi",
                    "prefix": "cpu_i_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"],
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
                    "ADDR_W": params["addr_w"],
                    "DATA_W": params["data_w"],
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
            {
                "name": "unused_interconnect_bits",
                "descr": "Wires to connect to unused output bits of interconnect",
                "signals": [
                    {
                        "name": "unused_m0_araddr_bits",
                        "width": params["addr_w"] - params["mem_addr_w"],
                    },
                    {
                        "name": "unused_m0_awaddr_bits",
                        "width": params["addr_w"] - params["mem_addr_w"],
                    },
                    {
                        "name": "unused_m1_araddr_bits",
                        "width": f"{params['addr_w']} - AXI_ADDR_W",
                    },
                    {
                        "name": "unused_m1_awaddr_bits",
                        "width": f"{params['addr_w']} - AXI_ADDR_W",
                    },
                    {
                        "name": "unused_m2_araddr_bits",
                        "width": params["addr_w"] - (params["bootrom_addr_w"] + 1),
                    },
                    {
                        "name": "unused_m2_awaddr_bits",
                        "width": params["addr_w"] - (params["bootrom_addr_w"] + 1),
                    },
                    {"name": "unused_m3_araddr_bits", "width": xbar_sel_w},
                    {"name": "unused_m3_awaddr_bits", "width": xbar_sel_w},
                ],
            },
        ]
    if params["use_intmem"]:
        attributes_dict["wires"] += [
            {
                "name": "int_mem_axi",
                "descr": "AXI manager interface for internal memory",
                "signals": {
                    "type": "axi",
                    "prefix": "int_mem_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": f"{params['mem_addr_w']}",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ]
    if params["use_bootrom"]:
        attributes_dict["wires"] += [
            {
                "name": "bootrom_cbus",
                "descr": "iob-system boot controller data interface",
                "signals": {
                    "type": "axi",
                    "prefix": "bootrom_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["bootrom_addr_w"] + 1,  # +1 for csrs
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
        ]
    if params["use_peripherals"] and params["cpu"] != "none":
        attributes_dict["wires"] += [
            {
                "name": "axi_periphs_cbus",
                "descr": "AXI bus for peripheral CSRs",
                "signals": {
                    "type": "axi",
                    "prefix": "periphs_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"] - xbar_sel_w,
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
        ]
    if params["use_peripherals"]:
        attributes_dict["wires"] += [
            {
                "name": "split_reset",
                "descr": "Reset signal for iob_split components",
                "signals": [
                    {"name": "arst_i"},
                ],
            },
            {
                "name": "iob_periphs_cbus",
                "descr": "AXI-Lite bus for peripheral CSRs",
                "signals": {
                    "type": "iob",
                    "prefix": "periphs_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"] - xbar_sel_w,
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            # Peripheral cbus wires added automatically
            # NOTE: Add other peripheral wires here
        ]
    attributes_dict["subblocks"] = []
    if params["cpu"] != "none":
        attributes_dict["subblocks"] += [
            {
                "core_name": params["cpu"],
                "name": params["name"] + "_" + params["cpu"],
                "instance_name": "cpu",
                "instance_description": "RISC-V CPU instance",
                # Reset address and uncached range are filled automatically
                # "reset_addr": 0x00000000,
                # "uncached_start_addr": 0x00000000,
                # "uncached_size": 2**32,
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
                        ["plic_cbus_iob_addr[22-1:0]"],
                    ),
                    "clint_cbus_s": (
                        "clint_cbus",
                        ["clint_cbus_iob_addr[16-1:0]"],
                    ),
                },
            },
            {
                "core_name": "iob_axi_full_xbar",
                "name": params["name"] + "_axi_full_xbar",
                "instance_name": "iob_axi_full_xbar",
                "instance_description": "AXI full xbar instance",
                "parameters": {
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "s0_axi_s": "cpu_ibus",
                    "s1_axi_s": "cpu_dbus",
                    # Manager interfaces connected below
                },
                "addr_w": params["addr_w"],
                "data_w": params["data_w"],
                "lock_w": 1,
                "num_subordinates": 2,
            },
        ]
        full_xbar_manager_interfaces = {
            "use_intmem": (
                "int_mem_axi",
                [
                    "{unused_m0_araddr_bits, int_mem_axi_araddr}",
                    "{unused_m0_awaddr_bits, int_mem_axi_awaddr}",
                ],
            ),
            "use_extmem": (
                "axi_m",
                [
                    "{unused_m1_araddr_bits, axi_araddr_o}",
                    "{unused_m1_awaddr_bits, axi_awaddr_o}",
                ],
            ),
            "use_bootrom": (
                "bootrom_cbus",
                [
                    "{unused_m2_araddr_bits, bootrom_axi_araddr}",
                    "{unused_m2_awaddr_bits, bootrom_axi_awaddr}",
                ],
            ),
            "use_peripherals": (
                "axi_periphs_cbus",
                [
                    "{unused_m3_araddr_bits, periphs_axi_araddr}",
                    "{unused_m3_awaddr_bits, periphs_axi_awaddr}",
                    "periphs_axi_awlock[0]",
                    "periphs_axi_arlock[0]",
                ],
            ),
        }
        # Connect xbar manager interfaces
        num_managers = 0
        for param_name, interface_connection in full_xbar_manager_interfaces.items():
            if params[param_name]:
                attributes_dict["subblocks"][-1]["connect"] |= {
                    f"m{num_managers}_axi_m": interface_connection
                }
                num_managers += 1
        attributes_dict["subblocks"][-1]["num_managers"] = num_managers

    if params["use_intmem"]:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_axi_ram",
                "instance_name": "internal_memory",
                "instance_description": "Internal memory",
                "parameters": {
                    "ID_WIDTH": "AXI_ID_W",
                    "LEN_WIDTH": "AXI_LEN_W",
                    "ADDR_WIDTH": params["mem_addr_w"],
                    "DATA_WIDTH": "AXI_DATA_W",
                },
                "connect": {
                    "clk_i": "clk",
                    "rst_i": "rst",
                    "axi_s": (
                        "int_mem_axi",
                        [
                            "{1'b0, int_mem_axi_arlock}",
                            "{1'b0, int_mem_axi_awlock}",
                        ],
                    ),
                    "external_mem_bus_m": "external_mem_bus_m",
                },
            },
        ]
    if params["use_bootrom"]:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_bootrom",
                "instance_name": "bootrom",
                "instance_description": "Boot ROM peripheral",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_csrs_cbus_s": (
                        "bootrom_cbus",
                        [
                            "{1'b0, bootrom_axi_arlock}",
                            "{1'b0, bootrom_axi_awlock}",
                        ],
                    ),
                    "rom_bus_m": "rom_bus_m",
                },
                "bootrom_addr_w": params["bootrom_addr_w"],
                "soc_name": params["name"],
            },
        ]
    if params["use_peripherals"] and params["cpu"] != "none":
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_axi2iob",
                "instance_name": "periphs_axi2iob",
                "instance_description": "Convert AXI to AXI lite for CLINT",
                "parameters": {
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                    "ADDR_WIDTH": params["addr_w"] - xbar_sel_w,
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
        ]
    if params["use_peripherals"]:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_split",
                "name": params["name"] + "_pbus_split",
                "instance_name": "iob_pbus_split",
                "instance_description": "Split between peripherals",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "split_reset",
                    "input_s": (
                        "iob_periphs_cbus" if params["cpu"] != "none" else "iob_s"
                    ),
                    # Peripherals cbus connections added automatically
                },
                "num_outputs": 0,  # Num outputs configured automatically
                "addr_w": params["addr_w"] - xbar_sel_w,
            },
            # Peripherals
            {
                "core_name": "iob_uart",
                "instance_name": "UART0",
                "instance_description": "UART peripheral",
                # This attribute signals to iob_system scripts that this block is a peripheral
                "is_peripheral": True,
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
                "is_peripheral": True,
                "parameters": {},
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Cbus connected automatically
                },
            },
            # NOTE: Instantiate other peripherals here, using the 'is_peripheral' flag
        ]
    attributes_dict["superblocks"] = [
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
    ]
    if params["include_tester"]:
        # Append tester to "superblocks" list of memory wrapper
        attributes_dict["superblocks"] += [
            {
                "core_name": "iob_system_tester",
                "instance_name": "iob_system_tester",
                "iob_system_params": params,
                "dest_dir": "tester",
            },
            # # Create second tester but without CPU
            # # This Tester's verification instruments will be controlled by testbench
            # {
            #     "core_name": "iob_system_tester",
            #     "instance_name": "iob_system_tester_no_cpu",
            #     "cpu": "none",
            #     "iob_system_params": params,
            #     "dest_dir": "tester_no_cpu",
            # },
        ]
    attributes_dict["sw_modules"] = [
        # Software modules
        {
            "core_name": "iob_printf",
            "instance_name": "iob_printf_inst",
        },
    ]

    attributes_dict["snippets"] = []
    if params["include_snippet"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
   //assign interrupts = {{30{1'b0}}, uart_interrupt_o, 1'b0};
   assign interrupts = {{30{1'b0}}, 1'b0, 1'b0};
"""
            }
        ]

    iob_system_scripts(attributes_dict, params, py_params_dict)

    return attributes_dict
