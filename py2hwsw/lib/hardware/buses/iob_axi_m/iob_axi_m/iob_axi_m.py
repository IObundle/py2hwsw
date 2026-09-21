# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXI4 manager module.
#
# This module composes the read and write helper paths into a single AXI4
# manager interface with AXI-Stream ingress/egress.
# It coordinates burst generation, buffering through local FIFOs, and
# transfer progress signaling for both channels.
# Burst type is independently configurable for read and write paths, with
# boundary handling applied according to the selected burst semantics.
#
# Status legend: supported / partial / not implemented.
#
# | AXI4 Feature | Support | Notes |
# | --- | --- | --- |
# | **Addressing & Bursts** |  |  |
# | Read channel (`AR/R`) | supported | Implemented in `iob_axi_m_read`. |
# | Write channel (`AW/W/B`) | supported | Implemented in `iob_axi_m_write`. |
# | Burst length (`AxLEN`) | supported | Burst length is generated and split when needed. |
# | 4KB boundary handling | supported | Bursts are split to avoid crossing 4KB boundaries. |
# | Burst types (`AxBURST`: INCR/FIXED/WRAP) | partial | INCR and FIXED supported; WRAP not implemented. |
# | IDs (`AWID/ARID/BID/RID`) | partial | `AWID/ARID` are fixed to 0; `BID/RID` are not checked. |
# | **Attributes & Sideband** |  |  |
# | Cache attributes (`AxCACHE`) | partial | Driven with a constant value. |
# | Protection attributes (`AxPROT`) | partial | Driven with a constant value. |
# | QoS attributes (`AxQOS`) | partial | Driven with a constant value. |
# | Transfer size (`AxSIZE`) | partial | Fixed to 4-byte beats (`3'd2`). |
# | Exclusive access (`AxLOCK`) | not implemented | Exclusive semantics are not implemented. |
# | Region attributes (`AxREGION`) | not implemented | Not generated. |
# | USER sideband signals | not implemented | `AWUSER/ARUSER/WUSER/RUSER/BUSER` are not used. |
# | **Data Path** |  |  |
# | Data width configurability | partial | `AXI_DATA_W` exists, but logic is focused on 32-bit words. |
# | Write byte strobes (`WSTRB`) | partial | Always full-word (`all ones`). |
# | Narrow/unaligned accesses | not implemented | No dynamic `AxSIZE`/`WSTRB` handling. |
# | **Responses** |  |  |
# | Read response checking (`RRESP`) | not implemented | Error codes are not evaluated. |
# | Write response checking (`BRESP`) | not implemented | Error codes are not evaluated. |
# | **Ordering & Concurrency** |  |  |
# | Multiple outstanding bursts | not implemented | Control FSMs serialize bursts (single burst in flight). |
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
                ],
            },
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
                ],
            },
            # AXIS Interfaces
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
                "name": "axis_out_io",
                "descr": "",
                "signals": [
                    {"name": "axis_out_data_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_valid_o", "width": "1"},
                    {"name": "axis_out_ready_i", "width": "1"},
                ],
            },
            {
                "name": "write_ext_mem_m",
                "descr": "External memory interface",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "w_ext_mem_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "read_ext_mem_m",
                "descr": "External memory interface",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "r_ext_mem_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "axi_m",
                "signals": {
                    "type": "axi",
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
            {"core": "iob_axi_m_read"},
            {"core": "iob_axi_m_write"},
        ],
    }

    return attributes_dict
