# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import sys
import shutil

# Add iob-system scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scripts"))

from iob_system_utils import update_params


def setup(py_params: dict):
    # Python parameters passed in py_params will override default values specified below and the ones of iob_system specified at: https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/iob_system/iob_system.py

    # Dictionary of available python parameters for iob_system_linux
    # Format: [parameter name]: [parameter default value]
    params = {
        "dma_demo": False,
    }
    # Set new default values for python parameters of iob_system (parent module)
    # List of iob_system python parameters available at: https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/iob_system/iob_system.py
    iob_system_default_overrides = {
        "use_intmem": False,
        "use_extmem": True,
        "mem_addr_w": 26,
        "bootrom_addr_w": 15,
        "fw_baseaddr": 0,
        "cpu": "iob_vexriscv",
        "include_snippet": False,  # Don't include iob_system's snippets. We will use our own.
    }
    iob_system_default_overrides |= {
        "fw_addr_w": iob_system_default_overrides["mem_addr_w"],
    }

    # Update parameters values with ones given in python parameters
    update_params(params, py_params)

    # py_params (not specific to linux) will be passed to iob_system. Merge with new default overrides.
    non_linux_py_params = {k: v for k, v in py_params.items() if k not in params}
    py_params = {**iob_system_default_overrides, **non_linux_py_params}

    #
    # Verilog snippets
    #
    verilog_snippet = """
   assign interrupts = {{30{1'b0}}, uart_interrupt, 1'b0};
"""

    if params["dma_demo"]:
        verilog_snippet += """
   assign AXISTREAMIN0_axis_clk_i = clk_i;
   assign AXISTREAMIN0_axis_cke_i = cke_i;
   assign AXISTREAMIN0_axis_arst_i = arst_i;
   assign AXISTREAMOUT0_axis_clk_i = clk_i;
   assign AXISTREAMOUT0_axis_cke_i = cke_i;
   assign AXISTREAMOUT0_axis_arst_i = arst_i;
"""

    #
    # Py2hwsw dictionary describing current core
    #

    attributes_dict = {
        # Every attribute in this dictionary will override/append to the ones of the iob_system parent core.
        "board_list": [
            "iob_aes_ku040_db_g",
            "iob_cyclonev_gt_dk",
            "iob_zybo_z7",
        ],
        "confs": [
            {  # Used for software.
                "name": "OS_RANGE",
                "descr": "Linux OS address range in hex",
                "type": "M",
                "val": hex(1 << py_params["mem_addr_w"]),
                "min": "1",
                "max": "32",
            },
            {  # For iob_spi_master
                "name": "FPGA_TOOL",
                "descr": "Use IPs from fpga tool. Avaliable options: 'XILINX', 'other'.",
                "type": "P",
                "val": '"other"',
                "min": "NA",
                "max": "NA",
            },
            # {
            #     "name": "DMA_DEMO",
            #     "type": "M",
            #     "val": True,
            #     "min": "0",
            #     "max": "1",
            #     "descr": "Enable DMA demo",
            # },
        ],
        "ports": [
            {
                # Add new rs232 port for uart
                "name": "rs232_m",
                "descr": "iob-system-linux uart interface",
                "signals": {
                    "type": "rs232",
                },
            },
            # NOTE: Add other ports here.
        ],
        "wires": [
            # UART
            {
                "name": "uart_interrupt",
                "descr": "Uart interrupt",
                "signals": [
                    {"name": "uart_interrupt", "width": 1},
                ],
            },
            # SPI master
            # {
            #     "name": "spi_cache",
            #     "descr": "SPI cache bus",
            #     "if_defined": "RUN_FLASH",
            #     "signals": {
            #         "type": "iob",
            #         "prefix": "spi_",
            #     },
            # },
            {
                "name": "spi_flash",
                "descr": "SPI flash bus",
                "signals": [
                    {"name": "ss", "width": 1},
                    {"name": "sclk", "width": 1},
                    {"name": "miso", "width": 1},
                    {"name": "mosi", "width": 1},
                    {"name": "wp_n", "width": 1},
                    {"name": "hold_n", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                # Instantiate a UART16550 core from: https://github.com/IObundle/iob-uart16550
                "core_name": "iob_uart16550",
                "instance_name": "UART0",  # Use same name as one inherited from iob_system to replace it
                "instance_description": "UART peripheral",
                "is_peripheral": True,
                "parameters": {},
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Cbus connected automatically
                    "rs232_m": "rs232_m",
                    "interrupt_o": "uart_interrupt",
                },
            },
            # {
            #     "core_name": "iob_eth",
            #     "instance_name": "ETH0",
            #     "instance_description": "Ethernet interface",
            #     "peripheral_addr_w": 12,
            #     "parameters": {
            #         "AXI_ID_W": "AXI_ID_W",
            #         "AXI_LEN_W": "AXI_LEN_W",
            #         "AXI_ADDR_W": params["addr_w"],
            #         "AXI_DATA_W": params["data_w"],
            #     },
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #         "axi_m": (
            #             "eth_axi",
            #             [
            #                 "eth_axi_arid[0]",
            #                 "eth_axi_rid[0]",
            #                 "eth_axi_awid[0]",
            #                 "eth_axi_bid[0]",
            #             ],
            #         ),
            #         "inta_o": "ethernet_interrupt",
            #         "phy_io": "phy_io",
            #     },
            # },
            # {
            #     # Instantiate a VERSAT core from: https://github.com/IObundle/iob-versat
            #     "core_name": "iob_versat",
            #     "instance_name": "VERSAT0",
            #     "instance_description": "VERSAT accelerator",
            #     "is_peripheral": True,
            #     "parameters": {},
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #         # Cbus connected automatically
            #         # TODO:
            #     },
            # },
            {
                # Instantiate a SPI master core from: https://github.com/IObundle/iob-spi
                "core_name": "iob_spi_master",
                "instance_name": "SPI0",
                "instance_description": "SPI master peripheral",
                "is_peripheral": True,
                "parameters": {
                    "FPGA_TOOL": "FPGA_TOOL",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Cbus connected automatically
                    # "cache_iob_s": "spi_cache",
                    "flash_io": "spi_flash",
                },
            },
            #
            # Peripherals for DMA demo
            # {
            #     "core_name": "iob_axistream_in",
            #     "instance_name": "AXISTREAMIN0",
            #     "instance_description": "AXI-Stream input interface",
            #     "parameters": {
            #         "TDATA_W": "32",
            #         "FIFO_ADDR_W": "4",
            #     },
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #         "interrupt_o": "axistream_in_interrupt",
            #         "axistream_io": "axistream_in_axis", # AXI-Stream in and out should be connected in loopback for demo
            #         "sys_axis_io": "dma_axis_in",
            #         "iob_csrs_cbus_s": "axistream_in_csrs",
            #     },
            # },
            # {
            #     "core_name": "iob_axistream_out",
            #     "instance_name": "AXISTREAMOUT0",
            #     "instance_description": "AXI-Stream output interface",
            #     "parameters": {
            #         "TDATA_W": "32",
            #         "FIFO_ADDR_W": "4",
            #     },
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #         "interrupt_o": "axistream_out_interrupt",
            #         "axistream_io": "axistream_out_axis",
            #         "sys_axis_io": "dma_axis_out",
            #         "iob_csrs_cbus_s": "axistream_out_csrs",
            #     },
            # },
            # {
            #     "core_name": "iob_dma",
            #     "instance_name": "DMA0",
            #     "instance_description": "DMA interface",
            #     "parameters": {
            #         "AXI_ID_W": "AXI_ID_W",
            #         "AXI_LEN_W": "AXI_LEN_W",
            #         "AXI_ADDR_W": "AXI_ADDR_W",
            #         "N_INPUTS": "1",
            #         "N_OUTPUTS": "1",
            #     },
            #     "connect": {
            #         "clk_en_rst_s": "clk_en_rst_s",
            #     },
            # },
            # NOTE: Add other components/peripherals here.
        ],
        "sw_modules": [
            {
                "core_name": "iob_linux",
                "instance_name": "iob_linux_inst",
            },
        ],
        "snippets": [{"verilog_code": verilog_snippet}],
    }

    # Iob_system_linux is actually a derived core of iob_system. Therefore, set iob_system as the parent core and pass iob_system_linux's attributes_dict as a python paremter.
    attributes_dict = {
        "version": "0.8",
        "parent": {
            # IOb-System-Linux is a derived core of iob_system: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_system
            # IOb-System-Linux will inherit all attributes/files from the iob_system core.
            "core_name": "iob_system",
            # Every parameter in the lines below will be passed to the iob_system parent core.
            # Full list of parameters availabe here: https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/iob_system/iob_system.py
            "system_attributes": attributes_dict,
            # NOTE: Place other iob_system python parameters here
            **py_params,
        },
    }

    #
    # Post-processing
    #

    # setup_dir = os.path.dirname(__file__)

    # # Copy linux kernel and rootfs to build directory
    # dst = f"{cls.build_dir}/software/src"
    # src = f"{setup_dir}/submodules/OS/software/OS_build"
    # files = ["rootfs.cpio.gz", "Image"]
    # for fname in files:
    #     src_file = os.path.join(src, fname)
    #     if os.path.isfile(src_file):
    #         shutil.copy2(src_file, dst)
    #
    # # Copy scripts to build directory
    if py_params.get("py2hwsw_target", "") == "setup" and py_params["build_dir"]:
        for src_file in [
            "scripts/check_if_run_linux.py",
        ]:
            src = os.path.join(os.path.dirname(__file__), src_file)
            dst = os.path.join(py_params["build_dir"], src_file)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            # Hack for Nix: Files copied from Nix's py2hwsw package do not contain write permissions
            os.system("chmod -R ug+w " + dst)

        # Create symlink for minicom's .minirc.iobundle.dfl
        # Note: Minicom only accepts configuration files starting with ".minirc", and python's setuptools does not copy dotfiles by default.
        #       So, as a workaround, we named the file 'minirc.iobundle.dfl' in the repo, and create a symlink to it during setup.
        fpga_dir = os.path.join(py_params["build_dir"], "hardware/fpga")
        os.makedirs(fpga_dir, exist_ok=True)
        minirc_path = os.path.join(fpga_dir, ".minirc.iobundle.dfl")
        if not os.path.exists(minirc_path):
            os.symlink("minirc.iobundle.dfl", minirc_path)

    #     iob_soc_scripts = [
    #         "terminalMode",
    #         "makehex",
    #         "hex_split",
    #         "hex_join",
    #         "board_client",
    #         "console",
    #         "console_ethernet",
    #     ]
    #     dst = f"{cls.build_dir}/scripts"
    #     for script in iob_soc_scripts:
    #         src_file = f"{setup_dir}/submodules/IOBSOC/scripts/{script}.py"
    #         shutil.copy2(src_file, dst)
    #     src_file = f"{setup_dir}/scripts/check_if_run_linux.py"
    #     shutil.copy2(src_file, dst)
    #
    #     shutil.copy2(
    #         f"{setup_dir}/software/versat/module/versat.ko",
    #         f"{cls.build_dir}/software",
    #     )
    #     shutil.copy2(
    #         f"{setup_dir}/software/tests/exampleTransfer.sh",
    #         f"{cls.build_dir}/software",
    #     )
    #     shutil.copy2(
    #         f"{setup_dir}/software/tests/setupTest.sh",
    #         f"{cls.build_dir}/software",
    #     )
    #     shutil.copy2(
    #         f"{setup_dir}/software/tests/test.sh",
    #         f"{cls.build_dir}/software",
    #     )
    #
    #     shutil.copytree(
    #         f"{setup_dir}/hardware/src/units",
    #         f"{cls.build_dir}/hardware/src",
    #         dirs_exist_ok=True,
    #     )
    #
    #     # Override periphs_tmp.h of iob-soc with one specific for linux
    #     create_periphs_tmp(
    #         cls.name,
    #         next(i["val"] for i in cls.confs if i["name"] == "ADDR_W"),
    #         cls.peripherals,
    #         f"{cls.build_dir}/software/{cls.name}_periphs.h",
    #     )
    #     check_linux_build_macros(cls, f"{setup_dir}/submodules/OS")
    #

    #
    # Versat
    #

    # VERSAT_SPEC = f"{setup_dir}/software/versat/versatSpec.txt"
    # VERSAT_EXTRA_UNITS = os.path.realpath(
    #     os.path.join(os.path.dirname(__file__), "hardware/src/units")
    # )

    # cls.versatType = CreateVersatClass(
    #     False, VERSAT_SPEC, "CryptoAlgos", VERSAT_EXTRA_UNITS, cls.build_dir
    # )

    return attributes_dict
