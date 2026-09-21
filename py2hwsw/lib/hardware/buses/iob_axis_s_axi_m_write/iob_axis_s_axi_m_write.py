# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

# AXIS-to-AXI4 write manager bridge.
#
# This bridge consumes AXI-Stream input data and issues AXI4 write bursts.
# It manages write-side burst control, address progression, and completion
# sequencing for address/data/response channels.
# It supports `INCR` and `FIXED` burst semantics, with 4KB boundary-aware
# splitting applied when required for incrementing bursts.
#
# Status legend: supported / partial / not implemented.
#
# | AXI4 Feature | Support | Notes |
# | --- | --- | --- |
# | **Core Function** |  |  |
# | AXIS sink to AXI write data | supported | Consumes AXIS input and drives AXI write payload. |
# | Write address/data/response channels (`AW/W/B`) | supported | Issues writes and waits for write responses. |
# | **Burst & Attributes** |  |  |
# | Burst length (`AWLEN`) | supported | Burst requests are generated from transfer length. |
# | Burst types (`AWBURST`: INCR/FIXED/WRAP) | partial | INCR and FIXED supported; WRAP not implemented. |
# | 4KB boundary handling | supported | Requests are split to keep transfers in bounds. |
# | IDs (`AWID/BID`) | partial | `AWID` fixed to 0; `BID` not checked. |
# | Transfer size (`AWSIZE`) | partial | Fixed to 4-byte beats. |
# | Write strobes (`WSTRB`) | partial | Fixed to full-word strobes (`all ones`). |
# | Write attributes (`AWCACHE/AWPROT/AWQOS`) | partial | Driven with constant values. |
# | Write response checking (`BRESP`) | not implemented | Error codes are not evaluated. |


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
            # Configuration
            {
                "name": "config_io",
                "descr": "Configuration signals",
                "signals": [
                    {"name": "w_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "w_length_i", "width": "AXI_LEN_W"},
                    {"name": "w_start_transfer_i", "width": "1"},
                    {"name": "w_burst_type_i", "width": "2"},
                    {"name": "w_busy_o", "width": "1"},
                    {"name": "w_resp_o", "width": "2"},
                ],
            },
            # Axi stream input
            {
                "name": "axis_in_io",
                "descr": "AXI Stream input",
                "signals": [
                    {"name": "axis_in_data_i", "width": "AXI_DATA_W"},
                    {"name": "axis_in_valid_i", "width": "1"},
                    {"name": "axis_in_ready_o", "width": "1"},
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
