#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# this script generates interfaces for Verilog modules and testbenches to add a
# new standard interface, add the name to the interface_names list, and an
# interface dictionary as below run this script with the -h option for help
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict
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


# NOTE: artur: I believe the 'params' attribute could be merged with 'widths' attibute.
@dataclass
class interface:
    """Class to represent an interface for generation"""

    # Type/Name of interface to generate
    type: str = ""
    # Prefix for signals of the interface
    prefix: str = ""
    # Width multiplier. Used when concatenating multiple instances of the interface.
    mult: str | int = 1
    # Generic string parameter that is passed to "get_<interface>_ports" function
    params: str = None
    # Dictionary of width properties of interface
    widths: Dict[str, str] = field(default_factory=dict)
    # Prefix for generated "Verilog Snippets" of this interface
    file_prefix: str = ""
    # Prefix for "Verilog snippets" of portmaps of this interface:
    portmap_port_prefix: str = ""

    def __post_init__(self):
        if not self.file_prefix:
            self.file_prefix = self.portmap_port_prefix + self.prefix


def dict2interface(interface_dict):
    """Convert dictionary to 'interface' class instance.
    Example interface dict:
    {
        "name": "cpu_m",
        "descr": "cpu instruction bus",
        "signals": {
            "type": "iob",
            # Generic string parameter
            "params": "",
            # Widths/Other parameters
            "DATA_W": "DATA_W",
            "ADDR_W": "ADDR_W",
        },
    },
    """
    if not interface_dict:
        return None
    interface_attributes = interface.__dataclass_fields__.keys()
    # Extract 'widths' from dictionary
    widths = {}
    new_interface_dict = {}
    for k, v in interface_dict.items():
        if k not in interface_attributes:
            widths[k] = v
        else:
            new_interface_dict[k] = v

    return interface(**new_interface_dict, widths=widths)


def parse_widths(func):
    """Decorator to temporarily change values of global variables based on `widths` dictionary."""

    def inner(widths={}, params=None):
        vars_backup = {}
        interface_name = func.__name__[4:-6]
        # Backup global variables
        for k, v in widths.items():
            assert (
                k in globals()
            ), f"The provided width variable '{k}' does not exist for interface '{interface_name}'!"
            vars_backup[k] = globals()[k]
            globals()[k] = v
        # Call the function
        if params is not None:
            return_obj = func(params)
        else:
            return_obj = func()
        # Restore global variables
        for k in widths:
            globals()[k] = vars_backup[k]
        return return_obj

    return inner


def try_math_eval(expr):
    """Try to evaluate math expressions, otherwise return the input."""
    try:
        return int(eval(expr, {"__builtins__": None}, {}))
    except TypeError:
        return expr


DATA_W = 32
DATA_SECTION_W = 8
ADDR_W = 32

#
# below are functions that return interface ports for each interface type
# the port direction is relative to the manager module (driver)
#


@parse_widths
def get_iob_ports():
    return [
        iob_signal(
            name="iob_valid_o",
            width=1,
            descr="Request address is valid.",
        ),
        iob_signal(
            name="iob_addr_o",
            width=ADDR_W,
            descr="Byte address.",
        ),
        iob_signal(
            name="iob_wdata_o",
            width=DATA_W,
            descr="Write data.",
        ),
        iob_signal(
            name="iob_wstrb_o",
            width=try_math_eval(f"{DATA_W}/{DATA_SECTION_W}"),
            descr="Write strobe.",
        ),
        iob_signal(
            name="iob_rvalid_i",
            width=1,
            descr="Read data valid.",
        ),
        iob_signal(
            name="iob_rdata_i",
            width=DATA_W,
            descr="Read data.",
        ),
        iob_signal(
            name="iob_ready_i",
            width=1,
            descr="Interface ready.",
        ),
    ]


@parse_widths
def get_iob_clk_ports(params: str = None):
    if params is None:
        params = "c_a"

    reset_polarity = getattr(iob_globals(), "reset_polarity", "positive")

    if reset_polarity != "positive":
        params = params.replace("a", "an")
    else:
        params = params.replace("an", "a")

    params = params.split("_")

    ports = [
        iob_signal(
            name="clk_o",
            width=1,
            descr="Clock",
        )
    ]

    for param, port, descr in [
        ("c", "cke", "Clock enable"),
        ("a", "arst", "Asynchronous active-high reset"),
        ("an", "arst_n", "Asynchronous active-low reset"),
        ("r", "rst", "Synchronous active-high reset"),
        ("e", "en", "Enable"),
    ]:
        if param in params:
            ports.append(
                iob_signal(
                    name=port + "_o",
                    width=1,
                    descr=descr,
                )
            )
    return ports


def get_mem_ports(
    suffix: str, async_clk: bool = False, addr: bool = True, enable: bool = True
):
    clk_prefix = f"{suffix}_" if async_clk else ""
    suffix = f"_{suffix}" if suffix else ""
    mem_ports = [
        iob_signal(
            name=clk_prefix + "clk" + "_o",
            width=1,
            descr=f"Clock port {clk_prefix}",
        ),
    ]
    if addr:
        mem_ports.append(
            iob_signal(
                name="addr" + suffix + "_o",
                width=ADDR_W,
                descr=f"Address port {suffix}",
            )
        )
    if enable:
        mem_ports.append(
            iob_signal(
                name="en" + suffix + "_o",
                width=1,
                descr=f"Enable port {suffix}",
            )
        )
    return mem_ports


def get_mem_read_ports(
    suffix: str,
    enable: bool = False,
    ready: bool = False,
    addr: bool = False,
    true: bool = False,
):
    suffix = f"_{suffix}" if suffix else ""
    rd_suffix = suffix if true else ""
    mem_read_ports = []
    if enable:
        mem_read_ports.append(
            iob_signal(
                name="r_en" + suffix + "_o",
                width=1,
                descr=f"Read enable port {suffix}",
            )
        )
    if addr:
        mem_read_ports.append(
            iob_signal(
                name="r_addr" + suffix + "_o",
                width=ADDR_W,
                descr=f"Read address port {suffix}",
            )
        )
    mem_read_ports += [
        iob_signal(
            name="r_data" + rd_suffix + "_i",
            width=DATA_W,
            descr=f"Data port {suffix}",
        ),
    ]
    if ready:
        mem_read_ports.append(
            iob_signal(
                name="r_ready" + suffix + "_i",
                width=1,
                descr=f"Read ready port {suffix}",
            )
        )
    return mem_read_ports


def get_mem_write_ports(
    suffix: str,
    ready: bool = False,
    addr: bool = False,
    true: bool = False,
    byte_enable: bool = False,
):
    suffix = f"_{suffix}" if suffix else ""
    wr_suffix = suffix if true else ""
    mem_write_ports = []
    if byte_enable:
        mem_write_ports.append(
            iob_signal(
                name="w_strb" + suffix + "_o",
                width=try_math_eval(f"{DATA_W}/{DATA_SECTION_W}"),
                descr=f"Write strobe port {suffix}",
            )
        )
    else:  # No byte enable
        mem_write_ports.append(
            iob_signal(
                name="w_en" + suffix + "_o",
                width=1,
                descr=f"Write enable port {suffix}",
            )
        )
    if addr:
        mem_write_ports.append(
            iob_signal(
                name="w_addr" + suffix + "_o",
                width=ADDR_W,
                descr=f"Write address port {suffix}",
            )
        )

    mem_write_ports += [
        iob_signal(
            name="w_data" + wr_suffix + "_o",
            width=DATA_W,
            descr=f"Data port {suffix}",
        ),
    ]
    if ready:
        mem_write_ports.append(
            iob_signal(
                name="w_ready" + suffix + "_i",
                width=1,
                descr=f"Write ready port {suffix}",
            )
        )
    return mem_write_ports


def remove_duplicates(ports):
    seen_dicts = []
    result = []
    for d in ports:
        if d not in seen_dicts:
            seen_dicts.append(d)
            result.append(d)
    return result


# Memory symbols meaning:
# SP: Single-Port read-write
# 2P: 2-Port (one read, one write)
# DP: Dual-Port (two read-write)
# TDP/T2P: True (Dual-/2-)Port; Can perform transactions in both ports at the same time
# ATDP/AT2P: Asynchronous ports
# BE: byte-enable for each byte of data word
# SE: Single enable for entire data word
# Xil: Xilinx IP implementation

@parse_widths
def get_rom_2p_ports():
    ports = (
        get_mem_ports("", addr=False, enable=False)
        + get_mem_read_ports("a", enable=True, ready=True, addr=True)
        + get_mem_read_ports("b", enable=True, ready=True, addr=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_rom_sp_ports():
    ports = get_mem_ports("") + get_mem_read_ports("")
    return remove_duplicates(ports)


@parse_widths
def get_rom_tdp_ports():
    ports = (
        get_mem_ports("", enable=False, addr=False)
        + get_mem_read_ports("a", enable=True, addr=True, true=True)
        + get_mem_read_ports("b", enable=True, addr=True, true=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_rom_atdp_ports():
    ports = (
        get_mem_ports("a", async_clk=True)
        + get_mem_read_ports("a", true=True)
        + get_mem_ports("b", async_clk=True)
        + get_mem_read_ports("b", true=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_2p_ports():
    ports = (
        get_mem_ports("", addr=False, enable=False)
        + get_mem_read_ports("", enable=True, ready=True, addr=True)
        + get_mem_write_ports("", ready=True, addr=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_at2p_ports():
    ports = (
        get_mem_ports("r", async_clk=True, addr=False, enable=False)
        + get_mem_read_ports("", enable=True, addr=True)
        + get_mem_ports("w", async_clk=True, addr=False, enable=False)
        + get_mem_write_ports("", addr=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_atdp_ports():
    ports = (
        get_mem_ports("a", async_clk=True)
        + get_mem_read_ports("a", true=True)
        + get_mem_write_ports("a", true=True)
        + get_mem_ports("b", async_clk=True)
        + get_mem_read_ports("b", true=True)
        + get_mem_write_ports("b", true=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_atdp_be_ports():
    ports = (
        get_mem_ports("a", async_clk=True)
        + get_mem_read_ports("a", true=True)
        + get_mem_write_ports("a", true=True, byte_enable=True)
        + get_mem_ports("b", async_clk=True)
        + get_mem_read_ports("b", true=True)
        + get_mem_write_ports("b", true=True, byte_enable=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_sp_ports():
    ports = get_mem_ports("") + get_mem_read_ports("") + get_mem_write_ports("")
    return remove_duplicates(ports)


@parse_widths
def get_ram_sp_be_ports():
    ports = (
        get_mem_ports("")
        + get_mem_read_ports("")
        + get_mem_write_ports("", byte_enable=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_sp_se_ports():
    return get_ram_sp_ports()


@parse_widths
def get_ram_t2p_ports():
    ports = (
        get_mem_ports("", addr=False, enable=False)
        + get_mem_read_ports("", enable=True, addr=True)
        + get_mem_write_ports("", addr=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_t2p_be_ports():
    ports = (
        get_mem_ports("", addr=False, enable=False)
        + get_mem_read_ports("", enable=True, addr=True)
        + get_mem_write_ports("", addr=True, byte_enable=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_t2p_tiled_ports():
    ports = (
        get_mem_ports("", enable=False)
        + get_mem_read_ports("", enable=True)
        + get_mem_write_ports("")
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_tdp_ports():
    ports = (
        get_mem_ports("a")
        + get_mem_read_ports("a")
        + get_mem_write_ports("a")
        + get_mem_ports("b")
        + get_mem_read_ports("b")
        + get_mem_write_ports("b")
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_tdp_be_ports():
    ports = (
        get_mem_ports("a")
        + get_mem_read_ports("a")
        + get_mem_write_ports("a", byte_enable=True)
        + get_mem_ports("b")
        + get_mem_read_ports("b")
        + get_mem_write_ports("b", byte_enable=True)
    )
    return remove_duplicates(ports)


@parse_widths
def get_ram_tdp_be_xil_ports():
    return get_ram_tdp_be_ports()


@parse_widths
def get_regfile_2p_ports():
    raise NotImplementedError("REGFILE 2P not interface implemented")


@parse_widths
def get_regfile_at2p_ports():
    raise NotImplementedError("REGFILE AT2P not interface implemented")


@parse_widths
def get_regfile_sp_ports():
    raise NotImplementedError("REGFILE SP not interface implemented")


#
# AXI4
#
ID_W = 1
SIZE_W = 3
BURST_W = 2
LOCK_W = 2
CACHE_W = 4
PROT_W = 3
QOS_W = 4
RESP_W = 2
LEN_W = 8


@parse_widths
def get_axil_write_ports(params: str = None):
    if params is None:
        params = ""
    params = params.split("_")

    signals = [
        iob_signal(
            name="axil_awaddr_o",
            width=ADDR_W,
            descr="Address write channel byte address.",
        ),
    ]
    if "prot" in params:
        signals += [
            iob_signal(
                name="axil_awprot_o",
                width=PROT_W,
                descr="Address write channel protection type. Set to 000 if manager output; ignored if subordinate input.",
            ),
        ]
    signals += [
        iob_signal(
            name="axil_awvalid_o",
            width=1,
            descr="Address write channel valid.",
        ),
        iob_signal(
            name="axil_awready_i",
            width=1,
            descr="Address write channel ready.",
        ),
        iob_signal(
            name="axil_wdata_o",
            width=DATA_W,
            descr="Write channel data.",
        ),
        iob_signal(
            name="axil_wstrb_o",
            width=try_math_eval(f"{DATA_W}/{DATA_SECTION_W}"),
            descr="Write channel write strobe.",
        ),
        iob_signal(
            name="axil_wvalid_o",
            width=1,
            descr="Write channel valid.",
        ),
        iob_signal(
            name="axil_wready_i",
            width=1,
            descr="Write channel ready.",
        ),
        iob_signal(
            name="axil_bresp_i",
            width=RESP_W,
            descr="Write response channel response.",
        ),
        iob_signal(
            name="axil_bvalid_i",
            width=1,
            descr="Write response channel valid.",
        ),
        iob_signal(
            name="axil_bready_o",
            width=1,
            descr="Write response channel ready.",
        ),
    ]
    return signals


@parse_widths
def get_axil_read_ports(params: str = None):
    if params is None:
        params = ""
    params = params.split("_")

    signals = [
        iob_signal(
            name="axil_araddr_o",
            width=ADDR_W,
            descr="Address read channel byte address.",
        ),
    ]
    if "prot" in params:
        signals += [
            iob_signal(
                name="axil_arprot_o",
                width=PROT_W,
                descr="Address read channel protection type. Set to 000 if manager output; ignored if subordinate input.",
            ),
        ]
    signals += [
        iob_signal(
            name="axil_arvalid_o",
            width=1,
            descr="Address read channel valid.",
        ),
        iob_signal(
            name="axil_arready_i",
            width=1,
            descr="Address read channel ready.",
        ),
        iob_signal(
            name="axil_rdata_i",
            width=DATA_W,
            descr="Read channel data.",
        ),
        iob_signal(
            name="axil_rresp_i",
            width=RESP_W,
            descr="Read channel response.",
        ),
        iob_signal(
            name="axil_rvalid_i",
            width=1,
            descr="Read channel valid.",
        ),
        iob_signal(
            name="axil_rready_o",
            width=1,
            descr="Read channel ready.",
        ),
    ]
    return signals


@parse_widths
def get_axil_ports(params: str = None):
    return get_axil_read_ports(params=params) + get_axil_write_ports(params=params)


@parse_widths
def get_axi_write_ports(params: str = None):
    axil_write = get_axil_write_ports(params=params)

    for port in axil_write:
        port.name = port.name.replace("axil", "axi")

    return axil_write + [
        iob_signal(
            name="axi_awid_o",
            width=ID_W,
            descr="Address write channel ID.",
        ),
        iob_signal(
            name="axi_awlen_o",
            width=LEN_W,
            descr="Address write channel burst length.",
        ),
        iob_signal(
            name="axi_awsize_o",
            width=SIZE_W,
            descr="Address write channel burst size. This signal indicates the size of each transfer in the burst.",
        ),
        iob_signal(
            name="axi_awburst_o",
            width=BURST_W,
            descr="Address write channel burst type.",
        ),
        iob_signal(
            name="axi_awlock_o",
            width=LOCK_W,
            descr="Address write channel lock type.",
        ),
        iob_signal(
            name="axi_awcache_o",
            width=CACHE_W,
            descr="Address write channel memory type. Set to 0000 if manager output; ignored if subordinate input.",
        ),
        iob_signal(
            name="axi_awqos_o",
            width=QOS_W,
            descr="Address write channel quality of service.",
        ),
        iob_signal(
            name="axi_wlast_o",
            width=1,
            descr="Write channel last word flag.",
        ),
        iob_signal(
            name="axi_bid_i",
            width=ID_W,
            descr="Write response channel ID.",
        ),
    ]


@parse_widths
def get_axi_read_ports(params: str = None):
    axil_read = get_axil_read_ports(params=params)

    for port in axil_read:
        port.name = port.name.replace("axil", "axi")

    return axil_read + [
        iob_signal(
            name="axi_arid_o",
            width=ID_W,
            descr="Address read channel ID.",
        ),
        iob_signal(
            name="axi_arlen_o",
            width=LEN_W,
            descr="Address read channel burst length.",
        ),
        iob_signal(
            name="axi_arsize_o",
            width=SIZE_W,
            descr="Address read channel burst size. This signal indicates the size of each transfer in the burst.",
        ),
        iob_signal(
            name="axi_arburst_o",
            width=BURST_W,
            descr="Address read channel burst type.",
        ),
        iob_signal(
            name="axi_arlock_o",
            width=LOCK_W,
            descr="Address read channel lock type.",
        ),
        iob_signal(
            name="axi_arcache_o",
            width=CACHE_W,
            descr="Address read channel memory type. Set to 0000 if manager output; ignored if subordinate input.",
        ),
        iob_signal(
            name="axi_arqos_o",
            width=QOS_W,
            descr="Address read channel quality of service.",
        ),
        iob_signal(
            name="axi_rid_i",
            width=ID_W,
            descr="Read channel ID.",
        ),
        iob_signal(
            name="axi_rlast_i",
            width=1,
            descr="Read channel last word.",
        ),
    ]


@parse_widths
def get_axi_ports(params: str = None):
    return get_axi_read_ports(params=params) + get_axi_write_ports(params=params)


@parse_widths
def get_axis_ports(params: str = None):
    if params is None:
        params = ""
    params = params.split("_")

    signals = [
        iob_signal(
            name="axis_tvalid_o",
            width=1,
            descr="axis stream valid.",
        ),
        iob_signal(
            name="axis_tready_i",
            width=1,
            descr="axis stream ready.",
        ),
        iob_signal(
            name="axis_tdata_o",
            width=DATA_W,
            descr="axis stream data.",
        ),
    ]
    if "tlast" in params:
        signals += [
            iob_signal(
                name="axis_tlast_o",
                width=1,
                descr="axis stream last.",
            ),
        ]
    return signals


#
# APB
#


@parse_widths
def get_apb_ports():
    return [
        iob_signal(
            name="apb_addr_o",
            width=ADDR_W,
            descr="Byte address of the transfer.",
        ),
        iob_signal(
            name="apb_sel_o",
            width=1,
            descr="Subordinate select.",
        ),
        iob_signal(
            name="apb_enable_o",
            width=1,
            descr="Enable. Indicates the number of clock cycles of the transfer.",
        ),
        iob_signal(
            name="apb_write_o",
            width=1,
            descr="Write. Indicates the direction of the operation.",
        ),
        iob_signal(
            name="apb_wdata_o",
            width=DATA_W,
            descr="Write data.",
        ),
        iob_signal(
            name="apb_wstrb_o",
            width=try_math_eval(f"{DATA_W}/{DATA_SECTION_W}"),
            descr="Write strobe.",
        ),
        iob_signal(
            name="apb_rdata_i",
            width=DATA_W,
            descr="Read data.",
        ),
        iob_signal(
            name="apb_ready_i",
            width=1,
            descr="Ready. Indicates the end of a transfer.",
        ),
    ]


#
# AHB
#
AHB_PROT_W = 4
AHB_BURST_W = 3
AHB_TRANS_W = 2


@parse_widths
def get_ahb_ports():
    return [
        iob_signal(
            name="ahb_addr_o",
            width=ADDR_W,
            descr="Byte address of the transfer.",
        ),
        iob_signal(
            name="ahb_burst_o",
            width=AHB_BURST_W,
            descr="Burst size.",
        ),
        iob_signal(
            name="ahb_mastlock_o",
            width=1,
            descr="Current transfer is locked sequence.",
        ),
        iob_signal(
            name="ahb_prot_o",
            width=AHB_PROT_W,
            descr="Byte address of the transfer.",
        ),
        iob_signal(
            name="ahb_size_o",
            width=SIZE_W,
            descr="Size of transfer.",
        ),
        iob_signal(
            name="ahb_trans_o",
            width=AHB_TRANS_W,
            descr="Transfer type.",
        ),
        iob_signal(
            name="ahb_wdata_o",
            width=DATA_W,
            descr="Write data.",
        ),
        iob_signal(
            name="ahb_wstrb_o",
            width=try_math_eval(f"{DATA_W}/{8}"),
            descr="Write strobe.",
        ),
        iob_signal(
            name="ahb_write_o",
            width=1,
            descr="Transfer direction: (1) Write; (0) Read.",
        ),
        iob_signal(
            name="ahb_rdata_i",
            width=DATA_W,
            descr="Read data.",
        ),
        iob_signal(
            name="ahb_readyout_i",
            width=1,
            descr="Transfer finished on the bus.",
        ),
        iob_signal(
            name="ahb_resp_i",
            width=1,
            descr="Transfer response: (0) Okay; (1) Error.",
        ),
        iob_signal(
            name="ahb_sel_o",
            width=1,
            descr="Subordinate select.",
        ),
    ]


#
# RS232
#
N_PINS = 4


@parse_widths
def get_rs232_ports():
    assert N_PINS in [2, 4, 9], "rs232 'N_PINS' must be 2, 4 or 9!"
    ports = []
    if N_PINS == 9:
        ports += [
            iob_signal(
                name="rs232_dcd_i",
                width=1,
                descr="Data carrier detect.",
            ),
        ]
    if N_PINS in [2, 4]:
        ports += [
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
    if N_PINS == 9:
        ports += [
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
    if N_PINS == 4:
        ports += [
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
    if N_PINS == 9:
        ports += [
            iob_signal(
                name="rs232_ri_i",
                width=1,
                descr="Ring indicator.",
            ),
        ]

    return ports


#
# Wishbone
#


@parse_widths
def get_wb_ports():
    ports = [
        iob_signal(
            name="wb_dat_i",
            width=DATA_W,
            descr="Data input.",
        ),
        iob_signal(
            name="wb_datout_o",
            width=DATA_W,
            descr="Data output.",
        ),
        iob_signal(
            name="wb_ack_i",
            width=1,
            descr="Acknowledge input. Indicates normal termination of a bus cycle.",
        ),
        iob_signal(
            name="wb_adr_o",
            width=ADDR_W,
            descr="Address output. Passes binary address.",
        ),
        iob_signal(
            name="wb_cyc_o",
            width=1,
            descr="Cycle output. Indicates a valid bus cycle.",
        ),
        iob_signal(
            name="wb_sel_o",
            width=try_math_eval(f"{DATA_W}/{DATA_SECTION_W}"),
            descr="Select output. Indicates where valid data is expected on the data bus.",
        ),
        iob_signal(
            name="wb_stb_o",
            width=1,
            descr="Strobe output. Indicates valid access.",
        ),
        iob_signal(
            name="wb_we_o",
            width=1,
            descr="Write enable. Indicates write access.",
        ),
    ]

    return ports


@parse_widths
def get_wb_full_ports():
    ports = get_wb_ports()
    ports += [
        iob_signal(
            name="wb_clk_i",
            width=1,
            descr="Clock input.",
        ),
        iob_signal(
            name="wb_rst_i",
            width=1,
            descr="Reset input.",
        ),
        iob_signal(
            name="wb_tgd_i",
            width=1,
            descr="Data tag type. Contains information associated with data lines [dat] and [strb].",
        ),
        iob_signal(
            name="wb_tgd_o",
            width=1,
            descr="Data tag type. Contains information associated with data lines [dat] and [strb].",
        ),
        iob_signal(
            name="wb_err_i",
            width=1,
            descr="Error input. Indicates abnormal cycle termination.",
        ),
        iob_signal(
            name="wb_lock_o",
            width=1,
            descr="Lock output. Indicates current bus cycle is uninterruptable.",
        ),
        iob_signal(
            name="wb_rty_i",
            width=1,
            descr="Retry input. Indicates interface is not ready to accept or send data, and cycle should be retried.",
        ),
        iob_signal(
            name="wb_tga_o",
            width=1,
            descr="Address tag type. Contains information associated with address lines [adr], and is qualified by signal [stb].",
        ),
        iob_signal(
            name="wb_tgc_o",
            width=1,
            descr="Cycle tag type. Contains information associated with bus cycles, and is qualified by signal [cyc].",
        ),
    ]

    return ports


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
