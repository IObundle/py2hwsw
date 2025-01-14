# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import shutil
import sys
import os
import subprocess
from iob_base import nix_permission_hack

sys.path.append(f"{os.path.dirname(__file__)}/scripts/")
from gen_custom_config_build import gen_custom_config_build


def setup(py_params_dict):
    gen_custom_config_build(py_params_dict)

    # Copy simulation testbench utility files
    dst = f"{py_params_dict['build_dir']}/hardware/simulation/src"
    os.makedirs(dst, exist_ok=True)
    src = f"{os.path.dirname(__file__)}/hardware/simulation/src"
    for src_file in [
        "iob_eth_driver_tb.v",
        "iob_eth_driver_tb.h",
        "iob_eth_driver_tb.cpp",
        "iob_eth_defines.vh",
        "iob_eth_defines_verilator.h",
        "iob_eth_defines_tasks.vs",
    ]:
        shutil.copy2(os.path.join(src, src_file), dst)
        nix_permission_hack(dst)

    shutil.copytree(
        f"{os.path.dirname(__file__)}/scripts",
        f"{py_params_dict['build_dir']}/scripts",
        dirs_exist_ok=True,
    )
    nix_permission_hack(f"{py_params_dict['build_dir']}/scripts")

     # Check if pyRawWrapper exists
    pyRawWrapper_path = f"{py_params_dict['build_dir']}/scripts/pyRawWrapper/pyRawWrapper"

    if not os.path.exists(pyRawWrapper_path):
        print("Create pyRawWrapper for RAW access to ethernet frames")

        # Run make compile
        subprocess.run(
            ["make", "-C", f"{py_params_dict['build_dir']}/scripts/pyRawWrapper", "compile"],
            check=True
        )

        # Run sudo make set-capabilities
        subprocess.run(
            ["sudo", "make", "-C", f"{py_params_dict['build_dir']}/scripts/pyRawWrapper", "set-capabilities"],
            check=True
        )

    attributes_dict = {
        "generate_hw": True,
        "version": "0.1",
        "confs": [
            # Macros
            {
                "name": "PREAMBLE",
                "type": "M",
                "val": "8'h55",
                "min": "NA",
                "max": "NA",
                "descr": "Ethernet packet preamble value",
            },
            {
                "name": "PREAMBLE_LEN",
                "type": "M",
                "val": "7",  # Should it be 7 + 2 bytes to align data transfers?
                "max": "NA",
                "min": "NA",
                "descr": "Ethernet packet preamble length",
            },
            {
                "name": "SFD",
                "type": "M",
                "val": "8'hD5",
                "min": "NA",
                "max": "NA",
                "descr": "Start Frame Delimiter",
            },
            {
                "name": "MAC_ADDR_LEN",
                "type": "M",
                "val": "6",
                "min": "NA",
                "max": "NA",
                "descr": "Ethernet MAC address length",
            },
            # Parameters
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "128",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "`IOB_ETH_CSRS_ADDR_W",
                "min": "NA",
                "max": "128",
                "descr": "Address bus width",
            },
            # External memory interface
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
                "descr": "AXI ID bus width",
            },
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "24",
                "min": "1",
                "max": "32",
                "descr": "AXI address bus width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "DATA_W",
                "min": "1",
                "max": "32",
                "descr": "AXI data bus width",
            },
            {
                "name": "AXI_LEN_W",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "4",
                "descr": "AXI burst length width",
            },
            # Ethernet
            {
                "name": "PHY_RST_CNT",
                "type": "P",
                "val": "20'hFFFFF",
                "min": "NA",
                "max": "NA",
                "descr": "PHY reset counter value. Sets the duration of the PHY reset signal",
            },
            {
                "name": "BD_NUM_LOG2",
                "type": "P",
                "val": "7",
                "min": "NA",
                "max": "7",
                "descr": "Log2 amount of buffer descriptors",
            },
            {
                "name": "BUFFER_W",
                "type": "P",
                "val": "11",
                "min": "0",
                "max": "32",
                "descr": "Buffer size",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "clk_en_rst",
                },
            },
            {
                "name": "cbus_s",
                "descr": "CPU native interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": 12 - 2,
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "axi_m",
                "descr": "AXI master interface for external memory",
                "signals": {
                    "type": "axi",
                },
            },
            {
                "name": "inta_o",
                "descr": "Interrupt Output A",
                "signals": [
                    {"name": "inta_o", "width": 1},
                ],
            },
            {
                "name": "phy_io",
                "descr": "PHY Interface Ports",
                "signals": [
                    {
                        "name": "MTxClk_i",
                        "width": "1",
                        "descr": "Transmit Nibble or Symbol Clock. The PHY provides the MTxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the transfer of MTxD[3:0], MtxEn, and MTxErr.",
                    },
                    {
                        "name": "MTxEn_o",
                        "width": "1",
                        "descr": "Transmit Enable. When asserted, this signal indicates to the PHY that the data MTxD[3:0] is valid and the transmission can start. The transmission starts with the first nibble of the preamble. The signal remains asserted until all nibbles to be transmitted are presented to the PHY. It is deasserted prior to the first MTxClk, following the final nibble of a frame.",
                    },
                    {
                        "name": "MTxD_o",
                        "width": "4",
                        "descr": "Transmit Data Nibble. Signals are the transmit data nibbles. They are synchronized to the rising edge of MTxClk. When MTxEn is asserted, PHY accepts the MTxD.",
                    },
                    {
                        "name": "MTxErr_o",
                        "width": "1",
                        "descr": "Transmit Coding Error. When asserted for one MTxClk clock period while MTxEn is also asserted, this signal causes the PHY to transmit one or more symbols that are not part of the valid data or delimiter set somewhere in the frame being transmitted to indicate that there has been a transmit coding error.",
                    },
                    {
                        "name": "MRxClk_i",
                        "width": "1",
                        "descr": "Receive Nibble or Symbol Clock. The PHY provides the MRxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the reception of MRxD[3:0], MRxDV, and MRxErr.",
                    },
                    {
                        "name": "MRxDv_i",
                        "width": "1",
                        "descr": "Receive Data Valid. The PHY asserts this signal to indicate to the Rx MAC that it is presenting the valid nibbles on the MRxD[3:0] signals. The signal is asserted synchronously to the MRxClk. MRxDV is asserted from the first recovered nibble of the frame to the final recovered nibble. It is then deasserted prior to the first MRxClk that follows the final nibble.",
                    },
                    {
                        "name": "MRxD_i",
                        "width": "4",
                        "descr": "Receive Data Nibble. These signals are the receive data nibble. They are synchronized to the rising edge of MRxClk. When MRxDV is asserted, the PHY sends a data nibble to the Rx MAC. For a correctly interpreted frame, seven bytes of a preamble and a completely formed SFD must be passed across the interface.",
                    },
                    {
                        "name": "MRxErr_i",
                        "width": "1",
                        "descr": "Receive Error. The PHY asserts this signal to indicate to the Rx MAC that a media error was detected during the transmission of the current frame. MRxErr is synchronous to the MRxClk and is asserted for one or more MRxClk clock periods and then deasserted.",
                    },
                    {
                        "name": "MColl_i",
                        "width": "1",
                        "descr": "Collision Detected. The PHY asynchronously asserts the collision signal MColl after the collision has been detected on the media. When deasserted, no collision is detected on the media.",
                    },
                    {
                        "name": "MCrS_i",
                        "width": "1",
                        "descr": "Carrier Sense. The PHY asynchronously asserts the carrier sense MCrS signal after the medium is detected in a non-idle state. When deasserted, this signal indicates that the media is in an idle state (and the transmission can start).",
                    },
                    {
                        "name": "MDC_o",
                        "width": "1",
                        "descr": "Management Data Clock. This is a clock for the MDIO serial data channel.",
                    },
                    {
                        "name": "MDIO_o",  # TODO: Make this port bidirectional. Probably best by using two separate ports, as 'inout' may not be synthesizable.
                        "width": "1",
                        "descr": "Management Data Input/Output. Bi-directional serial data channel for PHY/STA communication.",
                    },
                    {
                        "name": "phy_rstn_o",
                        "width": "1",
                        "descr": "Reset signal for PHY. Duration configurable via PHY_RST_CNT parameter.",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "moder",
                "descr": "",
                "signals": [
                    {"name": "moder_wr", "width": 32},
                    {"name": "moder_rd", "width": 32},
                ],
            },
            {
                "name": "int_source",
                "descr": "",
                "signals": [
                    {"name": "int_source_wr", "width": 32},
                    {"name": "int_source_rd", "width": 32},
                ],
            },
            {
                "name": "int_mask",
                "descr": "",
                "signals": [
                    {"name": "int_mask_wr", "width": 32},
                    {"name": "int_mask_rd", "width": 32},
                ],
            },
            {
                "name": "ipgt",
                "descr": "",
                "signals": [
                    {"name": "ipgt_wr", "width": 32},
                    {"name": "ipgt_rd", "width": 32},
                ],
            },
            {
                "name": "ipgr1",
                "descr": "",
                "signals": [
                    {"name": "ipgr1_wr", "width": 32},
                    {"name": "ipgr1_rd", "width": 32},
                ],
            },
            {
                "name": "ipgr2",
                "descr": "",
                "signals": [
                    {"name": "ipgr2_wr", "width": 32},
                    {"name": "ipgr2_rd", "width": 32},
                ],
            },
            {
                "name": "packetlen",
                "descr": "",
                "signals": [
                    {"name": "packetlen_wr", "width": 32},
                    {"name": "packetlen_rd", "width": 32},
                ],
            },
            {
                "name": "collconf",
                "descr": "",
                "signals": [
                    {"name": "collconf_wr", "width": 32},
                    {"name": "collconf_rd", "width": 32},
                ],
            },
            {
                "name": "tx_bd_num",
                "descr": "",
                "signals": [
                    {"name": "tx_bd_num_wr", "width": 32},
                    {"name": "tx_bd_num_rd", "width": 32},
                ],
            },
            {
                "name": "ctrlmoder",
                "descr": "",
                "signals": [
                    {"name": "ctrlmoder_wr", "width": 32},
                    {"name": "ctrlmoder_rd", "width": 32},
                ],
            },
            {
                "name": "miimoder",
                "descr": "",
                "signals": [
                    {"name": "miimoder_wr", "width": 32},
                    {"name": "miimoder_rd", "width": 32},
                ],
            },
            {
                "name": "miicommand",
                "descr": "",
                "signals": [
                    {"name": "miicommand_wr", "width": 32},
                    {"name": "miicommand_rd", "width": 32},
                ],
            },
            {
                "name": "miiaddress",
                "descr": "",
                "signals": [
                    {"name": "miiaddress_wr", "width": 32},
                    {"name": "miiaddress_rd", "width": 32},
                ],
            },
            {
                "name": "miitx_data",
                "descr": "",
                "signals": [
                    {"name": "miitx_data_wr", "width": 32},
                    {"name": "miitx_data_rd", "width": 32},
                ],
            },
            {
                "name": "miirx_data",
                "descr": "",
                "signals": [
                    {"name": "miirx_data_wr", "width": 32},
                    {"name": "miirx_data_rd", "width": 32},
                ],
            },
            {
                "name": "miistatus",
                "descr": "",
                "signals": [
                    {"name": "miistatus_wr", "width": 32},
                    {"name": "miistatus_rd", "width": 32},
                ],
            },
            {
                "name": "mac_addr0",
                "descr": "",
                "signals": [
                    {"name": "mac_addr0_wr", "width": 32},
                    {"name": "mac_addr0_rd", "width": 32},
                ],
            },
            {
                "name": "mac_addr1",
                "descr": "",
                "signals": [
                    {"name": "mac_addr1_wr", "width": 32},
                    {"name": "mac_addr1_rd", "width": 32},
                ],
            },
            {
                "name": "eth_hash0_adr",
                "descr": "",
                "signals": [
                    {"name": "eth_hash0_adr_wr", "width": 32},
                    {"name": "eth_hash0_adr_rd", "width": 32},
                ],
            },
            {
                "name": "eth_hash1_adr",
                "descr": "",
                "signals": [
                    {"name": "eth_hash1_adr_wr", "width": 32},
                    {"name": "eth_hash1_adr_rd", "width": 32},
                ],
            },
            {
                "name": "eth_txctrl",
                "descr": "",
                "signals": [
                    {"name": "eth_txctrl_wr", "width": 32},
                    {"name": "eth_txctrl_rd", "width": 32},
                ],
            },
            {
                "name": "tx_bd_cnt",
                "descr": "",
                "signals": [
                    {"name": "tx_bd_cnt_rdata_rd", "width": "BD_NUM_LOG2"},
                    {"name": "tx_bd_cnt_rvalid_rd", "width": 1},
                    {"name": "tx_bd_cnt_ren_rd", "width": 1},
                    {"name": "tx_bd_cnt_rready_rd", "width": 1},
                ],
            },
            {
                "name": "rx_bd_cnt",
                "descr": "",
                "signals": [
                    {"name": "rx_bd_cnt_rdata_rd", "width": "BD_NUM_LOG2"},
                    {"name": "rx_bd_cnt_rvalid_rd", "width": 1},
                    {"name": "rx_bd_cnt_ren_rd", "width": 1},
                    {"name": "rx_bd_cnt_rready_rd", "width": 1},
                ],
            },
            {
                "name": "tx_word_cnt",
                "descr": "",
                "signals": [
                    {"name": "tx_word_cnt_rdata_rd", "width": "BUFFER_W"},
                    {"name": "tx_word_cnt_rvalid_rd", "width": 1},
                    {"name": "tx_word_cnt_ren_rd", "width": 1},
                    {"name": "tx_word_cnt_rready_rd", "width": 1},
                ],
            },
            {
                "name": "rx_word_cnt",
                "descr": "",
                "signals": [
                    {"name": "rx_word_cnt_rdata_rd", "width": "BUFFER_W"},
                    {"name": "rx_word_cnt_rvalid_rd", "width": 1},
                    {"name": "rx_word_cnt_ren_rd", "width": 1},
                    {"name": "rx_word_cnt_rready_rd", "width": 1},
                ],
            },
            {
                "name": "rx_nbytes",
                "descr": "",
                "signals": [
                    {"name": "rx_nbytes_rdata_rd", "width": "BUFFER_W"},
                    {"name": "rx_nbytes_rvalid_rd", "width": 1},
                    {"name": "rx_nbytes_ren_rd", "width": 1},
                    {"name": "rx_nbytes_rready_rd", "width": 1},
                ],
            },
            {
                "name": "frame_word",
                "descr": "",
                "signals": [
                    {"name": "frame_word_wdata_wr", "width": 8},
                    {"name": "frame_word_wen_wr", "width": 1},
                    {"name": "frame_word_wready_wr", "width": 1},
                    {"name": "frame_word_rdata_rd", "width": 8},
                    {"name": "frame_word_rvalid_rd", "width": 1},
                    {"name": "frame_word_ren_rd", "width": 1},
                    {"name": "frame_word_rready_rd", "width": 1},
                ],
            },
            {
                "name": "phy_rst_val",
                "descr": "",
                "signals": [
                    {"name": "phy_rst_val_rd", "width": 1},
                ],
            },
            {
                "name": "bd",
                "descr": "",
                "signals": [
                    {"name": "bd_waddr_wr", "width": "BD_NUM_LOG2+1"},
                    {"name": "bd_wdata_wr", "width": 32},
                    {"name": "bd_wen_wr", "width": 1},
                    {"name": "bd_wready_wr", "width": 1},
                    {"name": "bd_raddr_rd", "width": "BD_NUM_LOG2+1"},
                    {"name": "bd_rdata_rd", "width": 32},
                    {"name": "bd_rvalid_rd", "width": 1},
                    {"name": "bd_ren_rd", "width": 1},
                    {"name": "bd_rready_rd", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "csrs_inst",
                "instance_description": "Control/Status Registers",
                "autoaddr": False,
                "rw_overlap": True,
                "csrs": [
                    {
                        "name": "iob_eth",
                        "descr": "IOb_Eth Software Accessible Registers",
                        "regs": [
                            {
                                "name": "moder",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 40960,
                                "addr": 0,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Mode Register",
                            },
                            {
                                "name": "int_source",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 4,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Interrupt Source Register",
                            },
                            {
                                "name": "int_mask",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 8,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Interrupt Mask Register",
                            },
                            {
                                "name": "ipgt",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 18,
                                "addr": 12,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Back to Back Inter Packet Gap Register",
                            },
                            {
                                "name": "ipgr1",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 12,
                                "addr": 16,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Non Back to Back Inter Packet Gap Register 1",
                            },
                            {
                                "name": "ipgr2",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 18,
                                "addr": 20,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Non Back to Back Inter Packet Gap Register 2",
                            },
                            {
                                "name": "packetlen",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 4195840,
                                "addr": 24,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Packet Length (minimum and maximum) Register",
                            },
                            {
                                "name": "collconf",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 61443,
                                "addr": 28,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Collision and Retry Configuration",
                            },
                            {
                                "name": "tx_bd_num",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 64,
                                "addr": 32,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Transmit Buffer Descriptor Number",
                            },
                            {
                                "name": "ctrlmoder",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 36,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Control Module Mode Register",
                            },
                            {
                                "name": "miimoder",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 100,
                                "addr": 40,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Mode Register",
                            },
                            {
                                "name": "miicommand",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 44,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Command Register",
                            },
                            {
                                "name": "miiaddress",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 48,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Address Register. Contains the PHY address and the register within the PHY address",
                            },
                            {
                                "name": "miitx_data",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 52,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Transmit Data. The data to be transmitted to the PHY",
                            },
                            {
                                "name": "miirx_data",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 56,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Receive Data. The data received from the PHY",
                            },
                            {
                                "name": "miistatus",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 60,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MII Status Register",
                            },
                            {
                                "name": "mac_addr0",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 64,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MAC Individual Address0. The LSB four bytes of the individual address are written to this register",
                            },
                            {
                                "name": "mac_addr1",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 68,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "MAC Individual Address1. The MSB two bytes of the individual address are written to this register",
                            },
                            {
                                "name": "eth_hash0_adr",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 72,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "HASH0 Register",
                            },
                            {
                                "name": "eth_hash1_adr",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 76,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "HASH1 Register",
                            },
                            {
                                "name": "eth_txctrl",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 80,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Transmit Control Register",
                            },
                        ],
                    },
                    {
                        "name": "no_dma",
                        "descr": "Data transfer/status registers for use without DMA",
                        "regs": [
                            {
                                "name": "tx_bd_cnt",
                                "type": "R",
                                "n_bits": "BD_NUM_LOG2",
                                "rst_val": 0,
                                "addr": 84,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Buffer descriptor number of current TX frame",
                            },
                            {
                                "name": "rx_bd_cnt",
                                "type": "R",
                                "n_bits": "BD_NUM_LOG2",
                                "rst_val": 0,
                                "addr": 88,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Buffer descriptor number of current RX frame",
                            },
                            {
                                "name": "tx_word_cnt",
                                "type": "R",
                                "n_bits": "BUFFER_W",
                                "rst_val": 0,
                                "addr": 92,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Word number of current TX frame",
                            },
                            {
                                "name": "rx_word_cnt",
                                "type": "R",
                                "n_bits": "BUFFER_W",
                                "rst_val": 0,
                                "addr": 96,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Word number of current RX frame",
                            },
                            {
                                "name": "rx_nbytes",
                                "type": "R",
                                "n_bits": "BUFFER_W",
                                "rst_val": 0,
                                "addr": 100,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Size of received frame in bytes. Will be zero if no frame has been received. Will reset to zero when cpu completes reading the frame.",
                            },
                            {
                                "name": "frame_word",
                                "type": "RW",
                                "n_bits": 8,
                                "rst_val": 0,
                                "addr": 104,
                                "log2n_items": 0,
                                "autoreg": False,
                                "descr": "Frame word to transfer to/from buffer",
                            },
                        ],
                    },
                    {
                        "name": "phy_rst",
                        "descr": "PHY reset control registers",
                        "regs": [
                            {
                                "name": "phy_rst_val",
                                "type": "R",
                                "n_bits": 1,
                                "rst_val": 0,
                                "addr": 108,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Current PHY reset signal value",
                            },
                        ],
                    },
                    {
                        "name": "iob_eth_bd",
                        "descr": "IOb_Eth Buffer Descriptors",
                        "regs": [
                            {
                                "name": "bd",
                                "type": "RW",
                                "n_bits": 32,
                                "rst_val": 0,
                                "addr": 1024,
                                "log2n_items": "BD_NUM_LOG2+1",
                                "autoreg": False,
                                "descr": "Buffer descriptors",
                            },
                        ],
                    },
                ],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "control_if_s": "cbus_s",
                    # Register interfaces
                    "moder_io": "moder",
                    "int_source_io": "int_source",
                    "int_mask_io": "int_mask",
                    "ipgt_io": "ipgt",
                    "ipgr1_io": "ipgr1",
                    "ipgr2_io": "ipgr2",
                    "packetlen_io": "packetlen",
                    "collconf_io": "collconf",
                    "tx_bd_num_io": "tx_bd_num",
                    "ctrlmoder_io": "ctrlmoder",
                    "miimoder_io": "miimoder",
                    "miicommand_io": "miicommand",
                    "miiaddress_io": "miiaddress",
                    "miitx_data_io": "miitx_data",
                    "miirx_data_io": "miirx_data",
                    "miistatus_io": "miistatus",
                    "mac_addr0_io": "mac_addr0",
                    "mac_addr1_io": "mac_addr1",
                    "eth_hash0_adr_io": "eth_hash0_adr",
                    "eth_hash1_adr_io": "eth_hash1_adr",
                    "eth_txctrl_io": "eth_txctrl",
                    "tx_bd_cnt_io": "tx_bd_cnt",
                    "rx_bd_cnt_io": "rx_bd_cnt",
                    "tx_word_cnt_io": "tx_word_cnt",
                    "rx_word_cnt_io": "rx_word_cnt",
                    "rx_nbytes_io": "rx_nbytes",
                    "frame_word_io": "frame_word",
                    "phy_rst_val_i": "phy_rst_val",
                    "bd_io": "bd",
                },
            },
            {
                "core_name": "iob_reg",
                "instantiate": False,
            },
            {
                "core_name": "iob_acc",
                "instantiate": False,
            },
            {
                "core_name": "iob_sync",
                "instantiate": False,
            },
            {
                "core_name": "iob_ram_at2p",
                "instantiate": False,
            },
            {
                "core_name": "iob_ram_tdp",
                "instantiate": False,
            },
            {
                "core_name": "iob_arbiter",
                "instantiate": False,
            },
            {
                "core_name": "iob_tasks",
                "instantiate": False,
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
