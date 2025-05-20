# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def find_and_update_regfile_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the regfile CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of type "*REGFILE". This CSR will be replaced by regfile_csrs.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add regfile instance, wires and ports.
    """
    csr_group_ref = None
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            # Try to convert log2n_items to int
            log2n_items = csr.get("log2n_items", 0)
            try:
                log2n_items = int(log2n_items)
            except ValueError:
                pass

            # Reg arrays contain log2n_items > 0
            # If log2n_items is not int, assume it is a verilog expression with parameters, so it likely is > 0
            if csr.get("type", "REG") == "REG" and (
                type(log2n_items) is not int or log2n_items > 0
            ):
                csr_group_ref = csr_group
                csr_ref = csr

                # Replace original csr with "NOAUTO" type
                csr_ref["type"] = "NOAUTO"
                # Don't generate standard ports for this CSR.
                # It will be internal to the CSRs module, and have a custom port generated later.
                csr_ref["internal_use"] = True

                if "R" in csr_ref["mode"]:
                    create_regfile_instance(attributes_dict, csr_ref, "R")
                if "W" in csr_ref["mode"]:
                    create_regfile_instance(attributes_dict, csr_ref, "W")
                # FIXME: If RW, make sure signals do not colide


def create_regfile_instance(attributes_dict, csr_ref, mode):
    """Add regfile instance, wires and ports to given attributes_dict, based on regfile description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add regfile instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with REGFILE information.
    """
    regfile_name = csr_ref["name"]
    REGFILE_NAME = regfile_name.upper()

    log2n_items = csr_ref["log2n_items"]
    n_items = 2**log2n_items
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)
    internal_n_bits = (
        f"($signed({asym}) > 0 ? ({n_bits} * {asym}) : ({n_bits} / iob_abs({asym})))"
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
    # Confs: Based on confs from iob_regfile_2p.py
    #
    # Create confs to simplify long expressions.
    attributes_dict["confs"] += [
        {
            "name": f"{REGFILE_NAME}_W_DATA_W",
            "descr": "",
            "type": "D",
            "val": wdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGFILE_NAME}_R_DATA_W",
            "descr": "",
            "type": "D",
            "val": rdata_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGFILE_NAME}_W_ADDR_W",
            "descr": "Write address width",
            "type": "D",
            "val": waddr_w,
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGFILE_NAME}_R_ADDR_W",
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
                "name": f"{regfile_name}_write_i",
                "descr": "REGFILE write interface.",
                "signals": [
                    {
                        "name": f"{regfile_name}_w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{regfile_name}_w_strb_i",
                        "width": f"{REGFILE_NAME}_W_DATA_W/8",
                        "descr": "Write strobe",
                    },
                    {
                        "name": f"{regfile_name}_w_addr_i",
                        "width": f"{REGFILE_NAME}_W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": f"{regfile_name}_w_data_i",
                        "width": f"{REGFILE_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
        ]
    else:  # mode == "W"
        attributes_dict["ports"].append(
            {
                "name": f"{regfile_name}_read_io",
                "descr": "REGFILE read interface.",
                "signals": [
                    {
                        "name": f"{regfile_name}_r_addr_i",
                        "width": f"{REGFILE_NAME}_R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": f"{regfile_name}_r_data_o",
                        "width": f"{REGFILE_NAME}_R_DATA_W",
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
                "name": f"{regfile_name}_wen",
                "descr": "regfile data write enable",
                "signals": [
                    {"name": f"{regfile_name}_wen", "width": 1},
                ],
            },
            {
                "name": f"{regfile_name}_write_i",
                "descr": "REGFILE write interface.",
                "signals": [
                    {"name": f"{regfile_name}_wen", "width": 1},
                    # Wstrb unused. Connected to high in verilog snippet.
                    {
                        "name": f"{regfile_name}_w_strb",
                        "width": f"{REGFILE_NAME}_W_DATA_W/8",
                    },
                    # FIXME: Not using verilog parameters WADDR_W and WDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{regfile_name}_addr", "width": waddr_w},
                    {"name": f"{regfile_name}_wdata", "width": wdata_w},
                ],
            },
        ]
    else:  # mode == "R"
        attributes_dict["wires"].append(
            {
                "name": f"{regfile_name}_read_io",
                "descr": "REGFILE read interface.",
                "signals": [
                    # FIXME: Not using verilog parameters RADDR_W and RDATA_W because csr_gen later creates a reference with 'n_bits' width
                    # but it would be better to use verilog parameters so the core can override it if needed.
                    {"name": f"{regfile_name}_addr", "width": raddr_w},
                    {"name": f"{regfile_name}_rdata", "width": rdata_w},
                ],
            }
        )
    #
    # Blocks
    #
    attributes_dict["subblocks"].append(
        {
            "core_name": "iob_regfile_2p",
            "instance_name": regfile_name,
            "instance_description": f"REGFILE {regfile_name}",
            "parameters": {
                "N": n_items,  # number of registers
                "W": n_bits,  # register width
                "WDATA_W": f"{REGFILE_NAME}_W_DATA_W",  # width of write data
                "WADDR_W": f"{REGFILE_NAME}_W_ADDR_W",  # width of write address
                "RDATA_W": f"{REGFILE_NAME}_R_DATA_W",  # width of read data
                "RADDR_W": f"{REGFILE_NAME}_R_ADDR_W",  # width of read address
                "DATA_W": "DATA_W",  # width of each register
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "write_i": f"{regfile_name}_write_i",
                "read_io": f"{regfile_name}_read_io",
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
   assign {regfile_name}_w_strb = {{{REGFILE_NAME}_W_DATA_W/8{{1'b1}}}};
   // Always ready
   assign {regfile_name}_ready = 1'b1;
   // Generate wen signal
   assign {regfile_name}_wen = {regfile_name}_valid & {regfile_name}_ready & |{regfile_name}_wstrb;
""",
            }
        )
    if mode == "R":
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
   // Always ready and rvalid
   assign {regfile_name}_ready = 1'b1;
   assign {regfile_name}_rvalid = 1'b1;
""",
            }
        )
