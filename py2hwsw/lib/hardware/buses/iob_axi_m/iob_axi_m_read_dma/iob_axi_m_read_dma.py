# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXI4 read manager helper module with DMA request/ack support.


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
                "name": "RLENGTH_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Read length width",
            },
            {
                "name": "FIFO_ADDR_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "FIFO address width",
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
                    {"name": "r_length_i", "width": "RLENGTH_W"},
                    {"name": "r_start_transfer_i", "width": "1"},
                    {"name": "r_dma_req_en_i", "width": "1"},
                    {"name": "r_dma_req_i", "width": "1"},
                    {"name": "r_dma_req_pending_o", "width": "1"},
                    {"name": "r_dma_ack_o", "width": "1"},
                    {"name": "r_max_len_i", "width": "AXI_LEN_W"},
                    {"name": "r_burst_type_i", "width": "2"},
                    {"name": "r_remaining_data_o", "width": "RLENGTH_W"},
                    {"name": "r_busy_o", "width": "1"},
                    {"name": "r_resp_o", "width": "2"},
                ],
            },
            # AXIS Master Interface
            {
                "name": "axis_out_io",
                "descr": "",
                "signals": [
                    {"name": "axis_out_tdata_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_tvalid_o", "width": "1"},
                    {"name": "axis_out_tready_i", "width": "1"},
                ],
            },
            {
                "name": "ext_mem_m",
                "descr": "External memory interface",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_",
                    "ADDR_W": "FIFO_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "axi_read_m",
                "signals": {
                    "type": "axi_read",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "PROT_W": 3,
                },
                "descr": "AXI interface",
            },
        ],
        "subblocks": [
            {
                "core": "iob_fifo2axis",
                "use_tlast": True,
                "use_level": True,
                "use_en": True,
            },
            {"core": "iob_fifo_sync"},
            {
                "core": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
            {"core": "iob_axis_m_axi_m_read"},
        ],
    }

    return attributes_dict
