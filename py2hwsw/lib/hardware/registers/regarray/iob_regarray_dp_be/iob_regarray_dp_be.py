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
                "wires": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "port_a_io",
                "descr": "Port A",
                "wires": [
                    {"name": "enA_i", "width": 1},
                    {"name": "wstrbA_i", "width": "WSTRB_W"},
                    {"name": "addrA_i", "width": "ADDR_W"},
                    {"name": "dA_i", "width": "DATA_W"},
                    {"name": "dA_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "port_b_io",
                "descr": "Port B",
                "wires": [
                    {"name": "enB_i", "width": 1},
                    {"name": "wstrbB_i", "width": "WSTRB_W"},
                    {"name": "addrB_i", "width": "ADDR_W"},
                    {"name": "dB_i", "width": "DATA_W"},
                    {"name": "dB_o", "width": "DATA_W"},
                ],
            },
        ],
        "buses": [
            {
                "name": "regarray_2p_write_i",
                "descr": "Write port",
                "wires": [
                    {"name": "regarray_2p_w_en_i", "width": 1},
                    {"name": "regarray_2p_w_strb_i", "width": "WSTRB_W"},
                    {"name": "regarray_2p_w_addr_i", "width": "ADDR_W"},
                    {"name": "regarray_2p_w_data_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "regarray_2p_read_io",
                "descr": "read port",
                "wires": [
                    {"name": "regarray_2p_r_addr_i", "width": "ADDR_W"},
                    {"name": "regarray_2p_r_data_o", "width": "DATA_W"},
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
   assign regarray_2p_w_en_i = (enA_i & |wstrbA_i) | (enB_i & |wstrbB_i);
   assign regarray_2p_w_strb_i = (enA_i & |wstrbA_i) ? wstrbA_i : wstrbB_i;
   assign regarray_2p_w_addr_i = (enA_i & |wstrbA_i) ? addrA_i : addrB_i;
   assign regarray_2p_w_data_i = (enA_i & |wstrbA_i) ? dA_i : dB_i;

   assign regarray_2p_r_addr_i = (enA_i & ~|wstrbA_i) ? addrA_i : addrB_i;
   assign dA_o = regarray_2p_r_data_o;
   assign dB_o = regarray_2p_r_data_o;
""",
            },
        ],
    }

    return attributes_dict
