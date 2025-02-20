# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "confs": [
            {
                "name": "ADDR_W",
                "descr": "",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
            },
            {
                "name": "DATA_W",
                "descr": "",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            # AXI parameters
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": "ADDR_W",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": "DATA_W",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "4",
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
                "name": "control_io",
                "descr": "Control interface",
                "signals": [
                    {"name": "run_i", "width": 1, "descr": ""},
                    {  # FIXME: Unused?
                        "name": "direction_i",
                        "width": 1,
                        "descr": "0 for reading, 1 for writing",
                    },
                    {"name": "addr_i", "width": "ADDR_W", "descr": ""},
                    {"name": "ready_o", "width": 1, "descr": ""},
                    {"name": "error_o", "width": 1, "descr": ""},
                ],
            },
            {
                "name": "axi_m",
                "descr": "Master AXI interface",
                "signals": {
                    "type": "axi",
                    "prefix": "m_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "iob_s",
                "descr": "Slave IOb interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "ext_fifo_sync0_mem_m",
                "descr": "External memory interface for fifo sync 0",
                "signals": {"type": "ram_t2p", "prefix": "fifo_sync0_"},
            },
            {
                "name": "ext_fifo_sync1_mem_m",
                "descr": "External memory interface for fifo sync 1",
                "signals": {"type": "ram_t2p", "prefix": "fifo_sync1_"},
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fifo_sync",
            },
            {
                "core_name": "iob_functions",
            },
            {
                "core_name": "iob_iob2axi_rd",
            },
            {
                "core_name": "iob_iob2axi_wr",
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
