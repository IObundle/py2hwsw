# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "AXI_ADDR_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "AXI address width",
            },
            {
                "name": "AXI_LEN_W",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "AXI len width",
            },
            {
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "AXI data width",
            },
            {
                "name": "AXI_ID_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "AXI ID width",
            },
            {
                "name": "WLEN_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Write length width",
            },
            {
                "name": "RLEN_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Read length width",
            },
            #
            # False-parameters for external memories
            #
            {
                "name": "WRITE_HEXFILE",
                "descr": "Write hexfile",
                "type": "D",
                "val": '"none"',
                "min": "NA",
                "max": "NA",
            },
            {
                "name": "READ_HEXFILE",
                "descr": "Read hexfile",
                "type": "D",
                "val": '"none"',
                "min": "NA",
                "max": "NA",
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
                "name": "rst_i",
                "descr": "Synchronous reset interface",
                "wires": [
                    {"name": "rst_i", "width": 1},
                ],
            },
            # Configuration IO's
            {
                "name": "config_write_io",
                "descr": "",
                "wires": [
                    {"name": "w_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "w_length_i", "width": "WLEN_W"},
                    {"name": "w_start_transfer_i", "width": "1"},
                    {"name": "w_max_len_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "w_remaining_data_o", "width": "WLEN_W"},
                    {"name": "w_busy_o", "width": "1"},
                ],
            },
            {
                "name": "config_read_io",
                "descr": "",
                "wires": [
                    {"name": "r_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "r_length_i", "width": "RLEN_W"},
                    {"name": "r_start_transfer_i", "width": "1"},
                    {"name": "r_max_len_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "r_remaining_data_o", "width": "RLEN_W"},
                    {"name": "r_busy_o", "width": "1"},
                ],
            },
            # AXIS Interfaces - without last
            {
                "name": "axis_in_io",
                "descr": "",
                "wires": [
                    {"name": "axis_in_tdata_i", "width": "AXI_DATA_W"},
                    {"name": "axis_in_tvalid_i", "width": "1"},
                    {"name": "axis_in_tready_o", "width": "1"},
                ],
            },
            {
                "name": "axis_out_io",
                "descr": "",
                "wires": [
                    {"name": "axis_out_tdata_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_tvalid_o", "width": "1"},
                    {"name": "axis_out_tready_i", "width": "1"},
                ],
            },
            {
                "name": "write_ext_mem_m",
                "descr": "External memory interface",
                "wires": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_write_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "read_ext_mem_m",
                "descr": "External memory interface",
                "wires": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_read_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "axi_m",
                "wires": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "descr": "AXI interface",
            },
        ],
        "subblocks": [
            {"core_name": "iob_axis_s_axi_m_read"},
            {"core_name": "iob_axis_s_axi_m_write"},
        ],
        "superblocks": [
            {"core_name": "iob_axistream_in"},
            {"core_name": "iob_axistream_out"},
            {"core_name": "iob_axi_ram"},
            {"core_name": "iob_ram_t2p_be"},
        ],
    }

    return attributes_dict
