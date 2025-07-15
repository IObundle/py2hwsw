# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
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
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "1",
                "min": "1",
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
                "name": "ram_2p_s",
                "descr": "RAM interface",
                "signals": {
                    "type": "ram_2p",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "buses": [
            {
                "name": "clk",
                "descr": "Input port",
                "signals": [
                    {"name": "clk_i"},
                ],
            },
            {
                "name": "en_int",
                "descr": "en bus",
                "signals": [
                    {"name": "en_int", "width": 1},
                ],
            },
            {
                "name": "we_int",
                "descr": "we bus",
                "signals": [
                    {"name": "we_int", "width": 1},
                ],
            },
            {
                "name": "addr_int",
                "descr": "addr bus",
                "signals": [
                    {"name": "addr_int", "width": "ADDR_W"},
                ],
            },
            {
                "name": "w_data",
                "descr": "Input port",
                "signals": [
                    {"name": "w_data_i"},
                ],
            },
            {
                "name": "r_data",
                "descr": "Output port",
                "signals": [
                    {"name": "r_data_o"},
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
                    "clk_i": "clk",
                    "en_i": "en_int",
                    "we_i": "we_int",
                    "addr_i": "addr_int",
                    "d_i": "w_data",
                    "d_o": "r_data",
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
