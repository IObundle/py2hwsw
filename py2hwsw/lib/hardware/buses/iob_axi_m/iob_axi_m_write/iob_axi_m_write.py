# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXI4 write manager helper module.
#
# This helper orchestrates AXI4 write transfers for `iob_axi_m`.
# It slices large write requests into bursts, manages FIFO buffering from
# AXI-Stream input, and emits AXI address/data bursts to memory.
# Address progression follows burst type semantics (`INCR` advances address,
# `FIXED` keeps address constant), and 4KB boundary splitting is applied when
# required by incrementing bursts.
#
# Status legend: supported / partial / not implemented.
#
# | AXI4 Feature | Support | Notes |
# | --- | --- | --- |
# | **Write Path** |  |  |
# | Write channel (`AW/W/B`) | supported | Write path is implemented end-to-end. |
# | Read channel (`AR/R`) | not implemented | This module handles write path only. |
# | Burst length (`AxLEN`) | supported | Burst length is generated and split when needed. |
# | 4KB boundary handling | supported | Bursts are split to avoid crossing 4KB boundaries. |
# | Burst types (`AxBURST`: INCR/FIXED/WRAP) | partial | INCR and FIXED supported; WRAP not implemented. |
# | **Attributes & IDs** |  |  |
# | IDs (`AWID/BID`) | partial | `AWID` is fixed to 0 and `BID` is not checked. |
# | Transfer size (`AWSIZE`) | partial | Fixed to 4-byte beats (`3'd2`). |
# | Byte strobes (`WSTRB`) | partial | Always full-word (`all ones`). |
# | Cache/protection/QoS (`AWCACHE/AWPROT/AWQOS`) | partial | Driven with constant values. |
# | Region/USER sideband (`AWREGION/AWUSER/WUSER/BUSER`) | not implemented | Not generated or consumed by this module. |
# | **Responses & Ordering** |  |  |
# | Write response checking (`BRESP`) | not implemented | Error codes are not evaluated. |
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
                "name": "WLENGTH_W",
                "type": "P",
                "val": "1",
                "min": "NA",
                "max": "NA",
                "descr": "Write length width",
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
                "name": "config_write_io",
                "descr": "",
                "signals": [
                    {"name": "w_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "w_length_i", "width": "WLENGTH_W"},
                    {"name": "w_start_transfer_i", "width": "1"},
                    {"name": "w_max_len_i", "width": "AXI_LEN_W"},
                    {"name": "w_burst_type_i", "width": "2"},
                    {"name": "w_remaining_data_o", "width": "WLENGTH_W"},
                    {"name": "w_busy_o", "width": "1"},
                    {"name": "w_resp_o", "width": "2"},
                ],
            },
            # AXIS Slave Interface
            {
                "name": "axis_in_io",
                "descr": "",
                "signals": [
                    {"name": "axis_in_data_i", "width": "AXI_DATA_W"},
                    {"name": "axis_in_valid_i", "width": "1"},
                    {"name": "axis_in_ready_o", "width": "1"},
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
                "name": "axi_write_m",
                "signals": {
                    "type": "axi_write",
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
            {"core": "iob_axis_s_axi_m_write"},
            {
                "core": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
        ],
    }

    return attributes_dict
