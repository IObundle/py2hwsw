#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This script generates interfaces for Verilog modules and testbenches to add a
# new standard interface, add the name to the interface_names list, and an
# interface dictionary as below. Run this script with the -h option for help
from copy import deepcopy
from dataclasses import dataclass, field
from encodings.punycode import T
from pydoc import describe
import re
from sys import prefix
from turtle import reset
from typing import Dict
from unittest import result, signals

from numpy import add, size
from iob_signal import iob_signal, iob_signal_reference
from iob_globals import iob_globals

mem_if_details = [
    {
        "name": "rom_2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "ROM 2 Port",
    },
    {
        "name": "rom_atdp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "ROM Asynchronous True Dual Port",
    },
    {
        "name": "rom_sp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "ROM Single Port",
    },
    {
        "name": "rom_tdp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "ROM True Dual Port",
    },
    {
        "name": "ram_2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM 2 Port",
    },
    {
        "name": "ram_at2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Asynchronous True 2 Port",
    },
    {
        "name": "ram_atdp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Asynchronous True Dual Port",
    },
    {
        "name": "ram_atdp_be",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Asynchronous True Dual Port with Byte Enable",
    },
    {
        "name": "ram_sp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Single Port",
    },
    {
        "name": "ram_sp_be",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Single Port with Byte Enable",
    },
    {
        "name": "ram_sp_se",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM Single Port with Single Enable",
    },
    {
        "name": "ram_t2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True 2 Port",
    },
    {
        "name": "ram_t2p_be",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True 2 Port with Byte Enable",
    },
    {
        "name": "ram_t2p_tiled",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True 2 Port Tiled",
    },
    {
        "name": "ram_tdp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True Dual Port",
    },
    {
        "name": "ram_tdp_be",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True Dual Port with Byte Enable",
    },
    {
        "name": "ram_tdp_be_xil",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "RAM True Dual Port with Byte Enable Xilinx",
    },
    {
        "name": "regfile_2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "Register File 2 Port",
    },
    {
        "name": "regfile_at2p",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "Register File Asynchronous True 2 Port",
    },
    {
        "name": "regfile_sp",
        "vendor": "IObundle",
        "lib": "MEM",
        "version": "1.0",
        "full_name": "Register File Single Port",
    },
]

mem_if_names = [item["name"] for item in mem_if_details]

if_details = [
    {
        "name": "iob_clk",
        "vendor": "IObundle",
        "lib": "CLK",
        "version": "1.0",
        "full_name": "Clock (configurable)",
    },
    {
        "name": "iob",
        "vendor": "IObundle",
        "lib": "IOb",
        "version": "1.0",
        "full_name": "IOb",
    },
    {
        "name": "axil_read",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI-Lite Read",
    },
    {
        "name": "axil_write",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI-Lite Write",
    },
    {
        "name": "axil",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI-Lite",
    },
    {
        "name": "axi_read",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI Read",
    },
    {
        "name": "axi_write",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI Write",
    },
    {
        "name": "axi",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI",
    },
    {
        "name": "apb",
        "vendor": "ARM",
        "lib": "APB",
        "version": "4.0",
        "full_name": "APB",
    },
    {
        "name": "ahb",
        "vendor": "ARM",
        "lib": "AHB",
        "version": "4.0",
        "full_name": "AHB",
    },
    {
        "name": "axis",
        "vendor": "ARM",
        "lib": "AXI",
        "version": "4.0",
        "full_name": "AXI Stream",
    },
    {
        "name": "rs232",
        "vendor": "Generic",
        "lib": "RS232",
        "version": "1.0",
        "full_name": "RS232",
    },
    {
        "name": "wb",
        "vendor": "OPENCORES",
        "lib": "Wishbone",
        "version": "B4",
        "full_name": "Wishbone",
    },
    {
        "name": "wb_full",
        "vendor": "OPENCORES",
        "lib": "Wishbone",
        "version": "B4",
        "full_name": "Wishbone Full",
    },
] + mem_if_details

if_names = [item["name"] for item in if_details]

if_types = [
    "m_port",
    "s_port",
    "m_portmap",
    "s_portmap",
    "m_m_portmap",
    "s_s_portmap",
    "wire",
    "m_tb_wire",
    "s_tb_wire",
]



@dataclass
class _Interface:
    """Class to represent an interface for generation"""

    # Prefix for signals of the interface
    prefix: str = ""
    # Width multiplier. Used when concatenating multiple instances of the interface.
    mult: str | int = 1
    # Prefix for generated "Verilog Snippets" of this interface
    file_prefix: str = ""
    # Prefix for "Verilog snippets" of portmaps of this interface:
    portmap_port_prefix: str = ""
    # List of signals for this interface (Internal, used for generation)
    _signals: list = []


    def __post_init__(self):
        if not self.file_prefix:
            self.file_prefix = self.portmap_port_prefix + self.prefix


    def get_signals(self):
        return self._signals


#
# IOb
#

@dataclass
class IobClkInterface(_Interface):
    """Class to represent an IOb clock interface for generation"""
    has_cke: bool = True
    has_arst: bool = True
    has_rst: bool = False
    has_en: bool = False


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the IOb clock interface."""

        arst_polarity = getattr(iob_globals(), "reset_polarity", "positive")

        self._signals.append(iob_signal(name="clk_o", descr="Clock"))

        if self.has_cke:
            self._signals.append(iob_signal(name="cke_o", descr="Clock enable"))
        if self.has_arst:
            if arst_polarity == "positive":
                self._signals.append(iob_signal(name="arst_o", descr="Asynchronous active-high reset"))
            else:
                self._signals.append(iob_signal(name="arst_n_o", descr="Asynchronous active-low reset"))
        if self.has_rst:
            self._signals.append(iob_signal(name="rst_o", descr="Synchronous active-high reset"))
        if self.has_en:
            self._signals.append(iob_signal(name="en_o", descr="Enable"))


@dataclass
class IobInterface(_Interface):
    """Class to represent an IOb interface for generation"""

    # Widths for the IOb interface
    data_w: int = 32
    # Only address width is configurable, data width is fixed
    addr_w: str or int = 32


    def __post_init__(self):
        super.post__init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the IOb interface."""
        wstrb_w = self.data_w // 8

        self._signals = self._signals + [
            iob_signal(name="iob_valid_o", descr="Request address is valid."),
            iob_signal(name="iob_addr_o", width=self.addr_w, descr="Byte address."),
            iob_signal(name="iob_wdata_o", width=self.data_w, descr="Write data."),
            iob_signal(name="iob_wstrb_o", width=wstrb_w, descr="Write strobe."),
            iob_signal(name="iob_rvalid_i", descr="Read data valid."),
            iob_signal(name="iob_rdata_i", width=self.data_w, descr="Read data."),
            iob_signal(name="iob_ready_i", descr="Interface ready."),
        ]


#
# Memory interfaces
#

# Memory symbols meaning:
# SP: Single-Port read-write
# 2P: 2-Port (one read, one write)
# DP: Dual-Port (two read-write)
# TDP/T2P: True (Dual-/2-)Port; Can perform transactions in both ports at the same time
# ATDP/AT2P: Asynchronous ports
# BE: byte-enable for each byte of data word
# SE: Single enable for entire data word
# Xil: Xilinx IP implementation

@dataclass
class _MemInterface(_Interface):
    """Class to represent a memory interface for generation"""

    # Width for the memory interface
    addr_w: int or str = 32
    # Asynchronous memory interface
    _is_async: bool = False
    # Memory type
    type: str = "ram_sp"


    def _set_mem_signals(
        self, suffix: str, has_addr: bool = True, has_enable: bool = True
    ):
        """Get common signals for the memory interface."""

        clk_prefix = f"{suffix}_" if self._is_async else ""
        suffix = f"_{suffix}" if suffix else ""

        self._signals.append(
            iob_signal(name=clk_prefix + "clk" + "_o", descr=f"Clock port {suffix}")
        )
        if has_addr:
            self._signals.append(
                iob_signal(
                    name="addr" + suffix + "_o",
                    width=self.addr_w,
                    descr=f"Address port {suffix}",
                )
            )
        if has_enable:
            self._signals.append(
                iob_signal(name="en" + suffix + "_o", descr=f"Enable port {suffix}")
            )


    def _remove_duplicate_signals(self):
        """Remove duplicate signals from the interface."""
        result = []
        for signal in self._signals:
            if signal not in result:
                result.append(signal)
        
        self._signals = result


@dataclass
class SymMemInterface(_MemInterface):
    """Class to represent a symmetric memory interface for generation"""

    # Data width for the memory interface
    data_w: int = 32


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the symmetric memory interface based on the memory type."""

        # Replace the long if-elif-else chain with a match-case statement (Python 3.10+)
        match self.type:
            case "rom_2p":
                self._set_mem_signals("", has_addr=False, has_enable=False)
                self.__set_mem_read_signals("a", has_enable=True, has_ready=True, has_addr=True)
                self.__set_mem_read_signals("b", has_enable=True, has_ready=True, has_addr=True)
            case "rom_sp":
                self._set_mem_signals("")
                self.__set_mem_read_signals("")
            case "rom_tdp":
                self._set_mem_signals("", has_enable=False, has_addr=False)
                self.__set_mem_read_signals("a", has_enable=True, has_addr=True, is_true_port=True)
                self.__set_mem_read_signals("b", hasEnable=True, has_addr=True, is_true_port=True)
            case "rom_atdp":
                self._is_async = True
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a", is_true_port=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b", is_true_port=True)
            case "ram_2p":
                self._set_mem_signals("", has_addr=False, has_enable=False)
                self.__set_mem_read_signals("", hasEnable=True, has_ready=True, has_addr=True)
                self.__set_mem_write_signals("", has_ready=True, has_addr=True)
            case "ram_at2p":
                self._is_async = True
                self._set_mem_signals("r", hasAddr=False, hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True, hasAddr=True)
                self._set_mem_signals("w", hasAddr=False, hasEnable=False)
                self.__set_mem_write_signals("", hasAddr=True)
            case "ram_atdp":
                self._is_async = True
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a", is_true_port=True)
                self.__set_mem_write_signals("a", is_true_port=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b", is_true_port=True)
                self.__set_mem_write_signals("b", is_true_port=True)
            case "ram_atdp_be":
                self._is_async = True
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a", is_true_port=True)
                self.__set_mem_write_signals("a", is_true_port=True, byte_enable=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b", is_true_port=True)
                self.__set_mem_write_signals("b", is_true_port=True, byte_enable=True)
            case "ram_sp" | "ram_sp_se":
                self._set_mem_signals("")
                self.__set_mem_read_signals("")
                self.__set_mem_write_signals("")
            case "ram_sp_be":
                self._set_mem_signals("")
                self.__set_mem_read_signals("")
                self.__set_mem_write_signals("", byte_enable=True)
            case "ram_t2p":
                self._set_mem_signals("", hasAddr=False, hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True, hasAddr=True)
                self.__set_mem_write_signals("", hasAddr=True)
            case "ram_t2p_be":
                self._set_mem_signals("", hasAddr=False, hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True, hasAddr=True)
                self.__set_mem_write_signals("", hasAddr=True, byte_enable=True)
            case "ram_t2p_tiled":
                self._set_mem_signals("", hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True)
                self.__set_mem_write_signals("")
            case "ram_tdp":
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a")
                self.__set_mem_write_signals("a")
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b")
                self.__set_mem_write_signals("b")
            case "ram_tdp_be" | "ram_tdp_be_xil":
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a")
                self.__set_mem_write_signals("a", byte_enable=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b")
                self.__set_mem_write_signals("b", byte_enable=True)
            case _:
                raise ValueError(f"Unknown memory interface type: {self.type}")

        self._signals = self._remove_duplicate_signals(self._signals)


    def __set_mem_read_signals(
        self,
        suffix: str = "",
        has_enable: bool = False,
        has_ready: bool = False,
        has_addr: bool = False,
        is_true_port: bool = False,
    ):
        """Get read ports for the memory interface."""

        suffix = f"_{suffix}" if suffix else ""
        rd_suffix = suffix if is_true_port else ""

        if has_enable:
            self._signals.append(
                iob_signal(
                    name="r_en" + suffix + "_o", descr=f"Read enable port {suffix}"
                )
            )
        if has_addr:
            self._signals.append(
                iob_signal(
                    name="r_addr" + suffix + "_o",
                    width=self.addr_w,
                    descr=f"Read address port {suffix}",
                )
            )
        self._signals.append(
            iob_signal(
                name="r_data" + rd_suffix + "_i",
                width=self.data_w,
                descr=f"Data port {suffix}",
            )
        )
        if has_ready:
            self._signals.append(
                iob_signal(
                    name="r_ready" + suffix + "_i", descr=f"Read ready port {suffix}"
                )
            )


    def __set_mem_write_signals(
        self,
        suffix: str = "",
        has_ready: bool = False,
        has_addr: bool = False,
        is_true_port: bool = False,
        has_byte_enable: bool = False,
    ):
        """Set write signals for the memory interface."""

        suffix = f"_{suffix}" if suffix else ""
        wr_suffix = suffix if is_true_port else ""

        if has_byte_enable:
            wstrb_w = self.data_w // 8
            self._signals.append(
                iob_signal(
                    name="w_strb" + suffix + "_o",
                    width=wstrb_w,
                    descr=f"Write strobe port {suffix}",
                )
            )
        else:  # No byte enable
            self._signals.append(
                iob_signal(
                    name="w_en" + suffix + "_o", descr=f"Write enable port {suffix}"
                )
            )
        if has_addr:
            self._signals.append(
                iob_signal(
                    name="w_addr" + suffix + "_o",
                    width=self.addr_w,
                    descr=f"Write address port {suffix}",
                )
            )
        self._signals.append(
            iob_signal(
                name="w_data" + wr_suffix + "_o",
                width=self.data_w,
                descr=f"Data port {suffix}",
            )
        )
        if has_ready:
            self._signals.append(
                iob_signal(
                    name="w_ready" + suffix + "_i", descr=f"Write ready port {suffix}"
                )
            )


@dataclass
class AsymMemInterface(_MemInterface):
    """Class to represent an asymmetric memory interface for generation"""

    # Data widths for the memory interface
    w_data_w: int = 32
    r_data_w: int = 32

    __block_data_w: int = field(init=False, default=32)
    __block_addr_w: int = field(init=False, default=32)
    __data_ratio: int = field(init=False)


    def __post_init__(self):
        super().__post_init__()
        
        max_data_w = max(self.w_data_w, self.r_data_w)
        min_data_w = min(self.w_data_w, self.r_data_w)

        ratio = max_data_w // min_data_w

        # Check if data widths are a multiple of each other and the ratio is a power of two
        if max_data_w % min_data_w != 0 or ratio & (ratio - 1) != 0:
            raise ValueError("Data widths must be a multiple of each other and the ratio must be a power of two.")

        if ratio <= 1:
            raise ValueError("Data widths must be different.")

        self.__data_ratio = ratio
        self.__block_data_w = max_data_w
        # Calculate address width based on the ratio (same as min_addr_w)
        self.__block_addr_w = self.addr_w - (ratio.bit_length() - 1)

        self.__set_signals()


    def __set_signals(self):
        """Set signals for the asymmetric memory interface based on the memory type."""

        match self.type:
            case "rom_2p":
                self._set_mem_signals("", has_addr=False, has_enable=False)
                self.__set_mem_read_signals("a", has_enable=True, has_ready=True, has_addr=True)
                self.__set_mem_read_signals("b", has_enable=True, has_ready=True, has_addr=True)
            case "rom_tdp":
                self._set_mem_signals("", has_enable=False, has_addr=False)
                self.__set_mem_read_signals("a", has_enable=True, has_addr=True, is_true_port=True)
                self.__set_mem_read_signals("b", hasEnable=True, has_addr=True, is_true_port=True)
            case "rom_atdp":
                self._is_async = True
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a", is_true_port=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b", is_true_port=True)
            case "ram_2p":
                self._set_mem_signals("", has_addr=False, has_enable=False)
                self.__set_mem_read_signals("", hasEnable=True, has_ready=True, has_addr=True)
                self.__set_mem_write_signals("", has_ready=True, has_addr=True)
            case "ram_at2p":
                self._is_async = True
                self._set_mem_signals("r", hasAddr=False, hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True, hasAddr=True)
                self._set_mem_signals("w", hasAddr=False, hasEnable=False)
                self.__set_mem_write_signals("", hasAddr=True)
            case "ram_atdp":
                self._is_async = True
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a", is_true_port=True)
                self.__set_mem_write_signals("a", is_true_port=True)
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b", is_true_port=True)
                self.__set_mem_write_signals("b", is_true_port=True)
            case "ram_t2p":
                self._set_mem_signals("", hasAddr=False, hasEnable=False)
                self.__set_mem_read_signals("", hasEnable=True, hasAddr=True)
                self.__set_mem_write_signals("", hasAddr=True)
            case "ram_tdp":
                self._set_mem_signals("a")
                self.__set_mem_read_signals("a")
                self.__set_mem_write_signals("a")
                self._set_mem_signals("b")
                self.__set_mem_read_signals("b")
                self.__set_mem_write_signals("b")
            case _:
                raise ValueError(f"Unknown memory interface type: {self.type}")

        self._signals = self._remove_duplicate_signals(self._signals)


    def __set_mem_read_signals(
        self,
        suffix: str = "",
        has_enable: bool = False,
        has_ready: bool = False,
        has_addr: bool = False,
        is_true_port: bool = False,
    ):
        """Get read ports for the memory interface."""

        suffix = f"_{suffix}" if suffix else ""
        rd_suffix = suffix if is_true_port else ""

        if has_enable:
            self._signals.append(
                iob_signal(
                    name="r_en" + suffix + "_o",
                    width=self.__data_ratio,
                    descr=f"Read enable port {suffix}"
                )
            )
        if has_addr:
            self._signals.append(
                iob_signal(
                    name="r_addr" + suffix + "_o",
                    width=self.__block_addr_w,
                    descr=f"Read address port {suffix}",
                )
            )
        self._signals.append(
            iob_signal(
                name="r_data" + rd_suffix + "_i",
                width=self.__block_data_w,
                descr=f"Data port {suffix}",
            )
        )
        if has_ready:
            self._signals.append(
                iob_signal(
                    name="r_ready" + suffix + "_i", descr=f"Read ready port {suffix}"
                )
            )


    def __set_mem_write_signals(
        self,
        suffix: str = "",
        has_ready: bool = False,
        has_addr: bool = False,
        is_true_port: bool = False,
    ):
        """Set write signals for the memory interface."""

        suffix = f"_{suffix}" if suffix else ""
        wr_suffix = suffix if is_true_port else ""

        self._signals.append(
            iob_signal(
                name="w_en" + suffix + "_o",
                width=self.__data_ratio, 
                descr=f"Write enable port {suffix}"
            )
        )
        if has_addr:
            self._signals.append(
                iob_signal(
                    name="w_addr" + suffix + "_o",
                    width=self.__block_addr_w,
                    descr=f"Write address port {suffix}",
                )
            )
        self._signals.append(
            iob_signal(
                name="w_data" + wr_suffix + "_o",
                width=self.__block_data_w,
                descr=f"Data port {suffix}",
            )
        )
        if has_ready:
            self._signals.append(
                iob_signal(
                    name="w_ready" + suffix + "_i", descr=f"Write ready port {suffix}"
                )
            )

#
# AXI interfaces
#

@dataclass
class AXIStreamInterface(_Interface):
    """Class to represent an AXI-Stream interface for generation"""

    # Data width for the AXI-Stream interface
    data_w: int = 32
    # Signal to indicate if the interface has a last signal
    has_tlast: bool = False


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the AXI-Stream interface."""
        self._signals += [
            iob_signal(
                name="axis_tdata_o",
                width=self.data_w,
                descr="AXI-Stream data output.",
            ),
            iob_signal(
                name="axis_tvalid_o",
                descr="AXI-Stream valid output.",
            ),
            iob_signal(
                name="axis_tready_i",
                descr="AXI-Stream ready input.",
            ),
        ]

        if self.has_tlast:
            self._signals.append(
                iob_signal(
                    name="axis_tlast_o",
                    descr="AXI-Stream last signal output.",
                )
            )


@dataclass
class AXILiteInterface(_Interface):
    """Class to represent an AXI-Lite interface for generation"""

    # Data width for the AXI-Lite interface
    data_w: int = 32
    # Address width for the AXI-Lite interface
    addr_w: int = 32
    # AXI-Lite parameters
    resp_w: int = 2
    prot_w: int = 3
    # Interfaces/Ports to include in the AXI-Lite interface
    has_read_if: bool = True
    has_write_if: bool = True
    has_prot: bool = True


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the AXI-Lite interface."""

        if self.has_read_if:
            self.__set_write_signals()
        if self.has_write_if:
            self.__set_read_signals()


    def __set_write_signals(self):
        """Set write signals for the AXI-Lite interface."""
        self._signals += [
            iob_signal(
                name="axil_awaddr_o",
                width=self.addr_w,
                descr="AXI-Lite address write channel byte address.",
            ),
        ]
        if self.has_prot:
            self._signals.append(
                iob_signal(
                    name="axil_awprot_o",
                    width=self.prot_w,
                    descr="AXI-Lite address write channel protection type.",
                )
            )
        self._signals += [
            iob_signal(
                name="axil_awvalid_o",
                descr="AXI-Lite address write channel valid.",
            ),
            iob_signal(
                name="axil_awready_i",
                descr="AXI-Lite address write channel ready.",
            ),
            iob_signal(
                name="axil_wdata_o",
                width=self.data_w,
                descr="AXI-Lite write channel data.",
            ),
            iob_signal(
                name="axil_wstrb_o",
                width=self.data_w // 8,
                descr="AXI-Lite write channel write strobe.",
            ),
            iob_signal(
                name="axil_wvalid_o",
                descr="AXI-Lite write channel valid.",
            ),
            iob_signal(
                name="axil_wready_i",
                descr="AXI-Lite write channel ready.",
            ),
            iob_signal(
                name="axil_bresp_i",
                width=self.resp_w,
                descr="AXI-Lite write response channel response.",
            ),
            iob_signal(
                name="axil_bvalid_i",
                descr="AXI-Lite write response channel valid.",
            ),
            iob_signal(
                name="axil_bready_o",
                descr="AXI-Lite write response channel ready.",
            ),
        ]


    def __set_read_signals(self):
        """Set read signals for the AXI-Lite interface."""
        self._signals += [
            iob_signal(
                name="axil_araddr_o",
                width=self.addr_w,
                descr="AXI-Lite address read channel byte address.",
            ),
        ]
        if self.has_prot:
            self._signals.append(
                iob_signal(
                    name="axil_arprot_o",
                    width=self.prot_w,
                    descr="AXI-Lite address read channel protection type.",
                )
            )
        self._signals += [
            iob_signal(
                name="axil_arvalid_o",
                descr="AXI-Lite address read channel valid.",
            ),
            iob_signal(
                name="axil_arready_i",
                descr="AXI-Lite address read channel ready.",
            ),
            iob_signal(
                name="axil_rdata_i",
                width=self.data_w,
                descr="AXI-Lite read channel data.",
            ),
            iob_signal(
                name="axil_rresp_i",
                width=self.resp_w,
                descr="AXI-Lite read channel response.",
            ),
            iob_signal(
                name="axil_rvalid_i",
                descr="AXI-Lite read channel valid.",
            ),
            iob_signal(
                name="axil_rready_o",
                descr="AXI-Lite read channel ready.",
            ),
        ]


@dataclass
class AXIInterface(_Interface):
    """Class to represent an AXI interface for generation"""

    # Data width for the AXI interface
    data_w: int = 32
    # Address width for the AXI interface
    addr_w: int = 32
    # AXI parameters
    id_w: int = 1
    size_w: int = 3
    burst_w: int = 2
    lock_w: int = 2
    cache_w: int = 4
    prot_w: int = 3
    qos_w: int = 4
    resp_w: int = 2
    len_w: int = 8
    # Interfaces/Ports to include in the AXI-Lite interface
    has_read_if: bool = True
    has_write_if: bool = True
    has_prot: bool = True

    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()

    def __set_signals(self):
        """Set signals for the AXI interface."""

        if self.has_read_if:
            self.__set_write_signals()
        if self.has_write_if:
            self.__set_read_signals()

    def __set_write_signals(self):
        """Set write signals for the AXI interface."""

        # AXI-Lite write signals
        self._signals += [
            iob_signal(
                name="axi_awaddr_o",
                width=self.addr_w,
                descr="AXI address write channel byte address.",
            ),
        ]
        if self.has_prot:
            self._signals.append(
                iob_signal(
                    name="axi_awprot_o",
                    width=self.prot_w,
                    descr="AXI address write channel protection type.",
                )
            )
        self._signals += [
            iob_signal(
                name="axi_awvalid_o",
                descr="AXI address write channel valid.",
            ),
            iob_signal(
                name="axil_awready_i",
                descr="AXI address write channel ready.",
            ),
            iob_signal(
                name="axi_wdata_o",
                width=self.data_w,
                descr="AXI write channel data.",
            ),
            iob_signal(
                name="axi_wstrb_o",
                width=self.data_w // 8,
                descr="AXI write channel write strobe.",
            ),
            iob_signal(
                name="axi_wvalid_o",
                descr="AXI write channel valid.",
            ),
            iob_signal(
                name="axi_wready_i",
                descr="AXI write channel ready.",
            ),
            iob_signal(
                name="axi_bresp_i",
                width=self.resp_w,
                descr="AXI write response channel response.",
            ),
            iob_signal(
                name="axi_bvalid_i",
                descr="AXI write response channel valid.",
            ),
            iob_signal(
                name="axi_bready_o",
                descr="AXI write response channel ready.",
            ),
        ]

        # AXI write channel signals
        self._signals += [
            iob_signal(
                name="axi_awid_o",
                width=self.id_w,
                descr="AXI address write channel ID.",
            ),
            iob_signal(
                name="axi_awlen_o",
                width=self.len_w,
                descr="AXI address write channel burst length.",
            ),
            iob_signal(
                name="axi_awsize_o",
                width=self.size_w,
                descr="AXI address write channel burst size.",
            ),
            iob_signal(
                name="axi_awburst_o",
                width=self.burst_w,
                descr="AXI address write channel burst type.",
            ),
            iob_signal(
                name="axi_awlock_o",
                width=self.lock_w,
                descr="AXI address write channel lock type.",
            ),
            iob_signal(
                name="axi_awcache_o",
                width=self.cache_w,
                descr="AXI address write channel memory type.",
            ),
            iob_signal(
                name="axi_awqos_o",
                width=self.qos_w,
                descr="AXI address write channel quality of service.",
            ),
            iob_signal(
                name="axi_wlast_o",
                descr="AXI Write channel last word flag.",
            ),
            iob_signal(
                name="axi_bid_i",
                width=self.id_w,
                descr="AXI Write response channel ID.",
            ),
        ]

    def __set_read_signals(self):
        """Set read signals for the AXI interface."""

        # AXI-Lite read signals
        self._signals += [
            iob_signal(
                name="axi_araddr_o",
                width=self.addr_w,
                descr="AXI address read channel byte address.",
            ),
        ]
        if self.has_prot:
            self._signals.append(
                iob_signal(
                    name="axi_arprot_o",
                    width=self.prot_w,
                    descr="AXI address read channel protection type.",
                )
            )
        self._signals += [
            iob_signal(
                name="axi_arvalid_o",
                descr="AXI address read channel valid.",
            ),
            iob_signal(
                name="axi_arready_i",
                descr="AXI address read channel ready.",
            ),
            iob_signal(
                name="axi_rdata_i",
                width=self.data_w,
                descr="AXI read channel data.",
            ),
            iob_signal(
                name="axi_rresp_i",
                width=self.resp_w,
                descr="AXI read channel response.",
            ),
            iob_signal(
                name="axi_rvalid_i",
                descr="AXI read channel valid.",
            ),
            iob_signal(
                name="axi_rready_o",
                descr="AXI read channel ready.",
            ),
        ]

        # AXI read channel signals
        self._signals += [
            iob_signal(
                name="axi_arid_o",
                width=self.id_w,
                descr="AXI address read channel ID.",
            ),
            iob_signal(
                name="axi_arlen_o",
                width=self.len_w,
                descr="AXI address read channel burst length.",
            ),
            iob_signal(
                name="axi_arsize_o",
                width=self.size_w,
                descr="AXI address read channel burst size.",
            ),
            iob_signal(
                name="axi_arburst_o",
                width=self.burst_w,
                descr="AXI address read channel burst type.",
            ),
            iob_signal(
                name="axi_arlock_o",
                width=self.lock_w,
                descr="AXI address read channel lock type.",
            ),
            iob_signal(
                name="axi_arcache_o",
                width=self.cache_w,
                descr="AXI address read channel memory type.",
            ),
            iob_signal(
                name="axi_arqos_o",
                width=self.qos_w,
                descr="AXI address read channel quality of service.",
            ),
            iob_signal(
                name="axi_rid_i",
                width=self.id_w,
                descr="AXI Read channel ID.",
            ),
            iob_signal(
                name="axi_rlast_i",
                descr="AXI Read channel last word.",
            ),
        ]

#
# APB interfaces
#

@dataclass
class APBInterface(_Interface):
    """Class to represent an APB interface for generation"""

    # Data width for the APB interface
    data_w: int = 32
    # Address width for the APB interface
    addr_w: int = 32


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()


    def __set_signals(self):
        """Set signals for the APB interface."""
        self._signals += [
            iob_signal(
                name="apb_addr_o",
                width=self.addr_w,
                descr="APB address output.",
            ),
            iob_signal(
                name="apb_sel_o",
                descr="APB subordinate select.",
            ),
            iob_signal(
                name="apb_enable_o",
                descr="APB enable. Indicates the number of clock cycles of the transfer.",
            ),
            iob_signal(
                name="apb_write_o",
                descr="APB write. Indicates the direction of the operation.",
            ),
            iob_signal(
                name="apb_wdata_o",
                width=self.data_w,
                descr="APB write data.",
            ),
            iob_signal(
                name="apb_wstrb_o",
                width=self.data_w // 8,
                descr="APB write strobe.",
            ),
            iob_signal(
                name="apb_rdata_i",
                width=self.data_w,
                descr="APB read data.",
            ),
            iob_signal(
                name="apb_ready_i",
                descr="APB ready. Indicates the end of a transfer.",
            ),
        ]

@dataclass
class AHBInterface(_Interface):
    """Class to represent an AHB interface for generation"""

    # Data width for the AHB interface
    data_w: int = 32
    # Address width for the AHB interface
    addr_w: int = 32
    # AHB parameters
    prot_w: int = 4
    burst_w: int = 3
    trans_w: int = 2
    size_w: int = 3

    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()

    def __set_signals(self):
        """Set signals for the AHB interface."""
        self._signals += [
            iob_signal(
                name="ahb_addr_o",
                width=self.addr_w,
                descr="AHB address output.",
            ),
            iob_signal(
                name="ahb_burst_o",
                width=self.burst_w,
                descr="AHB burst size.",
            ),
            iob_signal(
                name="ahb_mastlock_o",
                descr="AHB master lock signal.",
            ),
            iob_signal(
                name="ahb_prot_o",
                width=self.prot_w,
                descr="AHB protection type.",
            ),
            iob_signal(
                name="ahb_size_o",
                width=self.size_w,  # Size is typically 3 bits in AHB
                descr="AHB transfer size.",
            ),
            iob_signal(
                name="ahb_trans_o",
                width=self.trans_w,
                descr="AHB transfer type.",
            ),
            iob_signal(
                name="ahb_wdata_o",
                width=self.data_w,
                descr="AHB write data.",
            ),
            iob_signal(
                name="ahb_wstrb_o",
                width=self.data_w // 8,
                descr="AHB write strobe.",
            ),
            iob_signal(
                name="ahb_write_o",
                descr="AHB write signal. Transfer direction: (1) Write; (0) Read.",
            ),
            iob_signal(
                name="ahb_rdata_i",
                width=self.data_w,
                descr="AHB read data.",
            ),
            iob_signal(
                name="ahb_readyout_i",
                descr="AHB ready output. Indicates transfer finished on the bus.",
            ),
            iob_signal(
                name="ahb_resp_i",
                descr="AHB response input. Transfer response: (0) Okay; (1) Error.",
            ),
            iob_signal(
                name="ahb_sel_o",
                descr="AHB subordinate select.",
            ),
        ]

#
# RS232
#

@dataclass
class RS232Interface(_Interface):
    """Class to represent an RS232 interface for generation"""

    # Number of pins for the RS232 interface
    n_pins: int = 4


    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()

    def __set_signals(self):
        """Set signals for the RS232 interface."""
        if self.n_pins not in [2, 4, 9]:
            raise ValueError("RS232 interface must have 2, 4, or 9 pins.")

        if self.n_pins == 9:
            self._signals += [
                iob_signal(
                    name="rs232_dcd_i",
                    width=1,
                    descr="Data carrier detect.",
                ),
            ]
        if self.n_pins in [2, 4]:
            self._signals += [
                iob_signal(
                    name="rs232_rxd_i",
                    width=1,
                    descr="Receive data.",
                ),
                iob_signal(
                    name="rs232_txd_o",
                    width=1,
                    descr="Transmit data.",
                ),
            ]
        if self.n_pins == 9:
            self._signals += [
                iob_signal(
                    name="rs232_dtr_o",
                    width=1,
                    descr="Data terminal ready.",
                ),
                iob_signal(
                    name="rs232_gnd_i",
                    width=1,
                    descr="Ground.",
                ),
                iob_signal(
                    name="rs232_dsr_i",
                    width=1,
                    descr="Data set ready.",
                ),
            ]
        if self.n_pins == 4:
            self._signals += [
                iob_signal(
                    name="rs232_rts_o",
                    width=1,
                    descr="Request to send.",
                ),
                iob_signal(
                    name="rs232_cts_i",
                    width=1,
                    descr="Clear to send.",
                ),
            ]
        if self.n_pins == 9:
            self._signals += [
                iob_signal(
                    name="rs232_ri_i",
                    width=1,
                    descr="Ring indicator.",
                ),
            ]

#
# Wishbone
#

@dataclass
class WishboneInterface(_Interface):
    """Class to represent a Wishbone interface for generation"""

    # Data width for the Wishbone interface
    data_w: int = 32
    # Address width for the Wishbone interface
    addr_w: int = 32
    # Sets if it is a full Wishbone interface
    is_full: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.__set_signals()

        
    def __set_signals(self):
        """Set signals for the Wishbone interface."""
        self._signals += [
            iob_signal(
                name="wb_dat_i",
                width=self.data_w,
                descr="Data input.",
            ),
            iob_signal(
                name="wb_datout_o",
                width=self.data_w,
                descr="Data output.",
            ),
            iob_signal(
                name="wb_ack_i",
                descr="Acknowledge input. Indicates normal termination of a bus cycle.",
            ),
            iob_signal(
                name="wb_adr_o",
                width=self.addr_w,
                descr="Address output. Passes binary address.",
            ),
            iob_signal(
                name="wb_cyc_o",
                descr="Cycle output. Indicates a valid bus cycle.",
            ),
            iob_signal(
                name="wb_sel_o",
                width=self.data_w // 8,
                descr="Select output. Indicates where valid data is expected on the data bus.",
            ),
            iob_signal(
                name="wb_stb_o",
                descr="Strobe output. Indicates valid access.",
            ),
            iob_signal(
                name="wb_we_o",
                descr="Write enable. Indicates write access.",
            ),
        ]

        if self.is_full:
            self._signals += [
                iob_signal(
                    name="wb_clk_i",
                    descr="Clock input.",
                ),
                iob_signal(
                    name="wb_rst_i",
                    descr="Reset input.",
                ),
                iob_signal(
                    name="wb_tgd_i",
                    descr="Data tag type. Contains information associated with data lines [dat] and [strb].",
                ),
                iob_signal(
                    name="wb_tgd_o",
                    descr="Data tag type. Contains information associated with data lines [dat] and [strb].",
                ),
                iob_signal(
                    name="wb_err_i",
                    descr="Error input. Indicates abnormal cycle termination.",
                ),
                iob_signal(
                    name="wb_lock_o",
                    descr="Lock output. Indicates current bus cycle is uninterruptable.",
                ),
                iob_signal(
                    name="wb_rty_i",
                    descr="Retry input. Indicates interface is not ready to accept or send data, and cycle should be retried.",
                ),
                iob_signal(
                    name="wb_tga_o",
                    descr="Address tag type. Contains information associated with address lines [adr], and is qualified by signal [stb].",
                ),
                iob_signal(
                    name="wb_tgc_o",
                    descr="Cycle tag type. Contains information associated with bus cycles, and is qualified by signal [cyc].",
                ),
            ]



#
# Handle signal direction
#

# reverse direction in name's suffix
def reverse_name_direction(name):
    if name.endswith("_i"):
        return name[:-2] + "_o"
    elif name.endswith("_o"):
        return name[:-2] + "_i"
    elif name.endswith("_io"):
        return name
    else:
        print(f"ERROR: reverse_name_direction: invalid argument {name}.")
        exit(1)


# reverse module signal direction
def reverse_direction(direction):
    if direction == "input":
        return "output"
    elif direction == "output":
        return "input"
    else:
        print(f"ERROR: reverse_direction: invalid argument {direction}.")
        exit(1)


def reverse_signals_dir(signals):
    new_signals = deepcopy(signals)
    for signal in new_signals:
        signal.direction = reverse_direction(signal.direction)
        signal.name = reverse_name_direction(signal.name)
    return new_signals


# testbench signal direction
def get_tbsignal_type(direction):
    if direction == "input":
        return "wire"
    elif direction == "output":
        return "reg"
    else:
        print(f"ERROR: reverse_direction: invalid argument {direction}.")
        exit(1)


# get suffix from direction
def get_suffix(direction):
    if direction == "input":
        return "_i"
    elif direction == "output":
        return "_o"
    elif direction == "inout":
        return "_io"
    else:
        print(f"ERROR: reverse_direction: invalid argument {direction}.")
        exit(1)


#
# Port
#


# Write single port with given bus width, and name to file
def write_port(fout, prefix, port):
    direction = port.direction
    name = prefix + port.name
    width_str = f" [{port.width}-1:0] "
    fout.write(direction + width_str + name + "," + "\n")


def write_m_port(fout, prefix, port_list):
    for port in port_list:
        write_port(fout, prefix, port)


def write_s_port(fout, prefix, port_list):
    write_m_port(fout, prefix, port_list)


#
# Portmap
#


# Generate portmap string for a single port but width and name
def get_portmap_string(port_prefix, wire_prefix, port, connect_to_port):
    port_name = port_prefix + port.name
    wire_name = wire_prefix + port.name
    if not connect_to_port:
        suffix = get_suffix(port.direction)
        if wire_name.endswith(suffix):
            wire_name = wire_name[: -len(suffix)]
    return f".{port_name}({wire_name}),\n"


# Write single port with to file
def write_portmap(fout, port_prefix, wire_prefix, port, connect_to_port):
    portmap_string = get_portmap_string(
        port_prefix,
        wire_prefix,
        port,
        connect_to_port,
    )
    fout.write(portmap_string)


def write_m_portmap(fout, port_prefix, wire_prefix, port_list):
    for port in port_list:
        write_portmap(fout, port_prefix, wire_prefix, port, False)


def write_s_portmap(fout, port_prefix, wire_prefix, port_list):
    write_m_portmap(fout, port_prefix, wire_prefix, port_list)


def write_m_m_portmap(fout, port_prefix, wire_prefix, port_list):
    for port in port_list:
        write_portmap(fout, port_prefix, wire_prefix, port, True)


def write_s_s_portmap(fout, port_prefix, wire_prefix, port_list):
    write_m_m_portmap(fout, port_prefix, wire_prefix, port_list)


#
# Wire
#


# Write wire with given name, bus size, width to file
def write_single_wire(fout, prefix, wire, for_tb):
    if isinstance(wire, iob_signal_reference):
        return
    wire_name = prefix + wire.name
    suffix = get_suffix(wire.direction)
    if wire_name.endswith(suffix):
        wire_name = wire_name[: -len(suffix)]
    wtype = "wire"
    if for_tb:
        wire_name = wire_name + get_suffix(reverse_direction(wire.direction))
        wtype = get_tbsignal_type(wire.direction)
    if wire.isvar:
        wtype = "reg"
    width_str = f" [{wire.width}-1:0] "
    fout.write(wtype + width_str + wire_name + ";\n")


def write_wire(fout, prefix, wires):
    for wire in wires:
        write_single_wire(fout, prefix, wire, False)


def write_tb_wire(fout, prefix, wires):
    for wire in wires:
        write_single_wire(fout, prefix, wire, True)


def write_m_tb_wire(fout, prefix, wires):
    write_tb_wire(fout, prefix, wires)


def write_s_tb_wire(fout, prefix, wires):
    write_m_tb_wire(fout, prefix, wires)


#
# GENERATE INTERFACES
#


def get_signals(name, if_type="", mult=1, widths={}, params=None, signal_prefix=""):
    """Get list of signals for given interface
    param if_type: Type of interface.
                   Examples: '' (unspecified), 'manager', 'subordinate', ...
    param mult: Multiplication factor for all signal widths.
    param widths: Dictionary for configuration of specific signal widths.
    """
    eval_str = "get_" + name + "_ports(params=params,widths=widths)"
    # print(eval_str)
    signals = eval(eval_str)

    # Set direction according to if_type
    if if_type == "subordinate":
        signals = reverse_signals_dir(signals)
    # TODO: Code to support other if_types
    # For example, the rs232 has not type.

    if mult != 1:
        for signal in signals:
            signal.width = f"({mult}*{signal.width})"

    for signal in signals:
        signal.name = signal_prefix + signal.name

    return signals


def gen_if(interface):
    """Generate verilog snippets for all possible subtypes of a given interface"""
    name = interface.type
    file_prefix = interface.file_prefix
    portmap_port_prefix = interface.portmap_port_prefix
    prefix = interface.prefix
    mult = interface.mult
    params = interface.params
    widths = interface.widths

    #
    # GENERATE SNIPPETS FOR ALL TYPES OF PORTS AND WIRES
    #
    for if_type in if_types:
        fout = open(file_prefix + name + "_" + if_type + ".vs", "w")

        # get prefixes
        prefix1 = prefix
        prefix2_str = ""
        if "portmap" in if_type:
            prefix1 = portmap_port_prefix
            prefix2_str = " prefix,"

        # get ports
        if if_type.startswith("s"):
            ports = get_signals(
                name=name,
                if_type="subordinate",
                mult=mult,
                widths=widths,
                params=params,
            )
        else:
            ports = get_signals(
                name=name, if_type="manager", mult=mult, widths=widths, params=params
            )

        eval_str = f"write_{if_type}(fout, prefix1,{prefix2_str} ports)"
        # print(eval_str, prefix1)
        eval(eval_str)
        fout.close()


def gen_wires(interface):
    """Generate wires snippet for given interface"""
    name = interface.type
    file_prefix = interface.file_prefix
    prefix = interface.prefix
    mult = interface.mult
    params = interface.params
    widths = interface.widths

    signals = get_signals(
        name=name, if_type="", mult=mult, widths=widths, params=params
    )

    fout = open(file_prefix + name + "_wire.vs", "w")
    write_wire(fout, prefix, signals)
    fout.close()


#
# Test this Python module
#


if __name__ == "__main__":
    for if_name in if_names:
        gen_if(
            interface(
                type=if_name,
                file_prefix="bla_",
                prefix="di_",
                portmap_port_prefix="da_",
                widths={},
            )
        )
