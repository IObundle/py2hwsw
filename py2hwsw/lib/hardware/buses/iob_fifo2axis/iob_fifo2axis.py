# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    use_tlast = py_params_dict.get("use_tlast", False)
    use_level = py_params_dict.get("use_level", False)
    use_en = py_params_dict.get("use_en", False)

    # Set ports based on the parameters
    ports = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "iob_clk",
            },
            "descr": "Clock, clock enable, and reset",
        },
        {
            "name": "rst_i",
            "descr": "Reset signal",
            "signals": [
                {
                    "name": "rst_i",
                    "width": 1,
                    "descr": "Reset signal",
                },
            ],
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
    ports.append(
        {
            "name": "fifo_r_io",
            "descr": "FIFO read interface",
            "signals": [
                {
                    "name": "fifo_read_o",
                    "width": 1,
                    "descr": "FIFO read signal",
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
    )
    # AXIS master interface
    if use_tlast:
        ports.append(
            {
                "name": "axis_m",
                "descr": "AXIS master interface",
                "signals": {
                    "type": "axis",
                    "params": "tlast",
                    "DATA_W": "DATA_W",
                },
            },
        )
    else:
        ports.append(
            {
                "name": "axis_m",
                "descr": "AXIS master interface",
                "signals": {
                    "type": "axis",
                    "DATA_W": "DATA_W",
                },
            },
        )

    wires = [
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
    ]

    # Setup snippets based on the parameters
    snippets = [
        {
            "verilog_code": """
    wire                  read_condition;
    wire                  fifo_read_r;
    wire                  output_en;
    wire [DATA_W-1:0] saved_tdata;
    wire [(DATA_W+2)-1:0] output_nxt;
    wire [(DATA_W+2)-1:0] output_r;

    wire [AXIS_LEN_W-1:0] axis_word_count;
    wire                  axis_tlast_nxt;
    wire [AXIS_LEN_W-1:0] len_int;
    wire saved_tlast;

    iob_reg_cear_r #(
        .DATA_W (1),
        .RST_VAL(1'd0)
    ) fifo_read_reg (
        `include "iob_fifo2axis_iob_clk_s_s_portmap.vs"
        .rst_i (rst_i),
        .data_i(fifo_read_o),
        .data_o(fifo_read_r)
    );

    //FIFO tlast
    iob_reg_cear_re #(
        .DATA_W (1),
        .RST_VAL(1'd0)
    ) axis_tlast_reg (
        `include "iob_fifo2axis_iob_clk_s_s_portmap.vs"
        .rst_i (rst_i),
        .en_i  (fifo_read_r),
        .data_i(axis_tlast_nxt),
        .data_o(saved_tlast)
    );

    //tdata word count
    iob_modcnt #(
        .DATA_W (AXIS_LEN_W),
        .RST_VAL({AXIS_LEN_W{1'b1}})  // go to 0 after first enable
    ) word_count_inst (
        `include "iob_fifo2axis_iob_clk_s_s_portmap.vs"
        .rst_i (rst_i),
        .en_i  (fifo_read_o),
        .mod_i (len_int),
        .data_o(axis_word_count)
    );

    //tdata register
    iob_reg_cear_re #(
        .DATA_W (DATA_W),
        .RST_VAL({DATA_W{1'd0}})
    ) axis_tdata_reg (
        `include "iob_fifo2axis_iob_clk_s_s_portmap.vs"
        .rst_i (rst_i),
        .en_i  (fifo_read_r),
        .data_i(fifo_rdata_i),
        .data_o(saved_tdata)
    );

    // register valid + data + last
    iob_reg_cear_re #(
        .DATA_W (DATA_W + 2),
        .RST_VAL({(DATA_W + 2) {1'd0}})
    ) output_reg (
        `include "iob_fifo2axis_iob_clk_s_s_portmap.vs"
        .rst_i (rst_i),
        .en_i  (output_en),
        .data_i(output_nxt),
        .data_o(output_r)
    );

    // axis outputs
    assign axis_tvalid_o = output_r[DATA_W+1];
    assign axis_tdata_o  = output_r[1+:DATA_W];
    assign axis_tlast_o  = output_r[0];

    // tlast logic
    assign len_int        = len_i - 1;
    assign axis_tlast_nxt = (axis_word_count == len_int);

    //FIFO read
    // read new data:
    // 1. if tready is high
    // 2. if no data is saved
    // 3. if no data is being read from fifo
    assign read_condition = axis_tready_i | (~(saved | fifo_read_r));
    assign fifo_read_o    = (en_i & (~fifo_empty_i)) & read_condition;

    // Skid buffer
    assign output_nxt[DATA_W+1]  = (saved) ? 1'b1 : fifo_read_r;
    assign output_nxt[1+:DATA_W] = (saved) ? saved_tdata : fifo_rdata_i;
    assign output_nxt[0]         = (saved) ? saved_tlast : axis_tlast_nxt;
    assign output_en             = (~axis_tvalid_o) | axis_tready_i;

    """
        },
    ]

    comb_code = """
    // Skid buffer
    // Signals if there is valid data in skid buffer
    saved_nxt = (fifo_read_r & (~output_en)) | saved;
    saved_rst = (rst_i | output_en);
    """

    if use_level:
        comb_code += """
            if (saved && axis_tvalid_o) begin
                level_o = 2'd2;
            end else if (saved || axis_tvalid_o) begin
                level_o = 2'd1;
            end else begin
                level_o = 2'd0;
            end"""

    # Setup the module
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "0",
                "min": "1",
                "max": "NA",
            },
            {
                "name": "AXIS_LEN_W",
                "descr": "AXIS length bus width",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
            },
        ],
        "ports": ports,
        "wires": wires,
        "snippets": snippets,
        "comb": {
            "code": comb_code,
        },
    }

    # If using level, add the level output

    return attributes_dict
