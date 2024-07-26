def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_2to1mux",
        "name": "iob_2to1mux",
        "version": "0.1",
        "confs": [
            {
                "name": "W",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
                "descr": "IO width",
            },
        ],
        "ports": [
            {
                "name": "data_i",
                "descr": "Input port",
                "signals": [
                    {"name": "a", "width": "W", "direction": "input"},
                    {"name": "b", "width": "W", "direction": "input"},
                    {"name": "sel", "width": "1", "direction": "input"},
                ],
            },
            {
                "name": "y",
                "descr": "Output port",
                "signals": [
                    {"name": "y", "width": "W", "direction": "output"},
                ],
            },
        ],
        "combs": [
            {
                "verilog_code": """if (sel_i)
                    y_o = b_i;
                else
                    y_o = a_i;
                """,
            }
        ],
    }

    return attributes_dict
