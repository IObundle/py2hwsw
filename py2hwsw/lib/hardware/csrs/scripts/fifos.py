import copy

fifo_csrs = {
    "name": "fifo_csrs",
    "descr": "FIFO control and status registers",
    "regs": [
        {
            "name": "data",
            "type": "RW",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Read/write data from/to FIFO.",
        },
        {
            "name": "thresh",
            "type": "W",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Interrupt upper level threshold: an interrupt is triggered when the number of words in the FIFO reaches this upper level threshold.",
        },
        {
            "name": "empty",
            "type": "R",
            "n_bits": 1,
            "rst_val": 1,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Empty (1) or non-empty (0).",
        },
        {
            "name": "full",
            "type": "R",
            "n_bits": 1,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Full (1), or non-full (0).",
        },
        {
            "name": "level",
            "type": "R",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Number of words in FIFO.",
        },
    ],
}


def append_fifos_csrs(csrs_obj_list, fifo_names_list):
    """Given a list of fifo names, append a copy of the standard FIFO CSRs for each one"""
    for fifo_name in fifo_names_list:
        local_fifo_csrs = copy.deepcopy(fifo_csrs)
        local_fifo_csrs["name"] = fifo_name + "_" + fifo_csrs["name"]
        for reg in local_fifo_csrs["regs"]:
            reg["name"] = fifo_name + "_" + reg["name"]
        csrs_obj_list.append(local_fifo_csrs)


def create_fifos_instances(attributes_dict, sync_fifos, async_fifos):
    """Given lists of names for fifos, the ports, wires and blocks for them"""

    for fifo_name in sync_fifos:
        #
        # Confs: Copied from iob_fifo_sync.py
        #
        # Needed to define widths of FIFO ports based on verilog parameters
        attributes_dict["confs"] += [
            {
                "name": f"{fifo_name}_W_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_R_DATA_W",
                "descr": "",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_ADDR_W",
                "descr": "Higher ADDR_W lower DATA_W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_MAXDATA_W",
                "descr": "",
                "type": "F",
                "val": f"iob_max({fifo_name}_W_DATA_W, {fifo_name}_R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_MINDATA_W",
                "descr": "",
                "type": "F",
                "val": f"iob_min({fifo_name}_W_DATA_W, {fifo_name}_R_DATA_W)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_R",
                "descr": "",
                "type": "F",
                "val": f"{fifo_name}_MAXDATA_W / {fifo_name}_MINDATA_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_MINADDR_W",
                "descr": "Lower ADDR_W (higher DATA_W)",
                "type": "F",
                "val": f"{fifo_name}_ADDR_W - $clog2({fifo_name}_R)",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_W_ADDR_W",
                "descr": "",
                "type": "F",
                "val": f"({fifo_name}_W_DATA_W == {fifo_name}_MAXDATA_W) ? {fifo_name}_MINADDR_W : {fifo_name}_ADDR_W",
                "min": "NA",
                "max": "NA",
            },
            {
                "name": f"{fifo_name}_R_ADDR_W",
                "descr": "",
                "type": "F",
                "val": f"({fifo_name}_R_DATA_W == {fifo_name}_MAXDATA_W) ? {fifo_name}_MINADDR_W : {fifo_name}_ADDR_W",
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
                        "width": f"{fifo_name}_W_DATA_W",
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
                        "width": f"{fifo_name}_R_DATA_W",
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
                        "width": f"{fifo_name}_R",
                        "descr": "Memory write enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_addr",
                        "direction": "output",
                        "width": f"{fifo_name}_MINADDR_W",
                        "descr": "Memory write address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_w_data",
                        "direction": "output",
                        "width": f"{fifo_name}_MAXDATA_W",
                        "descr": "Memory write data",
                    },
                    #  Read port
                    {
                        "name": f"{fifo_name}_ext_mem_r_en",
                        "direction": "output",
                        "width": f"{fifo_name}_R",
                        "descr": "Memory read enable",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_addr",
                        "direction": "output",
                        "width": f"{fifo_name}_MINADDR_W",
                        "descr": "Memory read address",
                    },
                    {
                        "name": f"{fifo_name}_ext_mem_r_data",
                        "direction": "input",
                        "width": f"{fifo_name}_MAXDATA_W",
                        "descr": "Memory read data",
                    },
                ],
            },
            {
                "name": f"{fifo_name}_fifo",
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
                        "width": f"{fifo_name}_W_DATA_W",
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
                "core_name": "iob_fifo_sync",
                "instance_name": fifo_name,
                "connect": {
                    "clk_en_rst": "clk_en_rst",
                    "rst": f"{fifo_name}_rst",
                    "write": f"{fifo_name}_write_int",
                    "read": f"{fifo_name}_read_int",
                    "extmem": f"{fifo_name}_extmem",
                    "fifo": f"{fifo_name}_fifo",
                },
            },
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
