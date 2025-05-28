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
                csr_ref = csr

                # Replace original csr with "NOAUTO" type
                csr_ref["type"] = "NOAUTO"
                # Don't generate standard ports for this CSR.
                # It will be internal to the CSRs module, and have a custom port generated later.
                csr_ref["internal_use"] = True

                create_memory_instance(
                    attributes_dict, csr_ref, memory_type="iob_regarray_dp_be"
                )


def find_and_update_regfile_csrs(csrs_dict, attributes_dict):
    """Given a dictionary of CSRs, find the regfile CSRs group and update the dictionary
    accordingly.
    REGFILEs use iob_dp_ram, with memories inside the csrs core.
    :param dict csrs_dict: Dictionary of CSRs to update.
    :param dict attributes_dict: Dictionary of core attributes to add regfile instance, wires and ports.
    """
    for csr_group in csrs_dict:
        csr_ref = None
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "REGFILE":
                csr_ref = csr
                break

        if not csr_ref:
            continue

        # Replace original csr with "NOAUTO" type
        csr_ref["type"] = "NOAUTO"
        # Don't generate standard ports for this CSR.
        # It will be internal to the CSRs module, and have a custom port generated later.
        csr_ref["internal_use"] = True

        create_memory_instance(attributes_dict, csr_ref, memory_type="iob_ram_tdp_be")


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

        create_memory_instance(
            attributes_dict,
            csr_ref,
            memory_type="iob_ram_tdp_be",
            internal_memory=False,
        )


def create_memory_instance(
    attributes_dict, csr_ref, memory_type="iob_regarray_dp_be", internal_memory=True
):
    """Add memory instance, wires and ports to given attributes_dict, based on memory description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add memory instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with MEMORY information.
    :param dict memory_type: Memory type to use (regarray, regfile, ram).
    :param bool internal_memory: True if memory should be instantiated inside the CSRs module. Export memory ports otherwise.
    """
    memory_name = csr_ref["name"]
    MEMORY_NAME = memory_name.upper()

    mode = csr_ref["mode"]
    log2n_items = csr_ref["log2n_items"]
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)

    #
    # Confs
    #
    attributes_dict["confs"] += [
        # Localparams to simplify long expressions.
        # Note: external_n_bits = "DATA_W"
        {
            "name": f"{MEMORY_NAME}_INTERNAL_DATA_W",
            "descr": "Data width of the memory interface for the core",
            "type": "D",
            "val": f"({asym} > 0 ? ({n_bits} * {asym}) : ({n_bits} / iob_abs({asym})))",
            "min": "NA",
            "max": "NA",
        },
        # Note: external_addr_w = "ADDR_W"
        {
            "name": f"{MEMORY_NAME}_INTERNAL_ADDR_W",
            "descr": "Address width of the memory interface for the core",
            "type": "D",
            "val": f"{asym} > 0 ? ({log2n_items} + $clog2(iob_abs({asym}))) : ({log2n_items} - $clog2(iob_abs({asym})))",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{MEMORY_NAME}_MAX_ADDR_W",
            "descr": "Hiher address width of the memory asymetric interfaces",
            "type": "D",
            "val": f"{asym} > 0 ? ({log2n_items} + $clog2(iob_abs({asym}))) : {log2n_items}",
            "min": "NA",
            "max": "NA",
        },
    ]
    #
    # Ports
    #
    if "W" in mode:
        attributes_dict["ports"].append(
            {
                "name": f"{memory_name}_read_io",
                "descr": "MEMORY read interface.",
                "signals": [
                    {
                        "name": f"{memory_name}_r_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{memory_name}_r_addr_i",
                        "width": f"{MEMORY_NAME}_R_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": f"{memory_name}_r_data_o",
                        "width": f"{MEMORY_NAME}_R_DATA_W",
                        "descr": "Read data",
                    },
                ],
            }
        )
    if "R" in mode:
        attributes_dict["ports"] += [
            {
                "name": f"{memory_name}_write_i",
                "descr": "MEMORY write interface.",
                "signals": [
                    {
                        "name": f"{memory_name}_w_en_i",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{memory_name}_w_strb_i",
                        "width": f"{MEMORY_NAME}_W_DATA_W/8",
                        "descr": "Write strobe",
                    },
                    {
                        "name": f"{memory_name}_w_addr_i",
                        "width": f"{MEMORY_NAME}_W_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": f"{memory_name}_w_data_i",
                        "width": f"{MEMORY_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
        ]
    memory_wires = [
        # Wires for dual ports of memory
        {
            "name": f"{memory_name}_port_a_io",
            "descr": f"Port A of memory {memory_name}",
            "signals": [
                {"name": f"{memory_name}_enA_i", "width": 1},
                {"name": f"{memory_name}_wstrbA_i", "width": f"{n_bits}/8"},
                {"name": f"{memory_name}_addrA_i", "width": log2n_items},
                {"name": f"{memory_name}_dA_i", "width": n_bits},
                {"name": f"{memory_name}_dA_o", "width": n_bits},
            ],
        },
        {
            "name": f"{memory_name}_port_b_io",
            "descr": f"Port B of memory {memory_name}",
            "signals": [
                {"name": f"{memory_name}_enB_i", "width": 1},
                {"name": f"{memory_name}_wstrbB_i", "width": f"{n_bits}/8"},
                {"name": f"{memory_name}_addrB_i", "width": log2n_items},
                {"name": f"{memory_name}_dB_i", "width": n_bits},
                {"name": f"{memory_name}_dB_o", "width": n_bits},
            ],
        },
    ]
    if not internal_memory:
        # Export dual ports of memory
        attributes_dict["ports"] += memory_wires
    #
    # Wires
    #
    if internal_memory:
        # Wires for dual ports of memory
        attributes_dict["wires"] += memory_wires
    attributes_dict["wires"] += [
        # Asym converter wires
        {
            "name": f"{memory_name}_asym_s_io",
            "descr": "Subordinate interface of asym",
            "signals": [
                {"name": f"{memory_name}_asym_en_i", "width": 1},
                {
                    "name": f"{memory_name}_asym_wstrb_i",
                    "width": f"{MEMORY_NAME}_INTERNAL_DATA_W/8",
                },
                {
                    "name": f"{memory_name}_asym_addr_i",
                    "width": f"{MEMORY_NAME}_INTERNAL_ADDR_W",
                },
                {
                    "name": f"{memory_name}_asym_d_i",
                    "width": f"{MEMORY_NAME}_INTERNAL_DATA_W",
                },
                {
                    "name": f"{memory_name}_asym_d_o",
                    "width": f"{MEMORY_NAME}_INTERNAL_DATA_W",
                },
            ],
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_asym_converter",
            "instance_name": f"{memory_name}_asym_converter",
            "instance_description": f"Asymetric converter for MEMORY {memory_name}",
            "parameters": {
                "MDATA_W": f"{MEMORY_NAME}_INTERNAL_DATA_W",  # width of manager data
                "SDATA_W": n_bits,  # width of subordinate data
                "ADDR_W": f"{MEMORY_NAME}_MAX_ADDR_W",  # width of higher address
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "m_io": f"{memory_name}_port_b_io",
                "s_io": f"{memory_name}_asym_s_io",
            },
        },
    ]
    if internal_memory:
        attributes_dict["subblocks"] += [
            {
                "core_name": memory_type,
                "instance_name": memory_name,
                "instance_description": f"MEMORY {memory_name}",
                "parameters": {
                    "DATA_W": n_bits,
                    "ADDR_W": log2n_items,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "port_a_io": f"{memory_name}_port_a_io",
                    "port_b_io": f"{memory_name}_port_b_io",
                },
            },
        ]
    #
    # Snippets
    #
    snippet = f"""
    // MEMORY: {MEMORY_NAME}

"""
    # Signals for Port A of memory
    snippet = f"""
    // Connect Port A to internal logic (for cbus)
    assign enA_i = {memory_name}_valid & {memory_name}_ready;
    assign addrA_i = {memory_name}_addr;
    // Respond with always ready
    assign {memory_name}_ready = 1'b1;
"""
    # Port A write signals
    if "W" in mode:
        snippet = f"""
    // Write signals
    assign wstrbA_i = {memory_name}_wstrb;
    assign dA_i = {memory_name}_wdata;
"""
    else:
        snippet = """
    // Write signals (unused)
    assign wstrbA_i = 'd0;
    assign dA_i = 'd0;
"""
    # Port A read signals
    if "R" in mode:
        snippet = f"""
    // Read signals
    assign {memory_name}_rdata = dA_o;
    // {memory_name}_rready unused
    assign {memory_name}_rvalid = 1'b1;
"""

    # Signals for subordinate port of asym converter
    snippet = """
    // Connect asym converter subordinate port to core's logic
"""
    if mode == "RW":
        snippet = f"""
    assign {memory_name}_asym_en_i = {memory_name}_w_en_i | {memory_name}_r_en_i;
    assign {memory_name}_asym_wstrb_i = {memory_name}_w_strb_i;
    assign {memory_name}_asym_addr_i = {memory_name}_w_en_i ? {memory_name}_w_addr_i : {memory_name}_r_addr_i;
    assign {memory_name}_asym_d_i = {memory_name}_w_data_i;
    assign {memory_name}_r_data_o = {memory_name}_asym_d_o;
"""
    elif mode == "W":
        snippet = f"""
    assign {memory_name}_asym_en_i = {memory_name}_r_en_i;
    assign {memory_name}_asym_wstrb_i = 'd0;
    assign {memory_name}_asym_addr_i = {memory_name}_r_addr_i;
    assign {memory_name}_asym_d_i = 'd0;
    assign {memory_name}_r_data_o = {memory_name}_asym_d_o;
"""
    elif mode == "R":
        snippet = f"""
    assign {memory_name}_asym_en_i = {memory_name}_w_en_i;
    assign {memory_name}_asym_wstrb_i = {memory_name}_w_strb_i;
    assign {memory_name}_asym_addr_i = {memory_name}_w_addr_i;
    assign {memory_name}_asym_d_i = {memory_name}_w_data_i;
"""

    attributes_dict["snippets"].append({"verilog_code": snippet})
