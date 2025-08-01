# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "START",
                "type": "P",
                "val": "2",
                "min": "0",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "DURATION",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "WIDTH",
                "type": "D",
                "val": "$clog2(START + DURATION + 2)",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "START_INT",
                "type": "D",
                "val": "(START <= 0) ? 0 : START - 1",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "FINISH",
                "type": "D",
                "val": "START_INT + DURATION",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "start_i",
                "descr": "Input port",
                "signals": [
                    {"name": "start_i", "width": 1},
                ],
            },
            {
                "name": "pulse_o",
                "descr": "Output port",
                "signals": [
                    {"name": "pulse_o", "width": 1},
                ],
            },
        ],
        "wires": [
            {
                "name": "start_detected",
                "descr": "Start detect wire",
                "signals": [
                    {"name": "start_detected", "width": 1},
                ],
            },
            {
                "name": "start_detected_nxt",
                "descr": "Start detect next wire",
                "signals": [
                    {"name": "start_detected_nxt", "width": 1},
                ],
            },
            {
                "name": "cnt_en",
                "descr": "Counter enable signal",
                "signals": [{"name": "cnt_en"}],
            },
            {
                "name": "cnt",
                "descr": "",
                "signals": [
                    {"name": "cnt", "width": "WIDTH"},
                ],
            },
            {
                "name": "pulse_nxt",
                "descr": "",
                "signals": [
                    {"name": "pulse_nxt", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "start_detected_inst",
                "instance_description": "Detect start signal",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "start_detected_nxt",
                    "data_o": "start_detected",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "cnt0",
                "instance_description": "Counter for pulse generation",
                "parameters": {
                    "DATA_W": "WIDTH",
                    "RST_VAL": "{WIDTH{1'b0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "counter_rst_i": "start_i",
                    "counter_en_i": "cnt_en",
                    "data_o": "cnt",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "pulse_reg",
                "instance_description": "Pulse output state",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": 0,
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "pulse_nxt",
                    "data_o": "pulse_o",
                },
            },
        ],
        "superblocks": [
            {
                "core_name": "iob_pulse_gen_tester",
                "dest_dir": "tester",
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign start_detected_nxt = start_detected | start_i;
    assign cnt_en = start_detected & (cnt <= FINISH);
    assign pulse_nxt = cnt_en & (cnt < FINISH) & (cnt >= START_INT);
                """,
            },
        ],
    }

    return attributes_dict
