# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from sqlite3 import connect

from matplotlib.pylab import f
from csr_classes import fail_with_msg


def get_fifo_csrs(csr_ref):
    fifo_csrs = []
    optional_comment = f"For use with FIFO: {csr_ref['name']}"
    if csr_ref["mode"] == "R":  # FIFO_R
        fifo_csrs += [
            {
                "name": f"{csr_ref['name']}_data",
                "type": "NOAUTO",
                "mode": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Read data from FIFO.",
                "internal_use": True,
                "optional_comment": optional_comment,
            },
            {
                "name": f"{csr_ref['name']}_empty",
                "mode": "R",
                "n_bits": 1,
                "rst_val": 1,
                "log2n_items": 0,
                "descr": "Empty (1) or non-empty (0).",
                "internal_use": True,
                "optional_comment": optional_comment,
            },
            {
                "name": f"{csr_ref['name']}_thresh",
                "mode": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Interrupt upper level threshold: an interrupt is triggered when the number of words in the FIFO reaches this upper level threshold.",
                "internal_use": True,
                "optional_comment": optional_comment,
            },
        ]
    elif csr_ref["mode"] == "W":  # FIFO_W
        fifo_csrs += [
            {
                "name": f"{csr_ref['name']}_data",
                "type": "NOAUTO",
                "mode": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Write data to FIFO.",
                "internal_use": True,
                "optional_comment": optional_comment,
            },
            {
                "name": f"{csr_ref['name']}_full",
                "mode": "R",
                "n_bits": 1,
                "rst_val": 0,
                "log2n_items": 0,
                "descr": "Full (1), or non-full (0).",
                "internal_use": True,
                "optional_comment": optional_comment,
            },
        ]
    else:  # FIFO_RW
        fail_with_msg("FIFOs of mode 'RW' are not supported.", ValueError)
    fifo_csrs += [
        {
            "name": f"{csr_ref['name']}_level",
            "mode": "R",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "descr": "Number of words in FIFO.",
            "internal_use": True,
            "optional_comment": optional_comment,
        },
    ]
    return fifo_csrs


def find_and_update_fifo_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the fifo CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of type "*FIFO". This CSR will be replaced by fifo_csrs.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add fifo instance, wires and ports.
    """
    csr_group_ref = None
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") in ["FIFO", "AFIFO"]:
                csr_group_ref = csr_group
                csr_ref = csr
                break

        if not csr_ref:
            continue

        # Add fifo_csrs to group
        csr_group_ref["regs"] += get_fifo_csrs(csr_ref)

        # Remove original csr from csr_group
        csr_group_ref["regs"].remove(csr_ref)

        create_fifo_instance(attributes_dict, csr_ref)


def create_fifo_instance(attributes_dict, csr_ref):
    """Add fifo instance, wires and ports to given attributes_dict, based on fifo description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add fifo instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with FIFO information.
    """
    fifo_name = csr_ref["name"]
    FIFO_NAME = fifo_name.upper()
    mode = csr_ref["mode"]
    is_async = csr_ref["type"] == "AFIFO"

    log2n_items = csr_ref["log2n_items"]
    # n_items = 2**log2n_items
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)
    internal_n_bits = (
        f"({asym} > 0 ? ({n_bits} * {asym}) : ({n_bits} / iob_abs({asym})))"
    )
    # external_n_bits = "DATA_W"

    wdata_w = n_bits if mode == "W" else internal_n_bits
    rdata_w = n_bits if mode == "R" else internal_n_bits
    # Higher address width (the one with lower data width)
    higher_addr_w = f"iob_max({log2n_items}, $clog2(iob_abs({asym})))"

    #
    # Confs: Based on confs from iob_fifo_sync.py
    #
    # Create confs to simplify long expressions.
    attributes_dict["confs"] += [
        {
            "name": f"{FIFO_NAME}_W_DATA_W",
            "descr": "",
            "type": "D",
            "val": wdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_R_DATA_W",
            "descr": "",
            "type": "D",
            "val": rdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_ADDR_W",
            "descr": "Higher ADDR_W lower DATA_W",
            "type": "D",
            "val": higher_addr_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_MAXDATA_W",
            "descr": "",
            "type": "D",
            "val": f"iob_max({FIFO_NAME}_W_DATA_W, {FIFO_NAME}_R_DATA_W)",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_R",
            "descr": "",
            "type": "D",
            "val": f"iob_abs({asym})",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_MINADDR_W",
            "descr": "Lower ADDR_W (higher DATA_W)",
            "type": "D",
            "val": f"{FIFO_NAME}_ADDR_W - $clog2({FIFO_NAME}_R)",
            "min": "NA",
            "max": "NA",
        },
    ]
    if is_async:
        #
        # Async FIFO Ports
        #
        if mode == "R":
            attributes_dict["ports"] += [
                {
                    "name": f"{fifo_name}_w_clk_en_rst_s",
                    "descr": "Write clock, clock enable and async reset",
                    "signals": {
                        "type": "iob_clk",
                        "prefix": "w_",
                    },
                },
                {
                    "name": f"{fifo_name}_w_rst_i",
                    "descr": "Write sync reset",
                    "signals": [{"name": f"{fifo_name}_w_rst_i"}],
                },
                {
                    "name": f"{fifo_name}_w_en_i",
                    "descr": "Write enable",
                    "signals": [{"name": f"{fifo_name}_w_en_i"}],
                },
                {
                    "name": f"{fifo_name}_w_data_i",
                    "descr": "Write data",
                    "signals": [{"name": f"{fifo_name}_w_data_i", "width": wdata_w}],
                },
                {
                    "name": f"{fifo_name}_w_full_o",
                    "descr": "Write full signal",
                    "signals": [{"name": f"{fifo_name}_w_full_o"}],
                },
                {
                    "name": f"{fifo_name}_w_empty_o",
                    "descr": "Write empty signal",
                    "signals": [{"name": f"{fifo_name}_w_empty_o"}],
                },
                {
                    "name": f"{fifo_name}_w_level_o",
                    "descr": "Write FIFO level",
                    "signals": [
                        {
                            "name": f"{fifo_name}_w_level_o",
                            "width": f"{FIFO_NAME}_ADDR_W+1",
                        }
                    ],
                },
            ]
        else:  # mode == "W":
            attributes_dict["ports"] += [
                {
                    "name": f"{fifo_name}_r_clk_en_rst_s",
                    "descr": "Read clock, clock enable and async reset",
                    "signals": {
                        "type": "iob_clk",
                        "prefix": "r_",
                    },
                },
                {
                    "name": f"{fifo_name}_r_rst_i",
                    "descr": "Read sync reset",
                    "signals": [{"name": f"{fifo_name}_r_rst_i"}],
                },
                {
                    "name": f"{fifo_name}_r_en_i",
                    "descr": "Read enable",
                    "signals": [{"name": f"{fifo_name}_r_en_i"}],
                },
                {
                    "name": f"{fifo_name}_r_data_o",
                    "descr": "Read data",
                    "signals": [{"name": f"{fifo_name}_r_data_o", "width": rdata_w}],
                },
                {
                    "name": f"{fifo_name}_r_full_o",
                    "descr": "Read full signal",
                    "signals": [{"name": f"{fifo_name}_r_full_o"}],
                },
                {
                    "name": f"{fifo_name}_r_empty_o",
                    "descr": "Read empty signal",
                    "signals": [{"name": f"{fifo_name}_r_empty_o"}],
                },
                {
                    "name": f"{fifo_name}_r_level_o",
                    "descr": "Read fifo level",
                    "signals": [
                        {
                            "name": f"{fifo_name}_r_level_o",
                            "width": f"{FIFO_NAME}_ADDR_W+1",
                        }
                    ],
                },
            ]

        attributes_dict["ports"].append(
            {
                "name": f"{fifo_name}_extmem_io",
                "descr": "External memory interface",
                "signals": [
                    #  Write port
                    {
                        "name": f"{fifo_name}_ext_mem_w_clk_o",
                        "width": 1,
                        "descr": "Memory clock",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_en_o",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_addr_o",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_data_o",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": f"{fifo_name}_ext_mem_r_clk_o",
                        "width": 1,
                        "descr": "Memory clock",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_en_o",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_addr_o",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_data_i",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            }
        )

    else:  # not is_async
        #
        # Sync FIFO Ports
        #
        attributes_dict["ports"].append(
            {
                "name": f"{fifo_name}_rst_i",
                "descr": "Synchronous reset interface.",
                "signals": [
                    {
                        "name": f"{fifo_name}_rst_i",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            }
        )
        if mode == "R":
            attributes_dict["ports"] += [
                {
                    "name": f"{fifo_name}_w_en_i",
                    "descr": "Write enable",
                    "signals": [{"name": f"{fifo_name}_w_en_i"}],
                },
                {
                    "name": f"{fifo_name}_w_data_i",
                    "descr": "Write data",
                    "signals": [{"name": f"{fifo_name}_w_data_i", "width": wdata_w}],
                },
                {
                    "name": f"{fifo_name}_w_full_o",
                    "descr": "Write full signal",
                    "signals": [{"name": f"{fifo_name}_w_full_o"}],
                },
                {
                    "name": f"{fifo_name}_interrupt_o",
                    "descr": "Connects directly to FIFO",
                    "signals": [
                        {
                            "name": f"{fifo_name}_interrupt_o",
                            "width": 1,
                            "descr": "FIFO interrupt. Active when level reaches threshold.",
                        },
                    ],
                },
            ]
        else:  # mode == "W"
            attributes_dict["ports"] += [
                {
                    "name": f"{fifo_name}_r_en_i",
                    "descr": "Read enable",
                    "signals": [{"name": f"{fifo_name}_r_en_i"}],
                },
                {
                    "name": f"{fifo_name}_r_data_o",
                    "descr": "Read data",
                    "signals": [{"name": f"{fifo_name}_r_data_o", "width": rdata_w}],
                },
                {
                    "name": f"{fifo_name}_r_empty_o",
                    "descr": "Read empty signal",
                    "signals": [{"name": f"{fifo_name}_r_empty_o"}],
                },
            ]

        attributes_dict["ports"] += [
            {
                "name": f"{fifo_name}_extmem_io",
                "descr": "FIFO external memory interface.",
                "signals": [
                    {
                        "name": f"{fifo_name}_ext_mem_clk_o",
                        "width": 1,
                    },
                    #  Read port
                    {
                        "name": f"{fifo_name}_ext_mem_r_en_o",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_addr_o",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_data_i",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory read data",
                    },
                    # Write port
                    {
                        "name": f"{fifo_name}_ext_mem_w_en_o",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_addr_o",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_data_o",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory write data",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_current_level_o",
                "descr": "Connects directly to FIFO",
                "signals": [
                    {
                        "name": f"{fifo_name}_current_level_o",
                        "width": f"{FIFO_NAME}_ADDR_W+1",
                        "descr": "FIFO level",
                    },
                ],
            },
        ]
    if mode == "W":
        attributes_dict["wires"] += [
            {
                "name": f"{fifo_name}_data_wen",
                "descr": "FIFO data write enable",
                "signals": [
                    {"name": f"{fifo_name}_data_wen", "width": 1},
                ],
            },
        ]
    else:  # mode R
        attributes_dict["wires"] += [
            {
                "name": f"{fifo_name}_data_ren",
                "descr": "FIFO data read enable",
                "signals": [
                    {"name": f"{fifo_name}_data_ren", "width": 1},
                ],
            },
        ]
    if is_async:
        #
        # Async FIFO Wires
        #
        if mode == "W":
            attributes_dict["wires"] += [
                {
                    "name": f"{fifo_name}_data_wen",
                    "descr": "FIFO data write enable",
                    "signals": [
                        {"name": f"{fifo_name}_data_wen"},
                    ],
                },
                {
                    "name": f"{fifo_name}_data_wdata",
                    "descr": "FIFO data write data",
                    "signals": [
                        {"name": f"{fifo_name}_data_wdata", "width": 32},
                    ],
                },
                {
                    "name": f"{fifo_name}_full",
                    "descr": "FIFO full signal",
                    "signals": [{"name": f"{fifo_name}_full"}],
                },
                {
                    "name": f"{fifo_name}_empty",
                    "descr": "FIFO empty signal",
                    "signals": [{"name": f"{fifo_name}_empty"}],
                },
                {
                    "name": f"{fifo_name}_level",
                    "descr": "FIFO level",
                    "signals": [{"name": f"{fifo_name}_level", "width": 32}],
                },
            ]

        else:  # mode == "R"
            attributes_dict["wires"] += [
                {
                    "name": f"{fifo_name}_data_ren",
                    "descr": "FIFO data read enable",
                    "signals": [
                        {"name": f"{fifo_name}_data_ren"},
                    ],
                },
                {
                    "name": f"{fifo_name}_data_rdata",
                    "descr": "FIFO data read data",
                    "signals": [
                        {"name": f"{fifo_name}_data_rdata", "width": 32},
                    ],
                },
                {
                    "name": f"{fifo_name}_full",
                    "descr": "FIFO full signal",
                    "signals": [{"name": f"{fifo_name}_full"}],
                },
                {
                    "name": f"{fifo_name}_empty",
                    "descr": "FIFO empty signal",
                    "signals": [{"name": f"{fifo_name}_empty"}],
                },
                {
                    "name": f"{fifo_name}_level",
                    "descr": "FIFO level",
                    "signals": [{"name": f"{fifo_name}_level", "width": 32}],
                },
            ]
    else:  # not is_async
        #
        # Sync FIFO Wires
        #
        if mode == "W":
            attributes_dict["wires"] += [
                {
                    "name": f"{fifo_name}_data_wen",
                    "descr": "FIFO data write enable.",
                    "signals": [{"name": f"{fifo_name}_data_wen"}],
                },
                {
                    "name": f"{fifo_name}_data_wdata",
                    "descr": "FIFO data write data.",
                    "signals": [{"name": f"{fifo_name}_data_wdata", "width": 32}],
                },
                {
                    "name": f"{fifo_name}_full",
                    "descr": "FIFO full signal.",
                    "signals": [{"name": f"{fifo_name}_full"}],
                },
            ]
        else:  # mode == "R"
            attributes_dict["wires"] += [
                {
                    "name": f"{fifo_name}_data_ren",
                    "descr": "FIFO data read enable.",
                    "signals": [{"name": f"{fifo_name}_data_ren"}],
                },
                {
                    "name": f"{fifo_name}_data_rdata",
                    "descr": "FIFO data read data.",
                    "signals": [{"name": f"{fifo_name}_data_rdata", "width": 32}],
                },
                {
                    "name": f"{fifo_name}_empty",
                    "descr": "FIFO empty signal.",
                    "signals": [{"name": f"{fifo_name}_empty"}],
                },
            ]
    #
    # Blocks
    #
    if is_async:
        if mode == "W":
            # Connect write interface to CSR wires and read interface to ports
            fifo_connect = {
                "w_clk_en_rst_s": "clk_en_rst_s",
                "w_rst_i": "1'd0",
                "w_en_i": f"{fifo_name}_data_wen",
                "w_data_i": f"{fifo_name}_data_wdata",
                "w_full_o": f"{fifo_name}_full",
                "w_empty_o": f"{fifo_name}_empty",
                "w_level_o": f"{fifo_name}_level",
                "r_clk_en_rst_s": f"{fifo_name}_r_clk_en_rst_s",
                "r_rst_i": f"{fifo_name}_r_rst_i",
                "r_en_i": f"{fifo_name}_r_en_i",
                "r_data_o": f"{fifo_name}_r_data_o",
                "r_full_o": f"{fifo_name}_r_full_o",
                "r_empty_o": f"{fifo_name}_r_empty_o",
                "r_level_o": f"{fifo_name}_r_level_o",
            }

        else:  # mode == "R"
            # Connect read interface to CSR wires and write interface to ports
            fifo_connect = {
                "r_clk_en_rst_s": "clk_en_rst_s",
                "r_rst_i": "1'd0",
                "r_en_i": f"{fifo_name}_data_ren",
                "r_data_o": f"{fifo_name}_data_rdata",
                "r_full_o": f"{fifo_name}_full",
                "r_empty_o": f"{fifo_name}_empty",
                "r_level_o": f"{fifo_name}_level",
                "w_clk_en_rst_s": f"{fifo_name}_w_clk_en_rst_s",
                "w_rst_i": f"{fifo_name}_w_rst_i",
                "w_en_i": f"{fifo_name}_w_en_i",
                "w_data_i": f"{fifo_name}_w_data_i",
                "w_full_o": f"{fifo_name}_w_full_o",
                "w_empty_o": f"{fifo_name}_w_empty_o",
                "w_level_o": f"{fifo_name}_w_level_o",
            }

        fifo_connect["extmem_io"] = f"{fifo_name}_extmem_io"

        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_fifo_async",
                "instance_name": fifo_name,
                "instance_description": f"Asyncronous FIFO {fifo_name}",
                "parameters": {
                    "W_DATA_W": f"{FIFO_NAME}_W_DATA_W",
                    "R_DATA_W": f"{FIFO_NAME}_R_DATA_W",
                    "ADDR_W": f"{FIFO_NAME}_ADDR_W",
                },
                "connect": fifo_connect,
            }
        )
    else:  # not is_async
        if mode == "W":
            # Connect write interface to CSR wires and read interface to ports
            fifo_connect = {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": f"{fifo_name}_rst_i",
                "w_en_i": f"{fifo_name}_data_wen",
                "w_data_i": f"{fifo_name}_data_wdata",
                "w_full_o": f"{fifo_name}_full",
                "r_en_i": f"{fifo_name}_r_en_i",
                "r_data_o": f"{fifo_name}_r_data_o",
                "r_empty_o": f"{fifo_name}_r_empty_o",
                "extmem_io": f"{fifo_name}_extmem_io",
                "level_o": f"{fifo_name}_current_level_o",
            }
        else:  # mode == "R"
            # Connect read interface to CSR wires and write interface to ports
            fifo_connect = {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": f"{fifo_name}_rst_i",
                "r_en_i": f"{fifo_name}_data_ren",
                "r_data_o": f"{fifo_name}_data_rdata",
                "r_empty_o": f"{fifo_name}_empty",
                "w_en_i": f"{fifo_name}_w_en_i",
                "w_data_i": f"{fifo_name}_w_data_i",
                "w_full_o": f"{fifo_name}_full",
                "extmem_io": f"{fifo_name}_extmem_io",
                "level_o": f"{fifo_name}_current_level_o",
            }

        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_fifo_sync",
                "instance_name": fifo_name,
                "instance_description": f"Synchronous FIFO {fifo_name}",
                "parameters": {
                    "W_DATA_W": f"{FIFO_NAME}_W_DATA_W",
                    "R_DATA_W": f"{FIFO_NAME}_R_DATA_W",
                    "ADDR_W": f"{FIFO_NAME}_ADDR_W",
                },
                "connect": fifo_connect,
            }
        )
    #
    # Snippets
    #

    if not is_async:
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Connect FIFO level status to CSRs
   assign {fifo_name}_level_wdata = {fifo_name}_current_level_o;

""",
            }
        )
    if not is_async and mode == "R":
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Generate interrupt signal
   assign {fifo_name}_interrupt_o ={fifo_name}_current_level_o >= {fifo_name}_thresh_rdata;
""",
            }
        )

    if mode == "W":
        attributes_dict["snippets"] += [
            {
                "verilog_code": f"""
   // Generate wen signal
   assign {fifo_name}_data_wen = {fifo_name}_data_valid & |{fifo_name}_data_wstrb;

""",
            }
        ]
    else:  # mode R
        attributes_dict["snippets"] += [
            {
                "verilog_code": f"""
   // Generate ren signal
   assign {fifo_name}_data_ren = {fifo_name}_data_valid;

""",
            }
        ]
