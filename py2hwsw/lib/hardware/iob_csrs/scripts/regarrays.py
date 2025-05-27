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

                create_regarray_instance(attributes_dict, csr_ref)


def create_regarray_instance(attributes_dict, csr_ref):
    """Add regarray instance, wires and ports to given attributes_dict, based on regarray description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add regarray instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with REGARRAY information.
    """
    regarray_name = csr_ref["name"]
    REGARRAY_NAME = regarray_name.upper()

    mode = csr_ref["mode"]
    log2n_items = csr_ref["log2n_items"]
    n_bits = csr_ref["n_bits"]
    asym = csr_ref.get("asym", 1)

    #
    # Confs: Based on confs from iob_regarray_2p.py
    #
    attributes_dict["confs"] += [
        # Localparams to simplify long expressions.
        # Note: external_n_bits = "DATA_W"
        {
            "name": f"{REGARRAY_NAME}_INTERNAL_DATA_W",
            "descr": "Data width of the regarray interface for the core",
            "type": "D",
            "val": f"({asym} > 0 ? ({n_bits} * {asym}) : ({n_bits} / iob_abs({asym})))",
            "min": "NA",
            "max": "NA",
        },
        # Note: external_addr_w = "ADDR_W"
        {
            "name": f"{REGARRAY_NAME}_INTERNAL_ADDR_W",
            "descr": "Address width of the regarray interface for the core",
            "type": "D",
            "val": f"{asym} > 0 ? ({log2n_items} + $clog2(iob_abs({asym}))) : ({log2n_items} - $clog2(iob_abs({asym})))",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{REGARRAY_NAME}_MAX_ADDR_W",
            "descr": "Hiher address width of the regarray asymetric interfaces",
            "type": "D",
            "val": f"{asym} > 0 ? ({log2n_items} + $clog2(iob_abs({asym}))) : {log2n_items}",
            "min": "NA",
            "max": "NA",
        },
    ]
    #
    # Ports
    #
    # FIXME: Fix ports
    # if mode == "R":
    #     attributes_dict["ports"] += [
    #         {
    #             "name": f"{regarray_name}_write_i",
    #             "descr": "REGARRAY write interface.",
    #             "signals": [
    #                 {
    #                     "name": f"{regarray_name}_w_en_i",
    #                     "width": 1,
    #                     "descr": "Write enable",
    #                 },
    #                 {
    #                     "name": f"{regarray_name}_w_strb_i",
    #                     "width": f"{REGARRAY_NAME}_W_DATA_W/8",
    #                     "descr": "Write strobe",
    #                 },
    #                 {
    #                     "name": f"{regarray_name}_w_addr_i",
    #                     "width": f"{REGARRAY_NAME}_W_ADDR_W",
    #                     "descr": "Write address",
    #                 },
    #                 {
    #                     "name": f"{regarray_name}_w_data_i",
    #                     "width": f"{REGARRAY_NAME}_W_DATA_W",
    #                     "descr": "Write data",
    #                 },
    #             ],
    #         },
    #     ]
    # else:  # mode == "W"
    #     attributes_dict["ports"].append(
    #         {
    #             "name": f"{regarray_name}_read_io",
    #             "descr": "REGARRAY read interface.",
    #             "signals": [
    #                 {
    #                     "name": f"{regarray_name}_r_addr_i",
    #                     "width": f"{REGARRAY_NAME}_R_ADDR_W",
    #                     "descr": "Read address",
    #                 },
    #                 {
    #                     "name": f"{regarray_name}_r_data_o",
    #                     "width": f"{REGARRAY_NAME}_R_DATA_W",
    #                     "descr": "Read data",
    #                 },
    #             ],
    #         }
    #     )
    attributes_dict["wires"] += []
    #
    # Wires
    #
    attributes_dict["wires"] += [
        {
            "name": "rst",
            "descr": "Synchronous reset",
            "signals": [
                {"name": "rst", "width": 1},
            ],
        },
        # Wires for dual ports of regarray
        {
            "name": f"{regarray_name}_port_a_io",
            "descr": "Port A",
            "signals": [
                {"name": f"{regarray_name}_a_en_i", "width": 1},
                {"name": f"{regarray_name}_a_wstrb_i", "width": f"{n_bits}/8"},
                {"name": f"{regarray_name}_a_addr_i", "width": log2n_items},
                {"name": f"{regarray_name}_a_data_i", "width": n_bits},
                {"name": f"{regarray_name}_a_data_o", "width": n_bits},
            ],
        },
        {
            "name": f"{regarray_name}_port_b_io",
            "descr": "Port B",
            "signals": [
                {"name": f"{regarray_name}_b_en_i", "width": 1},
                {"name": f"{regarray_name}_b_wstrb_i", "width": f"{n_bits}/8"},
                {"name": f"{regarray_name}_b_addr_i", "width": log2n_items},
                {"name": f"{regarray_name}_b_data_i", "width": n_bits},
                {"name": f"{regarray_name}_b_data_o", "width": n_bits},
            ],
        },
    ]

    if "W" in mode:
        attributes_dict["wires"] += [
            # FIXME: Check correcct ports of asym converter
            {
                "name": f"{regarray_name}_w_asym_m_io",
                "descr": "Manager interface of W asym",
                "signals": [
                    {
                        "name": f"{regarray_name}_w_asym_m_en_o",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{regarray_name}_w_asym_m_addr_o",
                        "width": log2n_items,
                        "descr": "Write address",
                    },
                    {
                        "name": f"{regarray_name}_w_asym_m_data_i",
                        "width": n_bits,
                        "descr": "Write data",
                    },
                ],
            },
            {
                "name": f"{regarray_name}_w_asym_s_io",
                "descr": "Subordinate interface of W asym",
                "signals": [
                    {
                        "name": f"{regarray_name}_w_asym_s_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{regarray_name}_w_asym_s_addr_i",
                        "width": f"{REGARRAY_NAME}_INTERNAL_ADDR_W",
                        "descr": "Read address",
                    },
                    {
                        "name": f"{regarray_name}_w_asym_s_data_o",
                        "width": f"{REGARRAY_NAME}_INTERNAL_DATA_W",
                        "descr": "Read data",
                    },
                ],
            },
            # FIXME: Fix wires
            #######
            #######
            #######
            #######
            # {
            #     "name": f"{regarray_name}_wen",
            #     "descr": "Regarray data write enable",
            #     "signals": [
            #         {"name": f"{regarray_name}_wen", "width": 1},
            #     ],
            # },
            # {
            #     "name": f"{regarray_name}_write_i",
            #     "descr": "REGARRAY write interface.",
            #     "signals": [
            #         {"name": f"{regarray_name}_wen", "width": 1},
            #         # Wstrb unused. Connected to high in verilog snippet.
            #         {
            #             "name": f"{regarray_name}_w_strb",
            #             "width": f"{REGARRAY_NAME}_W_DATA_W/8",
            #         },
            #         # FIXME: Not using verilog parameters WADDR_W and WDATA_W because csr_gen later creates a signal reference with 'n_bits' width (this throws an errror during setup if signals have different widths)
            #         # but it would be better to use verilog parameters so the core can override it if needed.
            #         {"name": f"{regarray_name}_addr", "width": waddr_w},
            #         {"name": f"{regarray_name}_wdata", "width": wdata_w},
            #     ],
            # },
        ]

    if "R" in mode:
        attributes_dict["wires"] += [
            # FIXME: Check correcct ports of asym converter
            {
                "name": f"{regarray_name}_r_asym_m_io",
                "descr": "Manager interface of R asym",
                "signals": [
                    {
                        "name": f"{regarray_name}_r_asym_m_en_o",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{regarray_name}_r_asym_m_addr_o",
                        "width": f"{REGARRAY_NAME}_INTERNAL_ADDR_W",
                        "descr": "Write address",
                    },
                    {
                        "name": f"{regarray_name}_r_asym_m_data_i",
                        "width": f"{REGARRAY_NAME}_INTERNAL_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
            {
                "name": f"{regarray_name}_r_asym_s_io",
                "descr": "Subordinate interface of R asym",
                "signals": [
                    {
                        "name": f"{regarray_name}_r_asym_s_en_i",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{regarray_name}_r_asym_s_addr_i",
                        "width": log2n_items,
                        "descr": "Read address",
                    },
                    {
                        "name": f"{regarray_name}_r_asym_s_data_o",
                        "width": n_bits,
                        "descr": "Read data",
                    },
                ],
            },
            # FIXME: Fix wires
            #######
            #######
            #######
            #######
            # {
            #     "name": f"{regarray_name}_read_io",
            #     "descr": "REGARRAY read interface.",
            #     "signals": [
            #         # FIXME: Not using verilog parameters RADDR_W and RDATA_W because csr_gen later creates a signal reference with 'n_bits' width (this throws an errror during setup if signals have different widths)
            #         # but it would be better to use verilog parameters so the core can override it if needed.
            #         {"name": f"{regarray_name}_addr", "width": raddr_w},
            #         {"name": f"{regarray_name}_rdata", "width": rdata_w},
            #     ],
            # },
        ]
    #
    # Blocks
    #
    # FIXME: Check if we need two asym converters or just one
    if "W" in mode:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_asym_converter",
                "instance_name": f"{regarray_name}_w_asym_converter",
                "instance_description": f"Write asymetric converter for REGARRAY {regarray_name}",
                "parameters": {
                    "WDATA_W": n_bits,  # width of write data
                    "RDATA_W": f"{REGARRAY_NAME}_INTERNAL_DATA_W",  # width of read data
                    "ADDR_W": f"{REGARRAY_NAME}_MAX_ADDR_W",  # width of higher address
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "write_i": f"{regarray_name}_w_asym_write_i",
                    "read_io": f"{regarray_name}_w_asym_read_io",
                },
            },
        ]
    if "R" in mode:
        attributes_dict["subblocks"] += [
            {
                "core_name": "iob_asym_converter",
                "instance_name": f"{regarray_name}_r_asym_converter",
                "instance_description": f"Read asymetric converter for REGARRAY {regarray_name}",
                "parameters": {
                    "WDATA_W": f"{REGARRAY_NAME}_INTERNAL_DATA_W",  # width of write data
                    "RDATA_W": n_bits,  # width of read data
                    "ADDR_W": f"{REGARRAY_NAME}_MAX_ADDR_W",  # width of higher address
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "write_i": f"{regarray_name}_asym_r_write_i",
                    "read_io": f"{regarray_name}_asym_r_read_io",
                },
            },
        ]
    attributes_dict["subblocks"] += [
        {
            "core_name": "iob_regarray_dp",
            "instance_name": regarray_name,
            "instance_description": f"REGARRAY {regarray_name}",
            "parameters": {
                "DATA_W": n_bits,
                "ADDR_W": log2n_items,
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "port_a_io": f"{regarray_name}_port_a_io",
                "port_b_io": f"{regarray_name}_port_b_io",
            },
        },
    ]
    #
    # Snippets
    #
    snippet = f"""
    // REGARRAY: {REGARRAY_NAME}

    // Synchronous reset unused
    assign rst = 1'b0;

    // Connect Port A to internal logic (for cbus)
    assign a_en_i = {regarray_name}_valid & {regarray_name}_ready;
    assign a_wstrb_i = {regarray_name}_wstrb;
    assign a_addr_i = {regarray_name}_addr;
    assign a_data_i = {regarray_name}_wdata;
    assign {regarray_name}_rdata = a_data_o;

    // Respond with always ready
    assign {regarray_name}_ready = 1'b1;
"""
    if mode == "R":
        snippet = f"""
    // Respond with always rvalid
    assign {regarray_name}_rvalid = 1'b1;
"""

    # FIXME: Fix snippets
    #        Check if we need two asym converters or just one (we may or may not need to mux ports).
    if mode == "RW":
        snippet = f"""
    // Mux port B between R and W asym converters
    assign b_en_i = ;
    assign b_wstrb_i = ;
    assign b_addr_i = ;
    assign b_data_i = ;
    assign ... = b_data_o;
"""
    elif mode == "W":
        snippet = f"""
    // Connect port B to W asym converter
    assign b_en_i = {regarray_name}_r_asym_w_en_i;
    assign b_wstrb_i = 'd0;
    assign b_addr_i = {regarray_name}_r_asym_w_addr_i;
    assign b_data_i = 'd0;
    assign {regarray_name}_r_asym_w_data_i = b_data_o;
"""
    #   // Write always connected to high
    #   assign {regarray_name}_w_strb = {{{REGARRAY_NAME}_W_DATA_W/8{{1'b1}}}};
    #   // Generate wen signal
    #   assign {regarray_name}_wen = {regarray_name}_valid & {regarray_name}_ready & |{regarray_name}_wstrb;
    # """
    elif mode == "R":
        snippet = f"""
    // Connect port B to R asym converter
    assign b_en_i = {regarray_name}_r_asym_r_en_i;
    assign b_wstrb_i = 'd0;
    assign b_addr_i = {regarray_name}_r_asym_r_addr_i;
    assign b_data_i = 'd0;
    assign {regarray_name}_r_asym_r_data_i = b_data_o;
"""
    #        snippet += f"""
    #   // Always ready and rvalid
    #   assign {regarray_name}_ready = 1'b1;
    #   assign {regarray_name}_rvalid = 1'b1;
    # """

    attributes_dict["snippets"].append({"verilog_code": snippet})
