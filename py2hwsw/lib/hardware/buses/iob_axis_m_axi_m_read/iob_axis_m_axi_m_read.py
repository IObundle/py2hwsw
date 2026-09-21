# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXIS-to-AXI4 read manager bridge.
#
# This bridge generates AXI4 read bursts and converts returned read data into
# an AXI-Stream output.
# It implements read-side burst control and address progression, including
# `INCR` and `FIXED` burst semantics, plus 4KB boundary-aware splitting when
# required for incrementing bursts.
#
# Status legend: supported / partial / not implemented.
#
# | AXI4 Feature | Support | Notes |
# | --- | --- | --- |
# | **Core Function** |  |  |
# | AXIS source from AXI read data | supported | Converts AXI read beats into AXIS output stream. |
# | Read address/data channel (`AR/R`) | supported | Issues reads and forwards payload to AXIS. |
# | **Burst & Attributes** |  |  |
# | Burst length (`ARLEN`) | supported | Burst requests are generated from transfer length. |
# | Burst types (`ARBURST`: INCR/FIXED/WRAP) | partial | INCR and FIXED supported; WRAP not implemented. |
# | 4KB boundary handling | supported | Requests are split to keep transfers in bounds. |
# | IDs (`ARID/RID`) | partial | `ARID` fixed to 0; `RID` not checked. |
# | Transfer size (`ARSIZE`) | partial | Fixed to 4-byte beats. |
# | Read attributes (`ARCACHE/ARPROT/ARQOS`) | partial | Driven with constant values. |
# | Read response checking (`RRESP`) | not implemented | Error codes are not evaluated. |


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
            # Axi master interface
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
            # Configuration
            {
                "name": "config_io",
                "descr": "Configuration signals",
                "signals": [
                    {"name": "r_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "r_length_i", "width": "AXI_LEN_W"},
                    {"name": "r_start_transfer_i", "width": "1"},
                    {"name": "r_burst_type_i", "width": "2"},
                    {"name": "r_busy_o", "width": "1"},
                    {"name": "r_resp_o", "width": "2"},
                ],
            },
            # Axi stream output
            {
                "name": "axis_out_io",
                "descr": "AXI Stream output",
                "signals": [
                    {"name": "axis_out_data_o", "width": "AXI_DATA_W"},
                    {"name": "axis_out_valid_o", "width": "1"},
                    {"name": "axis_out_ready_i", "width": "1"},
                ],
            },
        ],
        "subblocks": [
            {
                "core": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
            },
            {
                "core": "iob_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
        ],
    }

    return attributes_dict
