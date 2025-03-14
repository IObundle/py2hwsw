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
                "val": "0",
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
                "name": "DMA_RLEN_W",
                "type": "P",
                "val": "0",
                "min": "NA",
                "max": "NA",
                "descr": "DMA read length width",
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
                "name": "config_read_io",
                "descr": "",
                "signals": [
                    {"name": "r_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "r_length_i", "width": "DMA_RLEN_W"},
                    {"name": "r_start_transfer_i", "width": "1"},
                    {"name": "r_max_len_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "r_remaining_data_o", "width": "DMA_RLEN_W"},
                    {"name": "r_busy_o", "width": "1"},
                ],
            },
            # AXIS Interface - without last
            {
                "name": "axis_out_io",
                "descr": "",
                "signals": [
                    {"name": "axis_out_data_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_valid_o", "width": "1"},
                    {"name": "axis_out_ready_i", "width": "1"},
                ],
            },
            {
                "name": "axi_read_m",
                "signals": {
                    "type": "axi_read",
                    "prefix": "m_",
                    "file_prefix": "iob_dma_read_m_",
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
                "signals": {"type": "ram_2p", "prefix": "dma_read_"},
            },
        ],
        "subblocks": [
            {"core_name": "iob_fifo2axis"},
            {"core_name": "iob_fifo_sync"},
            {"core_name": "iob_axis2axi"},
            {"core_name": "iob_reg_r"},
        ],
    }
    return attributes_dict
