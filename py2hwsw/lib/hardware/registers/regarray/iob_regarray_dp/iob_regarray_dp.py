# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of data",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "width of address",
            },
            # Derived Parameters
            {
                "name": "WSTRB_W",
                "type": "D",
                "val": "DATA_W / 8",
                "min": "0",
                "max": "NA",
                "descr": "width of write strobe",
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
                "name": "port_a_io",
                "descr": "Port A",
                "signals": [
                    {"name": "a_en_i", "width": 1},
                    {"name": "a_wstrb_i", "width": "WSTRB_W"},
                    {"name": "a_addr_i", "width": "ADDR_W"},
                    {"name": "a_data_i", "width": "DATA_W"},
                    {"name": "a_data_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "port_b_io",
                "descr": "Port B",
                "signals": [
                    {"name": "b_en_i", "width": 1},
                    {"name": "b_wstrb_i", "width": "WSTRB_W"},
                    {"name": "b_addr_i", "width": "ADDR_W"},
                    {"name": "b_data_i", "width": "DATA_W"},
                    {"name": "b_data_o", "width": "DATA_W"},
                ],
            },
        ],
        "wires": [
            {
                "name": "regarray_2p_write_i",
                "descr": "Write port",
                "signals": [
                    {"name": "2p_w_en_i", "width": 1},
                    {"name": "2p_w_strb_i", "width": "WSTRB_W"},
                    {"name": "2p_w_addr_i", "width": "ADDR_W"},
                    {"name": "2p_w_data_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "regarray_2p_read_io",
                "descr": "read port",
                "signals": [
                    {"name": "2p_r_addr_i", "width": "ADDR_W"},
                    {"name": "2p_r_data_o", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_regarray_2p",
                "instance_name": "iob_regarray_2p_inst",
                "instance_description": "2-port register array",
                "parameters": {
                    "N": "1<<ADDR_W",
                    "W": "DATA_W",
                    "WDATA_W": "DATA_W",
                    "WADDR_W": "ADDR_W",
                    "RDATA_W": "DATA_W",
                    "RADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "write_i": "regarray_2p_write_i",
                    "read_io": "regarray_2p_read_io",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   assign 2p_w_en_i = (a_en_i & |a_wstrb_i) | (b_en_i & |b_wstrb_i);
   assign 2p_w_strb_i = (a_en_i & |a_wstrb_i) ? a_wstrb_i : b_wstrb_i;
   assign 2p_w_addr_i = (a_en_i & |a_wstrb_i) ? a_addr_i : b_addr_i;
   assign 2p_w_data_i = (a_en_i & |a_wstrb_i) ? a_data_i : b_data_i;

   assign 2p_r_addr_i = (a_en_i & ~|a_wstrb_i) ? a_addr_i : b_addr_i;
   assign a_data_o = 2p_r_data_o;
   assign b_data_o = 2p_r_data_o;
""",
            },
        ],
    }

    return attributes_dict
