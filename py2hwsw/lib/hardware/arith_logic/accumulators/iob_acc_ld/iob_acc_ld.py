def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_acc_ld",
        "name": "iob_acc_ld",
        "version": "0.1",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "RST_VAL",
                "type": "P",
                "val": "{DATA_W{1'b0}}",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "interface": {
                    "type": "clk_en_rst",
                    "subtype": "slave",
                },
                "descr": "clock, clock enable and reset",
            },
            {
                "name": "en_rst_i",
                "descr": "Enable and Synchronous reset interface",
                "signals": [
                    {
                        "name": "en",
                        "direction": "input",
                        "width": 1,
                        "descr": "Enable input",
                    },
                    {
                        "name": "rst",
                        "direction": "input",
                        "width": 1,
                        "descr": "Synchronous reset input",
                    },
                ],
            },
            {
                "name": "ld_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "ld",
                        "width": 1,
                        "direction": "input",
                    },
                ],
            },
            {
                "name": "ld_val_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "ld_val",
                        "width": "DATA_W",
                        "direction": "input",
                    },
                ],
            },
            {
                "name": "incr_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "incr",
                        "width": "DATA_W",
                        "direction": "input",
                    },
                ],
            },
            {
                "name": "data_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "data",
                        "width": "DATA_W",
                        "direction": "output",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "data_nxt",
                "descr": "Sum result",
                "signals": [
                    {
                        "name": "data_nxt",
                        "width": "DATA_W+1",
                    },
                ],
            },
            {
                "name": "data_int",
                "descr": "data_int wire",
                "signals": [
                    {"name": "data_int", "width": "DATA_W+1"},
                ],
            },
        ],
        "blocks": [
            {
                "core_name": "iob_reg_re",
                "instance_name": "reg0",
                "parameters": {
                    "DATA_W": "DATA_W+1",
                    "RST_VAL": "RST_VAL",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "en_rst_i": "en_rst_i",
                    "data_i": "data_nxt",
                    "data_o": "data_int",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign data_nxt = ld_i ? ld_val_i : data_o + incr_i;
            assign data_o = data_int[DATA_W-1:0];
            """,
            },
        ],
    }

    return attributes_dict
