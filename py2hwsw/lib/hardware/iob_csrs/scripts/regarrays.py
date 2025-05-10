# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def find_and_update_regarray_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the regarray CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of type "*REGARRAY". This CSR will be replaced by regarray_csrs.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add regarray instance, wires and ports.
    """
    csr_group_ref = None
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "REG") == "REG" and csr.get("log2n_items", 0) > 0:
                csr_group_ref = csr_group
                csr_ref = csr

                # Replace original csr with "NOAUTO" type
                csr_ref["type"] = "NOAUTO"
                # Don't generate standard ports for this CSR.
                # It will be internal to the CSRs module, and have a custom port generated later.
                csr_ref["internal_use"] = True

                if "R" in csr_ref["mode"]:
                    create_regarray_instance(attributes_dict, csr_ref, "R")
                if "W" in csr_ref["mode"]:
                    create_regarray_instance(attributes_dict, csr_ref, "W")
                # FIXME: If RW, make sure signals do not colide


def create_regarray_instance(attributes_dict, csr_ref, mode):
    """Add regarray instance, wires and ports to given attributes_dict, based on regarray description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add regarray instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with REGARRAY information.
    """
    regarray_name = csr_ref["name"]
    REGARRAY_NAME = regarray_name.upper()

    log2n_items = csr_ref["log2n_items"]
    n_items = 2**log2n_items
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)
    asym_sign = f"iob_sign({asym})"
    internal_n_bits = f"({n_bits} * ({asym}**{asym_sign}))"
    # external_n_bits = "DATA_W"

    wdata_w = n_bits if mode == "W" else internal_n_bits
    rdata_w = n_bits if mode == "R" else internal_n_bits
    waddr_w = (
        log2n_items
        if mode == "W"
        else (f"{log2n_items} + {asym_sign} * $clog2(iob_abs({asym}))")
    )
    raddr_w = (
        log2n_items
        if mode == "R"
        else (f"{log2n_items} + {asym_sign} * $clog2(iob_abs({asym}))")
    )

    #
    # Confs: Based on confs from iob_regarray_2p.py
    #
    # Create confs to simplify long expressions.
    attributes_dict["confs"] += [
        {
            "name": f"{REGARRAY_NAME}_W_DATA_W",
            "descr": "",
            "type": "D",
            "val": wdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGARRAY_NAME}_R_DATA_W",
            "descr": "",
            "type": "D",
            "val": rdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGARRAY_NAME}_W_ADDR_W",
            "descr": "Write address width",
            "type": "D",
            "val": waddr_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGARRAY_NAME}_R_ADDR_W",
            "descr": "Read address width",
            "type": "D",
            "val": raddr_w,
            "min": "NA",
            "max": "NA",
        },
    ]
    #
    # Ports
    if mode == "R":
        attributes_dict["ports"] += [
            {
                "name": f"{regarray_name}_write_i",
                "descr": "REGARRAY write interface.",
                "signals": [
                    {
                        "name": f"{regarray_name}_w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{regarray_name}_w_strb_i",
                        "width": f"{REGARRAY_NAME}_W_DATA_W/8",
                        "descr": "Write strobe",
                    },
                    {
                        "name": f"{regarray_name}_w_addr_i",
                        "width": f"{REGARRAY_NAME}_W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": f"{regarray_name}_w_data_i",
                        "width": f"{REGARRAY_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
        ]
    else:  # mode == "W"
        attributes_dict["ports"].append(
            {
                "name": f"{regarray_name}_read_io",
                "descr": "REGARRAY read interface.",
                "signals": [
                    {
                        "name": f"{regarray_name}_r_addr_i",
                        "width": f"{REGARRAY_NAME}_R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": f"{regarray_name}_r_data_o",
                        "width": f"{REGARRAY_NAME}_R_DATA_W",
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
                "name": f"{regarray_name}_wen",
                "descr": "Regarray data write enable",
                "signals": [
                    {"name": f"{regarray_name}_wen", "width": 1},
                ],
            },
            {
                "name": f"{regarray_name}_write_i",
                "descr": "REGARRAY write interface.",
                "signals": [
                    {"name": f"{regarray_name}_wen", "width": 1},
                    # Wstrb unused. Connected to high in verilog snippet.
                    {"name": f"{regarray_name}_w_strb", "width": "WDATA_W/8"},
                    # FIXME: Not using verilog parameters WADDR_W and WDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{regarray_name}_addr", "width": waddr_w},
                    {"name": f"{regarray_name}_wdata", "width": wdata_w},
                ],
            },
        ]
    else:  # mode == "R"
        attributes_dict["wires"].append(
            {
                "name": f"{regarray_name}_read_io",
                "descr": "REGARRAY read interface.",
                "signals": [
                    # FIXME: Not using verilog parameters RADDR_W and RDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{regarray_name}_addr", "width": raddr_w},
                    {"name": f"{regarray_name}_rdata", "width": rdata_w},
                ],
            }
        )
    #
    # Blocks
    #
    attributes_dict["subblocks"].append(
        {
            "core_name": "iob_regarray_2p",
            "instance_name": regarray_name,
            "instance_description": f"REGARRAY {regarray_name}",
            "parameters": {
                "N": n_items,  # number of registers
                "W": n_bits,  # register width
                "WDATA_W": f"{REGARRAY_NAME}_W_DATA_W",  # width of write data
                "WADDR_W": f"{REGARRAY_NAME}_W_ADDR_W",  # width of write address
                "RDATA_W": f"{REGARRAY_NAME}_R_DATA_W",  # width of read data
                "RADDR_W": f"{REGARRAY_NAME}_R_ADDR_W",  # width of read address
                "DATA_W": "DATA_W",  # width of each register
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "write_i": f"{regarray_name}_write_i",
                "read_io": f"{regarray_name}_read_io",
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
   assign {regarray_name}_w_strb = {{WDATA_W/8{{1'b1}}}};
   // Always ready
   assign {regarray_name}_ready = 1'b1;
   // Generate wen signal
   assign {regarray_name}_wen = {regarray_name}_valid & {regarray_name}_ready & |{regarray_name}_wstrb;
""",
            }
        )
    if mode == "R":
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Always ready and rvalid
   assign {regarray_name}_ready = 1'b1;
   assign {regarray_name}_rvalid = 1'b1;
""",
            }
        )
