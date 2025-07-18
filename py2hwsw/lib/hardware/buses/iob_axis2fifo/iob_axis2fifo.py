# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    # Get parameters from the dictionary
    use_tlast = py_params_dict.get("use_tlast", False)
    use_en = py_params_dict.get("use_en", False)

    # change parameters to boolean
    if isinstance(use_tlast, str):
        use_tlast = use_tlast.lower() == "true"
    if isinstance(use_en, str):
        use_en = use_en.lower() == "true"

    confs = [
        {
            "name": "DATA_W",
            "descr": "Data bus width",
            "type": "P",
            "val": "32",
            "min": "1",
            "max": "32",
        },
    ]

    if use_tlast:
        confs.append(
            {
                "name": "AXIS_LEN_W",
                "descr": "AXIS length width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
        )

    # Set ports based on the parameters
    ports = [
        {
            "name": "clk_en_rst_s",
            "wires": {
                "type": "iob_clk",
                "params": "c_a_r",
            },
            "descr": "Clock, clock enable, async and sync reset",
        },
    ]
    # Use enable wire if requested
    if use_en:
        ports.append(
            {
                "name": "en_i",
                "descr": "Enable wire",
                "wires": [{"name": "en_i", "descr": "Enable wire"}],
            },
        )
    # Use len and done wire if tlast is requested
    if use_tlast:
        ports.append(
            {
                "name": "len_o",
                "descr": "Length wire",
                "wires": [
                    {
                        "name": "len_o",
                        "width": "AXIS_LEN_W",
                        "descr": "Length wire",
                    },
                ],
            },
        )
        ports.append(
            {
                "name": "done_o",
                "descr": "Done wire",
                "wires": [{"name": "done_o", "descr": "Done wire"}],
            },
        )

    # AXIS Interface - without last
    ports.append(
        {
            "name": "axis_s",
            "descr": "AXIS slave interface",
            "wires": {"type": "axis", "DATA_W": "DATA_W"},
        }
    )
    # FIFO write interface
    ports.append(
        {
            "name": "fifo_w_io",
            "descr": "FIFO write interface",
            "wires": [
                {"name": "fifo_write_o", "isvar": True},
                {"name": "fifo_wdata_o", "width": "DATA_W", "isvar": True},
                {"name": "fifo_full_i"},
            ],
        }
    )

    if use_tlast:
        # append tlast to "params" in axis_s wires
        for port in ports:
            if port["name"] == "axis_s":
                port["wires"]["params"] = "tlast"
                break

    # Buses declaration
    buses = [
        {
            "name": "axis_tdata",
            "descr": "AXIS tdata register",
            "wires": [
                {
                    "name": "axis_tdata",
                    "width": "DATA_W",
                    "descr": "AXIS tdata register",
                },
            ],
        },
        {
            "name": "axis_tvalid",
            "descr": "AXIS tvalid register",
            "wires": [{"name": "axis_tvalid", "descr": "AXIS tvalid register"}],
        },
    ]

    if use_tlast:
        buses.extend(
            [
                {
                    "name": "axis_tlast",
                    "descr": "AXIS tlast register",
                    "wires": [{"name": "axis_tlast", "descr": "AXIS tlast register"}],
                },
                {
                    "name": "axis_word_count_inc",
                    "descr": "AXIS word count increment",
                    "wires": [
                        {
                            "name": "axis_word_count_inc",
                            "descr": "AXIS word count increment",
                            "isvar": True,
                        }
                    ],
                },
                {
                    "name": "axis_tlast_int",
                    "descr": "AXIS tlast internal wire",
                    "wires": [
                        {
                            "name": "axis_tlast_int",
                            "descr": "AXIS tlast internal wire",
                            "isvar": True,
                        }
                    ],
                },
            ]
        )

    if use_en:
        buses.append(
            {
                "name": "en_input_regs",
                "descr": "Enable wire for input registers",
                "wires": [{"name": "en_input_regs", "isvar": True}],
            },
        )

    # Combinational logic
    if use_en:
        comb_code = """
        // tready register
        axis_tready_o_nxt = (~fifo_full_i) & en_i;

        en_input_regs = axis_tready_o & en_i;
        axis_tvalid_en = en_input_regs;
        axis_tdata_en = en_input_regs;
        """
        if use_tlast:
            comb_code += """
                axis_tlast_en = en_input_regs;
            """
    else:
        comb_code = """
        // tready register
        axis_tready_o_nxt = ~fifo_full_i;

        axis_tvalid_en = axis_tready_o;
        axis_tdata_en = axis_tready_o;
        """
        if use_tlast:
            comb_code += """
                axis_tlast_en = axis_tready_o;
            """

    comb_code += """
    // tvalid register
    axis_tvalid_nxt = axis_tvalid_i;

    // tdata register
    axis_tdata_nxt = axis_tdata_i;

     // Skid buffer mux
    if (axis_tready_o) begin
        fifo_wdata_o = axis_tdata_i;
        fifo_write_o = axis_tvalid_i & axis_tready_o;
    end else begin
        fifo_wdata_o = axis_tdata;
        fifo_write_o = axis_tvalid & axis_tready_o_nxt;
    end
    """

    if use_tlast:
        comb_code += """
        // tlast register
        axis_tlast_nxt = axis_tlast_i & axis_tvalid_i;
        if (axis_tready_o) begin
            axis_tlast_int = axis_tlast_i;
        end else begin
            axis_tlast_int = axis_tlast;
        end

        axis_word_count_inc = fifo_write_o & (~done_o);
    """

    attributes_dict = {
        "generate_hw": True,
        "confs": confs,
        "ports": ports,
        "buses": buses,
        "comb": {
            "code": comb_code,
            "clk_if": "c_a_r",
        },
    }

    if use_tlast:
        attributes_dict["buses"].extend(
            [
                {
                    "name": "clk_en_arst",
                    "descr": "Clock, clock enable and async reset",
                    "wires": [
                        {"name": "clk_i"},
                        {"name": "cke_i"},
                        {"name": "arst_i"},
                    ],
                },
                {
                    "name": "counter_en_rst",
                    "descr": "Counter enable and reset",
                    "wires": [{"name": "axis_word_count_inc"}, {"name": "rst_i"}],
                },
                {
                    "name": "rst_i",
                    "descr": "Reset wire",
                    "wires": [
                        {"name": "rst_i"},
                    ],
                },
            ]
        )

        attributes_dict["subblocks"] = [
            {
                "core_name": "iob_counter",
                "instance_name": "word_count_inst",
                "instance_description": "Word counter",
                "parameters": {
                    "DATA_W": "AXIS_LEN_W",
                    "RST_VAL": """{AXIS_LEN_W{1'b0}}""",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_arst",
                    "en_rst_i": "counter_en_rst",
                    "data_o": "len_o",
                },
            },
            {
                "core_name": "iob_edge_detect",
                "instance_name": "tlast_detect_inst",
                "instance_description": "tlast detection",
                "parameters": {
                    "EDGE_TYPE": '"rising"',
                    "OUT_TYPE": '"step"',
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_arst",
                    "rst_i": "rst_i",
                    "bit_i": "axis_tlast_int",
                    "detected_o": "done_o",
                },
            },
        ]

    return attributes_dict
