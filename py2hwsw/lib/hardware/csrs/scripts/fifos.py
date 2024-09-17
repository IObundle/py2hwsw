def get_fifo_csrs(csr_ref):
    fifo_csrs = []
    if csr_ref["type"].endswith("FIFO_R"):
        fifo_csrs += [
            {
                "name": f"{csr_ref['name']}_data",
                "type": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": False,
                "descr": "Read data from FIFO.",
                "internal_use": True,
            },
            {
                "name": f"{csr_ref['name']}_empty",
                "type": "R",
                "n_bits": 1,
                "rst_val": 1,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Empty (1) or non-empty (0).",
                "internal_use": True,
            },
            {
                "name": f"{csr_ref['name']}_thresh",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Interrupt upper level threshold: an interrupt is triggered when the number of words in the FIFO reaches this upper level threshold.",
                "internal_use": True,
            },
        ]
    else:  # FIFO_W
        fifo_csrs += [
            {
                "name": f"{csr_ref['name']}_data",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Write data to FIFO.",
                "internal_use": True,
            },
            {
                "name": f"{csr_ref['name']}_full",
                "type": "R",
                "n_bits": 1,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Full (1), or non-full (0).",
                "internal_use": True,
            },
        ]
    fifo_csrs += [
        {
            "name": f"{csr_ref['name']}_level",
            "type": "R",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Number of words in FIFO.",
            "internal_use": True,
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
    csr_ref = None
    for csr_group in csrs_dict:
        for csr in csr_group["regs"]:
            if csr["type"] in ["FIFO_R", "FIFO_W", "AFIFO_R", "AFIFO_W"]:
                csr_group_ref = csr_group
                csr_ref = csr
                break
        if csr_ref:
            break

    if not csr_ref:
        return

    # Add fifo_csrs to group
    csr_group_ref["regs"] += get_fifo_csrs(csr_ref)

    # Remove original csr from csr_group
    csr_group_ref["regs"].remove(csr_ref)

    if csr["type"].startswith("AFIFO"):
        create_async_fifo_instance(attributes_dict, csr_ref)
    else:
        create_sync_fifo_instance(attributes_dict, csr_ref)


def create_sync_fifo_instance(attributes_dict, csr_ref):
    """Add fifo instance, wires and ports to given attributes_dict, based on fifo description provided by CSR.
    :param dict attributes_dict: Dictionary of core attributes to add fifo instance, wires and ports.
    :param dict csr_ref: CSR description dictionary, with FIFO information.
    """
    fifo_name = csr_ref["name"]
    FIFO_NAME = fifo_name.upper()
    fifo_type = "R" if csr_ref["type"].endswith("FIFO_R") else "W"

    #
    # Confs: Based on confs from iob_fifo_sync.py
    #
    # Needed to define widths of FIFO ports based on verilog parameters
    attributes_dict["confs"] += [
        {
            "name": f"{FIFO_NAME}_W_DATA_W",
            "descr": "",
            "type": "P",
            "val": 32 if fifo_type == "W" else csr_ref["n_bits"],
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_R_DATA_W",
            "descr": "",
            "type": "P",
            "val": 32 if fifo_type == "R" else csr_ref["n_bits"],
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_ADDR_W",
            "descr": "Higher ADDR_W lower DATA_W",
            "type": "P",
            "val": csr_ref["log2n_items"],
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_MAXDATA_W",
            "descr": "",
            "type": "F",
            "val": f"iob_max({FIFO_NAME}_W_DATA_W, {FIFO_NAME}_R_DATA_W)",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_MINDATA_W",
            "descr": "",
            "type": "F",
            "val": f"iob_min({FIFO_NAME}_W_DATA_W, {FIFO_NAME}_R_DATA_W)",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_R",
            "descr": "",
            "type": "F",
            "val": f"{FIFO_NAME}_MAXDATA_W / {FIFO_NAME}_MINDATA_W",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_MINADDR_W",
            "descr": "Lower ADDR_W (higher DATA_W)",
            "type": "F",
            "val": f"{FIFO_NAME}_ADDR_W - $clog2({FIFO_NAME}_R)",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_W_ADDR_W",
            "descr": "",
            "type": "F",
            "val": f"({FIFO_NAME}_W_DATA_W == {FIFO_NAME}_MAXDATA_W) ? {FIFO_NAME}_MINADDR_W : {FIFO_NAME}_ADDR_W",
            "min": "NA",
            "max": "NA",
        },
        {
            "name": f"{FIFO_NAME}_R_ADDR_W",
            "descr": "",
            "type": "F",
            "val": f"({FIFO_NAME}_R_DATA_W == {FIFO_NAME}_MAXDATA_W) ? {FIFO_NAME}_MINADDR_W : {FIFO_NAME}_ADDR_W",
            "min": "NA",
            "max": "NA",
        },
    ]
    #
    # Ports
    #
    attributes_dict["ports"] += [
        {
            "name": f"{fifo_name}_rst",
            "descr": "Synchronous reset interface.",
            "signals": [
                {
                    "name": f"{fifo_name}_rst",
                    "direction": "input",
                    "width": 1,
                    "descr": "Synchronous reset input",
                },
            ],
        },
    ]
    if fifo_type == "R":
        attributes_dict["ports"] += [
            {
                "name": f"{fifo_name}_write",
                "descr": "FIFO write interface.",
                "signals": [
                    {
                        "name": f"{fifo_name}_w_en",
                        "direction": "input",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{fifo_name}_w_data",
                        "direction": "input",
                        "width": f"{FIFO_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                    {
                        "name": f"{fifo_name}_w_full",
                        "direction": "output",
                        "width": 1,
                        "descr": "Write full signal",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_interrupt",
                "descr": "Connects directly to FIFO",
                "signals": [
                    {
                        "name": f"{fifo_name}_interrupt",
                        "direction": "output",
                        "width": 1,
                        "descr": "FIFO interrupt. Active when level reaches threshold.",
                    },
                ],
            },
        ]
    else:  # fifo_type == "W"
        attributes_dict["ports"].append(
            {
                "name": f"{fifo_name}_read",
                "descr": "FIFO read interface.",
                "signals": [
                    {
                        "name": f"{fifo_name}_r_en",
                        "direction": "input",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{fifo_name}_r_data",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_R_DATA_W",
                        "descr": "Read data",
                    },
                    {
                        "name": f"{fifo_name}_r_empty",
                        "direction": "output",
                        "width": 1,
                        "descr": "Read empty signal",
                    },
                ],
            }
        )
    attributes_dict["ports"] += [
        {
            "name": f"{fifo_name}_extmem",
            "descr": "FIFO external memory interface.",
            "signals": [
                {
                    "name": f"{fifo_name}_ext_mem_clk",
                    "direction": "output",
                    "width": 1,
                },
                {
                    "name": f"{fifo_name}_ext_mem_w_en",
                    "direction": "output",
                    "width": f"{FIFO_NAME}_R",
                    "descr": "Memory write enable",
                },
                {
                    "name": f"{fifo_name}_ext_mem_w_addr",
                    "direction": "output",
                    "width": f"{FIFO_NAME}_MINADDR_W",
                    "descr": "Memory write address",
                },
                {
                    "name": f"{fifo_name}_ext_mem_w_data",
                    "direction": "output",
                    "width": f"{FIFO_NAME}_MAXDATA_W",
                    "descr": "Memory write data",
                },
                #  Read port
                {
                    "name": f"{fifo_name}_ext_mem_r_en",
                    "direction": "output",
                    "width": f"{FIFO_NAME}_R",
                    "descr": "Memory read enable",
                },
                {
                    "name": f"{fifo_name}_ext_mem_r_addr",
                    "direction": "output",
                    "width": f"{FIFO_NAME}_MINADDR_W",
                    "descr": "Memory read address",
                },
                {
                    "name": f"{fifo_name}_ext_mem_r_data",
                    "direction": "input",
                    "width": f"{FIFO_NAME}_MAXDATA_W",
                    "descr": "Memory read data",
                },
            ],
        },
        {
            "name": f"{fifo_name}_current_level",
            "descr": "Connects directly to FIFO",
            "signals": [
                {
                    "name": f"{fifo_name}_current_level",
                    "direction": "output",
                    "width": "ADDR_W+1",
                    "descr": "FIFO level",
                },
            ],
        },
    ]
    #
    # Wires
    #
    attributes_dict["wires"] += []
    if fifo_type == "W":
        attributes_dict["wires"].append(
            {
                "name": f"{fifo_name}_write",
                "descr": "FIFO write interface.",
                "signals": [
                    {"name": f"{fifo_name}_data_wen", "width": 1},
                    {"name": f"{fifo_name}_data", "width": 32},
                    {"name": f"{fifo_name}_full", "width": 1},
                ],
            }
        )
    else:  # fifo_type == "R"
        attributes_dict["wires"].append(
            {
                "name": f"{fifo_name}_read",
                "descr": "FIFO read interface.",
                "signals": [
                    {"name": f"{fifo_name}_data_ren", "width": 1},
                    {"name": f"{fifo_name}_data_rdata", "width": 32},
                    {"name": f"{fifo_name}_empty", "width": 1},
                ],
            }
        )
    #
    # Blocks
    #
    attributes_dict["blocks"] += [
        {
            "core_name": "iob_fifo_sync",
            "instance_name": fifo_name,
            "instance_description": f"Synchronous FIFO {fifo_name}",
            "parameters": {
                "W_DATA_W": f"{FIFO_NAME}_W_DATA_W",
                "R_DATA_W": f"{FIFO_NAME}_R_DATA_W",
                "ADDR_W": f"{FIFO_NAME}_ADDR_W",
            },
            "connect": {
                "clk_en_rst": "clk_en_rst",
                "rst": f"{fifo_name}_rst",
                "write": f"{fifo_name}_write",
                "read": f"{fifo_name}_read",
                "extmem": f"{fifo_name}_extmem",
                "fifo": f"{fifo_name}_current_level",
            },
        },
        {
            "core_name": "iob_functions",
            "instantiate": False,
        },
    ]
    #
    # Snippets
    #

    attributes_dict["snippets"].append(
        {
            "verilog_code": f"""
   // Include iob_functions for use in parameters
   `include "iob_functions.vs"

   // Connect FIFO level status to CSRs
   assign {fifo_name}_level = {fifo_name}_current_level_o;
   // Generate interrupt signal
   assign {fifo_name}_interrupt_o ={fifo_name}_current_level_o >= {fifo_name}_thresh;

   assign {fifo_name}_data_rvalid = 1'b1;
   assign {fifo_name}_data_rready = 1'b1;
""",
        }
    )


def create_async_fifo_instance(attributes_dict, async_fifos):
    """Given lists of names for fifos, the ports, wires and blocks for them"""

    for fifo_name in async_fifos:
        FIFO_NAME = fifo_name.upper()
        #
        # Confs: Copied from iob_fifo_async.py
        #
        # Needed to define widths of FIFO ports based on verilog parameters
        attributes_dict["confs"] += [
            {
                "name": f"{FIFO_NAME}_W_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_R_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_ADDR_W",
                "descr": "Higher ADDR_W lower DATA_W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_MAXDATA_W",
                "descr": "",
                "type": "F",
                "val": f"iob_max({FIFO_NAME}_W_DATA_W, {FIFO_NAME}_R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_MINDATA_W",
                "descr": "",
                "type": "F",
                "val": f"iob_min({FIFO_NAME}_W_DATA_W, {FIFO_NAME}_R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_R",
                "descr": "",
                "type": "F",
                "val": f"{FIFO_NAME}_MAXDATA_W / {FIFO_NAME}_MINDATA_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_MINADDR_W",
                "descr": "Lower ADDR_W (higher DATA_W)",
                "type": "F",
                "val": f"{FIFO_NAME}_ADDR_W - $clog2({FIFO_NAME}_R)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_W_ADDR_W",
                "descr": "",
                "type": "F",
                "val": f"({FIFO_NAME}_W_DATA_W == {FIFO_NAME}_MAXDATA_W) ? {FIFO_NAME}_MINADDR_W : {FIFO_NAME}_ADDR_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{FIFO_NAME}_R_ADDR_W",
                "descr": "",
                "type": "F",
                "val": f"({FIFO_NAME}_R_DATA_W == {FIFO_NAME}_MAXDATA_W) ? {FIFO_NAME}_MINADDR_W : {FIFO_NAME}_ADDR_W",
                "min": "NA",
                "max": "NA",
            },
        ]
        #
        # Ports
        #
        attributes_dict["ports"] += [
            {
                "name": f"{fifo_name}_rst",
                "descr": "Synchronous reset interface. Connects directly to FIFO.",
                "signals": [
                    {
                        "name": f"{fifo_name}_rst",
                        "direction": "input",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_write",
                "descr": "FIFO write interface. Some signals are muxed with CSRs.",
                "signals": [
                    {
                        "name": f"{fifo_name}_w_en",
                        "direction": "input",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{fifo_name}_w_data",
                        "direction": "input",
                        "width": f"{FIFO_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                    {
                        "name": f"{fifo_name}_w_full",
                        "direction": "output",
                        "width": 1,
                        "descr": "Write full signal",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_read",
                "descr": "FIFO read interface. Some signals are muxed with CSRs.",
                "signals": [
                    {
                        "name": f"{fifo_name}_r_en",
                        "direction": "input",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{fifo_name}_r_data",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_R_DATA_W",
                        "descr": "Read data",
                    },
                    {
                        "name": f"{fifo_name}_r_empty",
                        "direction": "output",
                        "width": 1,
                        "descr": "Read empty signal",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_extmem",
                "descr": "External memory interface. Connects directly to FIFO",
                "signals": [
                    {
                        "name": f"{fifo_name}_ext_mem_clk",
                        "direction": "output",
                        "width": 1,
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_en",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_addr",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_data",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": f"{fifo_name}_ext_mem_r_en",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_addr",
                        "direction": "output",
                        "width": f"{FIFO_NAME}_MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_data",
                        "direction": "input",
                        "width": f"{FIFO_NAME}_MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_level",
                "descr": "Connects directly to FIFO",
                "signals": [
                    {
                        "name": f"{fifo_name}_level",
                        "direction": "output",
                        "width": "ADDR_W+1",
                        "descr": "FIFO level",
                    },
                ],
            },
        ]
        #
        # Wires
        #
        attributes_dict["wires"] += [
            {
                "name": f"{fifo_name}_write_int",
                "descr": "Connects directly to FIFO write port",
                "signals": [
                    {
                        "name": f"{fifo_name}_w_en_int",
                        "direction": "input",
                        "width": 1,
                        "descr": "Write enable",
                    },
                    {
                        "name": f"{fifo_name}_w_data_int",
                        "direction": "input",
                        "width": f"{FIFO_NAME}_W_DATA_W",
                        "descr": "Write data",
                    },
                    {
                        "name": f"{fifo_name}_w_full",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_read_int",
                "descr": "Connects directly to FIFO read port",
                "signals": [
                    {
                        "name": f"{fifo_name}_r_en_int",
                        "direction": "input",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": f"{fifo_name}_r_data",
                    },
                    {
                        "name": f"{fifo_name}_r_empty",
                    },
                ],
            },
        ]
        #
        # Blocks
        #
        attributes_dict["blocks"].append(
            {
                "core_name": "iob_fifo_async",
                "instance_name": fifo_name,
                "connect": {
                    "clk_en_rst": "clk_en_rst",
                    "rst": f"{fifo_name}_rst",
                    "write": f"{fifo_name}_write_int",
                    "read": f"{fifo_name}_read_int",
                    "extmem": f"{fifo_name}_extmem",
                    "fifo": f"{fifo_name}_level",
                },
            }
        )
        #
        # Snippets
        #
        attributes_dict["snippets"].append(
            {
                "verilog_code": f"""
    // Mux FIFO read port from logic and csr
    assign {fifo_name}_r_en_int = {fifo_name}_data_rd_ren | {fifo_name}_r_en;
    assign {fifo_name}_data_rd = {fifo_name}_r_data;

    // Mux FIFO write port from logic and csr
    assign {fifo_name}_w_en_int = {fifo_name}_data_wr_wen | {fifo_name}_w_en;
    assign {fifo_name}_w_data = {fifo_name}_data_wr_wen ? {fifo_name}_data_wr : {fifo_name}_w_data;

    // Connect FIFO status outputs to CSRs
    assign {fifo_name}_full_rd = {fifo_name}_w_full;
    assign {fifo_name}_empty_rd = {fifo_name}_r_empty;
    assign {fifo_name}_level_rd = {fifo_name}_level;
""",
            }
        )
