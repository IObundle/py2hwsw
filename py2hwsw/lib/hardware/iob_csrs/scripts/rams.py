# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def find_and_update_ram_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the ram CSRs group and update the dictionary
    accordingly.
    RAMs use iob_dp_ram, with memories outside the csrs core.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add ram instance, wires and ports.
    """
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "RAM":
                csr_ref = csr
                break

        if not csr_ref:
            continue

        # Replace original csr with "NOAUTO" type
        csr_ref["type"] = "NOAUTO"
        # Don't generate standard ports for this CSR.
        # It will be internal to the CSRs module, and have a custom port generated later.
        csr_ref["internal_use"] = True

        if "R" in csr_ref["mode"]:
            create_ram_instance(attributes_dict, csr_ref, "R")
        if "W" in csr_ref["mode"]:
            create_ram_instance(attributes_dict, csr_ref, "W")


def create_ram_instance(attributes_dict, csr_ref, mode):
    """Add ram instance, wires and ports to given attributes_dict, based on ram description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add ram instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with RAM information.
    """
    ram_name = csr_ref["name"]
    RAM_NAME = ram_name.upper()

    log2n_items = csr_ref["log2n_items"]
    n_items = 2**log2n_items
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)
    internal_n_bits = (
        f"({asym} > 0 ? ({n_bits} * {asym}) : ({n_bits} / iob_abs({asym})))"
    )
    # external_n_bits = "DATA_W"

    wdata_w = n_bits if mode == "W" else internal_n_bits
    rdata_w = n_bits if mode == "R" else internal_n_bits
    waddr_w = (
        log2n_items if mode == "W" else (f"{log2n_items} + $clog2(iob_abs({asym}))")
    )
    raddr_w = (
        log2n_items if mode == "R" else (f"{log2n_items} + $clog2(iob_abs({asym}))")
    )

    #
    # Confs: Based on confs from iob_ram_2p.py
    #
    # Create confs to simplify long expressions.
    attributes_dict["confs"] += [
        {
            "name": f"{RAM_NAME}_W_DATA_W",
            "descr": "",
            "type": "D",
            "val": wdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{RAM_NAME}_R_DATA_W",
            "descr": "",
            "type": "D",
            "val": rdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{RAM_NAME}_W_ADDR_W",
            "descr": "Write address width",
            "type": "D",
            "val": waddr_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{RAM_NAME}_R_ADDR_W",
            "descr": "Read address width",
            "type": "D",
            "val": raddr_w,
            "min": "NA",
            "max": "NA",
        },
    ]
    #
    # Ports
    #
    if mode == "R":
        attributes_dict["ports"] += [
            {
                "name": f"{ram_name}_write_i",
                "descr": "RAM write interface.",
                "signals": [
                    {
                        "name": f"{ram_name}_w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{ram_name}_w_strb_i",
                        "width": f"{RAM_NAME}_W_DATA_W/8",
                        "descr": "Write strobe",
                    },
                    {
                        "name": f"{ram_name}_w_addr_i",
                        "width": f"{RAM_NAME}_W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": f"{ram_name}_w_data_i",
                        "width": f"{RAM_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
        ]
    else:  # mode == "W"
        attributes_dict["ports"].append(
            {
                "name": f"{ram_name}_read_io",
                "descr": "RAM read interface.",
                "signals": [
                    {
                        "name": f"{ram_name}_r_addr_i",
                        "width": f"{RAM_NAME}_R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": f"{ram_name}_r_data_o",
                        "width": f"{RAM_NAME}_R_DATA_W",
                        "descr": "Read data",
                    },
                ],
            }
        )
    attributes_dict["wires"] += []
    #
    # Wires
    #
    if mode == "W":
        attributes_dict["wires"] += [
            {
                "name": f"{ram_name}_wen",
                "descr": "ram data write enable",
                "signals": [
                    {"name": f"{ram_name}_wen", "width": 1},
                ],
            },
            {
                "name": f"{ram_name}_write_i",
                "descr": "RAM write interface.",
                "signals": [
                    {"name": f"{ram_name}_wen", "width": 1},
                    # Wstrb unused. Connected to high in verilog snippet.
                    {
                        "name": f"{ram_name}_w_strb",
                        "width": f"{RAM_NAME}_W_DATA_W/8",
                    },
                    # FIXME: Not using verilog parameters WADDR_W and WDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{ram_name}_addr", "width": waddr_w},
                    {"name": f"{ram_name}_wdata", "width": wdata_w},
                ],
            },
        ]
    else:  # mode == "R"
        attributes_dict["wires"].append(
            {
                "name": f"{ram_name}_read_io",
                "descr": "RAM read interface.",
                "signals": [
                    # FIXME: Not using verilog parameters RADDR_W and RDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{ram_name}_addr", "width": raddr_w},
                    {"name": f"{ram_name}_rdata", "width": rdata_w},
                ],
            }
        )
    #
    # Blocks
    #
    attributes_dict["subblocks"].append(
        {
            "core_name": "iob_ram_2p",
            "instance_name": ram_name,
            "instance_description": f"RAM {ram_name}",
            "parameters": {
                "N": n_items,  # number of registers
                "W": n_bits,  # register width
                "WDATA_W": f"{RAM_NAME}_W_DATA_W",  # width of write data
                "WADDR_W": f"{RAM_NAME}_W_ADDR_W",  # width of write address
                "RDATA_W": f"{RAM_NAME}_R_DATA_W",  # width of read data
                "RADDR_W": f"{RAM_NAME}_R_ADDR_W",  # width of read address
                "DATA_W": "DATA_W",  # width of each register
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "write_i": f"{ram_name}_write_i",
                "read_io": f"{ram_name}_read_io",
            },
        }
    )
    #
    # Snippets
    #
    if mode == "W":
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Write always connected to high
   assign {ram_name}_w_strb = {{{RAM_NAME}_W_DATA_W/8{{1'b1}}}};
   // Always ready
   assign {ram_name}_ready = 1'b1;
   // Generate wen signal
   assign {ram_name}_wen = {ram_name}_valid & {ram_name}_ready & |{ram_name}_wstrb;
""",
            }
        )
    if mode == "R":
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Always ready and rvalid
   assign {ram_name}_ready = 1'b1;
   assign {ram_name}_rvalid = 1'b1;
""",
            }
        )
