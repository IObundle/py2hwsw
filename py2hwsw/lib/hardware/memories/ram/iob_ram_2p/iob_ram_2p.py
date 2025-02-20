# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "version": "0.1",
        "confs": [
            {
                "name": "HEXFILE",
                "type": "P",
                "val": '"none"',
                "min": "NA",
                "max": "NA",
                "descr": "Name of file to load into RAM",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "WRITE_FIRST",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "w_en_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_en_i", "width": 1},
                ],
            },
            {
                "name": "w_addr_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "w_data_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_data_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "w_ready_o",
                "descr": "Output port",
                "signals": [
                    {"name": "w_ready_o", "width": 1},
                ],
            },
            {
                "name": "r_en_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_en_i", "width": 1},
                ],
            },
            {
                "name": "r_addr_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "r_data_o",
                "descr": "Output port",
                "signals": [
                    {"name": "r_data_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "r_ready_o",
                "descr": "Output port",
                "signals": [
                    {"name": "r_ready_o", "width": 1},
                ],
            },
        ],
        "wires": [
            {
                "name": "en_int",
                "descr": "en wire",
                "signals": [
                    {"name": "en_int", "width": 1},
                ],
            },
            {
                "name": "we_int",
                "descr": "we wire",
                "signals": [
                    {"name": "we_int", "width": 1},
                ],
            },
            {
                "name": "addr_int",
                "descr": "addr wire",
                "signals": [
                    {"name": "addr_int", "width": "ADDR_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_ram_sp",
                "instance_name": "iob_ram_sp_inst",
                "parameters": {
                    "HEXFILE": "HEXFILE",
                    "DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                },
                "connect": {
                    "clk_i": "clk_i",
                    "en_i": "en_int",
                    "we_i": "we_int",
                    "addr_i": "addr_int",
                    "d_i": "w_data_i",
                    "d_o": "r_data_o",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            generate
    if (WRITE_FIRST) begin : write_first
        assign en_int = w_en_i | r_en_i;
        assign we_int = w_en_i;
        assign addr_int = w_en_i ? w_addr_i : r_addr_i;
        assign w_ready_o = 1'b1;
        assign r_ready_o = ~w_en_i;
    end else begin : read_first
        assign en_int = w_en_i | r_en_i;
        assign we_int = w_en_i & (~r_en_i);
        assign addr_int = r_en_i ? r_addr_i : w_addr_i;
        assign w_ready_o = ~r_en_i;
        assign r_ready_o = 1'b1;
    end
   endgenerate
            """,
            },
        ],
    }

    return attributes_dict
