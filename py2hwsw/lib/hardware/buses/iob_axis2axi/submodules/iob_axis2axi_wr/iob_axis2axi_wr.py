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
                "name": "rst_i",
                "descr": "Synchronous reset interface",
                "signals": [
                    {"name": "rst_i", "width": 1},
                ],
            },
            # Configuration IO's
            {
                "name": "config_write_io",
                "descr": "",
                "signals": [
                    {"name": "w_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "w_length_i", "width": "WLEN_W"},
                    {"name": "w_start_transfer_i", "width": "1"},
                    {"name": "w_max_len_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "w_remaining_data_o", "width": "WLEN_W"},
                    {"name": "w_busy_o", "width": "1"},
                ],
            },
            # AXIS Interface - without last
            {
                "name": "axis_in_io",
                "descr": "",
                "signals": [
                    {"name": "axis_in_tdata_i", "width": "AXI_DATA_W"},
                    {"name": "axis_in_tvalid_i", "width": "1"},
                    {"name": "axis_in_tready_o", "width": "1"},
                ],
            },
            {
                "name": "axi_write_m",
                "signals": {
                    "type": "axi_write",
                    "file_prefix": "iob_axis2axi_wr_m_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "descr": "AXI interface",
            },
            {
                "name": "ext_mem_m",
                "descr": "External memory interface",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_write_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "subblocks": [
            {"core_name": "iob_fifo_sync"},
            {
                "core_name": "iob_fifo2axis",
                "use_tlast": True,
                "use_level": True,
                "use_en": True,
            },
            {"core_name": "iob_reg", "port_params": {"clk_en_rst_s": "cke_arst_rst"}},
            {
                "core_name": "iob_reg",
                "port_params": {"clk_en_rst_s": "cke_arst_rst_en"},
            },
            {"core_name": "iob_counter"},
        ],
    }
    return attributes_dict
