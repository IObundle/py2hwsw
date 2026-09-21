# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXI4 read manager helper module.
#
# This helper orchestrates AXI4 read transfers for `iob_axi_m`.
# It slices large read requests into bursts, manages FIFO buffering, and
# forwards received data through AXI-Stream output.
# Address progression follows burst type semantics (`INCR` advances address,
# `FIXED` keeps address constant), and 4KB boundary splitting is applied when
# required by incrementing bursts.
#
# Status legend: supported / partial / not implemented.
#
# | AXI4 Feature | Support | Notes |
# | --- | --- | --- |
# | **Read Path** |  |  |
# | Read channel (`AR/R`) | supported | Read path is implemented end-to-end. |
# | Write channel (`AW/W/B`) | not implemented | This module handles read path only. |
# | Burst length (`AxLEN`) | supported | Burst length is generated and split when needed. |
# | 4KB boundary handling | supported | Bursts are split to avoid crossing 4KB boundaries. |
# | Burst types (`AxBURST`: INCR/FIXED/WRAP) | partial | INCR and FIXED supported; WRAP not implemented. |
# | **Attributes & IDs** |  |  |
# | IDs (`ARID/RID`) | partial | `ARID` is fixed to 0 and `RID` is not checked. |
# | Transfer size (`ARSIZE`) | partial | Fixed to 4-byte beats (`3'd2`). |
# | Cache/protection/QoS (`ARCACHE/ARPROT/ARQOS`) | partial | Driven with constant values. |
# | Region/USER sideband (`ARREGION/ARUSER/RUSER`) | not implemented | Not generated or consumed by this module. |
# | **Responses & Ordering** |  |  |
# | Read response checking (`RRESP`) | not implemented | Error codes are not evaluated. |
# | Multiple outstanding bursts | not implemented | Bursts are serialized by control FSMs. |
# | Out-of-order completion handling | not implemented | No ID-based tracking/reordering logic. |


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
