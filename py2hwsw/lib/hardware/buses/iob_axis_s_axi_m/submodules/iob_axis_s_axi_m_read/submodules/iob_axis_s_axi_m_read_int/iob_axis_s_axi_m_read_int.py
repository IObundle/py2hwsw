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
                "name": "AXI_DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "AXI data width",
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
                "name": "AXI_ID_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "AXI ID width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable, async and sync reset",
            },
            # Configuration IO's
            {
                "name": "config_read_io",
                "descr": "",
                "signals": [
                    {"name": "r_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "r_length_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "r_start_transfer_i"},
                    {"name": "r_busy_o"},
                ],
            },
            # AXIS Interface - without last
            {
                "name": "axis_out_io",
                "descr": "",
                "signals": [
                    {"name": "axis_out_data_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_valid_o"},
                    {"name": "axis_out_ready_i"},
                ],
            },
            {
                "name": "axi_read_m",
                "signals": {
                    "type": "axi_read",
                    "file_prefix": "iob_axis_s_axi_m_read_int_m_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "descr": "AXI interface",
            },
        ],
        "subblocks": [
            {"core_name": "iob_reg", "port_params": {"clk_en_rst_s": "c_a_r"}},
            {"core_name": "iob_reg", "port_params": {"clk_en_rst_s": "c_a_r_e"}},
        ],
    }
    return attributes_dict
