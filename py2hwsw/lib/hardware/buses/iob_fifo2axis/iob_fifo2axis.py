# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    # Get parameters from the dictionary
    use_tlast = py_params_dict.get("use_tlast", False)
    use_level = py_params_dict.get("use_level", False)
    use_en = py_params_dict.get("use_en", False)

    # change parameters to boolean
    if isinstance(use_tlast, str):
        use_tlast = use_tlast.lower() == "true"
    if isinstance(use_level, str):
        use_level = use_level.lower() == "true"
    if isinstance(use_en, str):
        use_en = use_en.lower() == "true"

    # Set ports based on the parameters
    ports = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "iob_clk",
                "params": "c_a_r",
            },
            "descr": "Clock, clock enable, async and sync reset",
        },
    ]
    # Use enable signal if requested
    if use_en:
        ports.append(
            {
                "name": "en_i",
                "descr": "Enable signal",
                "signals": [
                    {
                        "name": "en_i",
                        "width": 1,
                        "descr": "Enable signal",
                    },
                ],
            },
        )
    # Use len signal if tlast is requested
    if use_tlast:
        ports.append(
            {
                "name": "len_i",
                "descr": "Length signal",
                "signals": [
                    {
                        "name": "len_i",
                        "width": "AXIS_LEN_W",
                        "descr": "Length signal",
                    },
                ],
            },
        )
    # Use level signal if requested
    if use_level:
        ports.append(
            {
                "name": "level_o",
                "descr": "Level signal",
                "signals": [
                    {
                        "name": "level_o",
                        "width": 2,
                        "descr": "Level signal",
                        "isvar": True,
                    },
                ],
            },
        )
    # FIFO read interface
    ports.extend(
        [
            {
                "name": "fifo_r_io",
                "descr": "FIFO read interface",
                "signals": [
                    {
                        "name": "fifo_read_o",
                        "width": 1,
                        "descr": "FIFO read signal",
                        "isvar": True,
                    },
                    {
                        "name": "fifo_rdata_i",
                        "width": "DATA_W",
                        "descr": "FIFO read data signal",
                    },
                    {
                        "name": "fifo_empty_i",
                        "width": 1,
                        "descr": "FIFO empty signal",
                    },
                ],
            },
            {
                "name": "axis_m",
                "descr": "AXIS master interface",
                "signals": {
                    "type": "axis",
                    "DATA_W": "DATA_W",
                },
            },
        ]
    )

    if use_tlast:
        # append tlast to "params" in axis_m signals
        for port in ports:
            if port["name"] == "axis_m":
                port["signals"]["params"] = "tlast"
                break

    wires = [
        {
            "name": "data_valid",
            "descr": "Data valid register",
            "signals": [
                {
                    "name": "data_valid",
                    "width": 1,
                },
            ],
        },
        # Skid buffer
        {
            "name": "saved",
            "descr": "Saved register",
            "signals": [
                {
                    "name": "saved",
                    "width": 1,
                },
            ],
        },
        {
            "name": "saved_tdata",
            "descr": "Saved tdata register",
            "signals": [
                {
                    "name": "saved_tdata",
                    "width": "DATA_W",
                },
            ],
        },
        {
            "name": "outputs_enable",
            "descr": "Outputs enable signal",
            "signals": [
                {
                    "name": "outputs_enable",
                    "width": 1,
                    "isvar": True,
                },
            ],
        },
        {
            "name": "read_condition",
            "descr": "Read condition signal",
            "signals": [
                {
                    "name": "read_condition",
                    "width": 1,
                    "isvar": True,
                },
            ],
        },
    ]

    comb_code = """

    // Skid buffer
    // Signals if there is valid data in skid buffer
    outputs_enable = (~axis_tvalid_o) | axis_tready_i;
    saved_rst = rst_i | outputs_enable;
    saved_nxt = (data_valid & (~outputs_enable)) | saved;
    saved_tdata_en = data_valid;
    saved_tdata_nxt = fifo_rdata_i;

    // AXIS regs
    // tvalid
    axis_tvalid_o_en  = outputs_enable;
    axis_tvalid_o_nxt = saved | data_valid;
    // tdata
    axis_tdata_o_en  = outputs_enable;
    axis_tdata_o_nxt = (saved) ? saved_tdata : fifo_rdata_i;

    //FIFO read
    // read new data:
    // 1. if tready is high
    // 2. if no data is saved
    // 3. if no data is being read from fifo
    read_condition = axis_tready_i | (~axis_tvalid_o_nxt);
    """

    if use_level:
        comb_code += """
        if (saved && axis_tvalid_o) begin
            level_o = 2'd2;
        end else if (saved || axis_tvalid_o) begin
            level_o = 2'd1;
        end else begin
            level_o = 2'd0;
        end
        """

    if use_en:
        comb_code += """
        fifo_read_o    = (en_i & (~fifo_empty_i)) & read_condition;
        """
    else:
        comb_code += """
        fifo_read_o    = (~fifo_empty_i) & read_condition;
        """

    comb_code += """
    // Data valid register
    data_valid_nxt = fifo_read_o;
    """

    # Setup the module
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
        ],
        "ports": ports,
        "wires": wires,
        "comb": {
            "code": comb_code,
            # All infered registers use rst_i
            "clk_if": "c_a_r",
        },
    }

    # When using tlast, add the modcnt module and necessary logic/signals
    if use_tlast:
        attributes_dict["confs"].append(
            {
                "name": "AXIS_LEN_W",
                "descr": "AXIS length signal width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
        )

        attributes_dict["wires"].extend(
            [
                {
                    "name": "axis_word_count",
                    "descr": "AXIS word count signal",
                    "signals": [
                        {
                            "name": "axis_word_count",
                            "width": "AXIS_LEN_W",
                        },
                    ],
                },
                {
                    "name": "len_int",
                    "descr": "Length internal signal",
                    "signals": [
                        {
                            "name": "len_int",
                            "width": "AXIS_LEN_W",
                            "isvar": True,
                        },
                    ],
                },
                {
                    "name": "saved_tlast",
                    "descr": "Saved tlast register",
                    "signals": [
                        {
                            "name": "saved_tlast",
                            "width": 1,
                        },
                    ],
                },
                {
                    "name": "en_rst_i_ref",
                    "descr": "Modcnt Synchronous and Enable reset reference",
                    "signals": [
                        {
                            "name": "rst_i",
                        },
                        {
                            "name": "fifo_read_o",
                        },
                    ],
                },
            ],
        )

        attributes_dict["comb"][
            "code"
        ] += """
        // tlast
        len_int = len_i - 1;
        saved_tlast_en = data_valid;
        saved_tlast_nxt = axis_word_count == len_int;
        axis_tlast_o_en  = outputs_enable;
        axis_tlast_o_nxt = (saved) ? saved_tlast : saved_tlast_nxt;
        """

        attributes_dict["subblocks"] = [
            {
                "core_name": "iob_modcnt",
                "instance_name": "word_count_inst",
                "instance_description": "tdata word count",
                "parameters": {
                    "DATA_W": "AXIS_LEN_W",
                    "RST_VAL": """{AXIS_LEN_W{1'b1}}""",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "en_rst_i": "en_rst_i_ref",
                    "mod_i": "len_int",
                    "data_o": "axis_word_count",
                },
            },
        ]

    return attributes_dict
