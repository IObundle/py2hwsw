# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": "iob_rom_acc",
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "VALUES_DATA_W",
                "type": "P",
                "val": 8,
                "min": 1,
                "max": "NA",
                "descr": "Data width",
            },
            {
                "name": "VALUES_ADDR_W",
                "type": "P",
                "val": 4,
                "min": 1,
                "max": "NA",
                "descr": "Address width",
            },
            {
                "name": "VALUES_HEXFILE",
                "type": "P",
                "val": "rom.hex",
                "min": "NA",
                "max": "NA",
                "descr": "Hex file to load",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {"type": "clk_en_rst"},
                "descr": "Clock, enable and reset",
            },
            {
                "name": "start_i",
                "signals": [{"name": "start_i", "width": 1}],
                "descr": "Start signal",
            },
            {
                "name": "values_m",
                "signals": {
                    "type": "rom_sp",
                    "prefix": "values",
                    "DATA_W": "VALUES_DATA_W",
                    "ADDR_W": "VALUES_ADDR_W",
                },
                "descr": "Memory interface",
            },
            {
                "name": "result_o",
                "signals": [{"name": "result_o", "width": "VALUES_DATA_W"}],
                "descr": "Result",
            },
        ],
        "wires": [
            {
                "name": "r_data_i",
                "signals": [{"name": "r_data_i"}],
            },
            {
                "name": "addr_o",
                "signals": [{"name": "addr_o"}],
            },
            {
                "name": "acc_en_rst",
                "signals": [
                    {"name": "acc_enable", "width": 1, "descr": "Enable signal"},
                    {
                        "name": "acc_reset",
                        "width": 1,
                        "descr": "Synchronous reset signal",
                    },
                ],
            },
            {
                "name": "ctr_en_rst",
                "signals": [
                    {"name": "ctr_enable", "width": 1, "descr": "Enable signal"},
                    {
                        "name": "ctr_reset",
                        "width": 1,
                        "descr": "Synchronous reset signal",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_acc",
                "instance_name": "accomulator0",
                "parameters": {
                    "DATA_W": "VALUES_DATA_W",
                    "RST_VAL": "{VALUES_DATA_W{1'b0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "en_rst_i": "acc_en_rst",
                    "incr_i": "r_data_i",
                    "data_o": "result_o",
                },
            },
            {
                "core_name": "iob_counter",
                "instance_name": "counter0",
                "parameters": {
                    "DATA_W": "VALUES_ADDR_W",
                    "RST_VAL": "{VALUES_ADDR_W{1'b0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "en_rst_i": "ctr_en_rst",
                    "data_o": "addr_o",
                },
            },
        ],
        "fsm": {
            "type": "fsm",
            "verilog_code": """
            default_assignments:
                ctr_enable = 1'b0;
                ctr_reset = 1'b0;
                acc_enable = 1'b0;
                acc_reset = 1'b0;

            IDLE:  
                if (start_i)
                begin
                    state_nxt = READ;
                    acc_reset = 1'b1;
                    ctr_reset = 1'b1;
                end
                
            READ:
                ctr_enable = 1'b1;
                state_nxt = ACCUMULATE;

            ACCUMULATE:
                acc_enable = 1'b1;
                if (values_addr_o == {VALUES_ADDR_W{1'b1}})
                    state_nxt = state + 1;
                else
                    state_nxt = READ;

            state_nxt = IDLE;
            """,
        },
        "snippets": [
            {
                "verilog_code": """
    assign valuesclk_o = clk_i;
            """
            }
        ],
    }
    return attributes_dict
