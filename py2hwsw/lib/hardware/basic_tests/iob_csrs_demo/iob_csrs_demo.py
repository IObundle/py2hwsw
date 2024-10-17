# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "confs": [
            {
                "name": "ADDR_W",
                "type": "P",
                "val": 4,  # Same as CSRS_ADDR_W
                "min": 0,
                "max": 32,
                "descr": "Address bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "interface": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "cbus_s",
                "interface": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W - 2",
                    "DATA_W": "DATA_W",
                },
                "descr": "CPU native interface",
            },
        ],
        "wires": [
            {
                "name": "csrs_iob",
                "descr": "Internal CSRs IOb interface. Signals used to handle CSRs with 'autoreg=False'.",
                "interface": {
                    "type": "iob",
                    "prefix": "csrs_",
                    "ADDR_W": "ADDR_W - 2",
                    "DATA_W": "DATA_W",
                },
            },
            # Register wires
            {
                "name": "single_write",
                "descr": "",
                "signals": [
                    {"name": "single_write_wr", "width": 1},
                ],
            },
            {
                "name": "single_read",
                "descr": "",
                "signals": [
                    {"name": "single_read_wr", "width": 1},
                ],
            },
            # Regifiles wires
            {
                "name": "regfile_write",
                "descr": "",
                "signals": [
                    {"name": "regfile_write_0_wr", "width": 8},
                    {"name": "regfile_write_1_wr", "width": 8},
                    {"name": "regfile_write_2_wr", "width": 8},
                    {"name": "regfile_write_3_wr", "width": 8},
                ],
            },
            {
                "name": "regfile_read",
                "descr": "",
                "signals": [
                    {"name": "regfile_read_0_rd", "width": 8},
                    {"name": "regfile_read_1_rd", "width": 8},
                    {"name": "regfile_read_2_rd", "width": 8},
                    {"name": "regfile_read_3_rd", "width": 8},
                ],
            },
            {
                "name": "fifo_write_rst",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_rst", "width": 1},
                ],
            },
            {
                "name": "fifo_write_read",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_w_en", "width": 1},
                    {"name": "fifo_write_w_full", "width": 1},
                    {"name": "fifo_write_w_data", "width": 8},
                ],
            },
            {
                "name": "fifo_write_interrupt",
                "descr": "",
                "signals": [
                    {"name": "fifo_write_interrupt", "width": 1},
                ],
            },
        ],
        "blocks": [
            {
                "core_name": "csrs",
                "instance_name": "csrs_inst",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "demo_single_csrs",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "single_write",
                                "type": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Single write register",
                            },
                            {
                                "name": "single_read",
                                "type": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "autoreg": True,
                                "descr": "Single read register",
                            },
                        ],
                    },
                    #
                    # See commit 0fc91ac for info about regfiles
                    #
                    {
                        "name": "demo_regfiles",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "regfile_write",
                                "type": "W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,
                                "autoreg": True,
                                "descr": "Write regfile with 4 registers",
                            },
                            {
                                "name": "regfile_read",
                                "type": "R",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,
                                "autoreg": True,
                                "descr": "Read regfile with wires for 4 registers (no generated registers)",
                            },
                        ],
                    },
                    #
                    # See commit 925e7ad for info about FIFOs
                    #
                    {
                        "name": "demo_fifo_write",
                        "descr": "demo software accessible registers.",
                        "regs": [
                            {
                                "name": "fifo_write",
                                "type": "FIFO_W",
                                "n_bits": 8,
                                "rst_val": 0,
                                "log2n_items": 2,
                                "autoreg": True,
                                "descr": "Write FIFO",
                            },
                        ],
                    },
                    # {
                    #     "name": "demo_fifo_read",
                    #     "descr": "demo software accessible registers.",
                    #     "regs": [
                    #         {
                    #             "name": "fifo_read",
                    #             "type": "FIFO_R",
                    #             "n_bits": 8,
                    #             "rst_val": 0,
                    #             "log2n_items": 2,
                    #             "autoreg": True,
                    #             "descr": "Read FIFO",
                    #         },
                    #     ],
                    # },
                    # {
                    #     "name": "demo_afifo_read",
                    #     "descr": "demo software accessible registers.",
                    #     "regs": [
                    #         {
                    #             "name": "asym_fifo_read",
                    #             "type": "AFIFO_R",
                    #             "n_bits": 8,
                    #             "rst_val": 0,
                    #             "log2n_items": 2,
                    #             "autoreg": True,
                    #             "descr": "Asymmetric read FIFO",
                    #         },
                    #     ],
                    # },
                    # {
                    #     "name": "demo_afifo_write",
                    #     "descr": "demo software accessible registers.",
                    #     "regs": [
                    #         {
                    #             "name": "asym_fifo_write",
                    #             "type": "AFIFO_W",
                    #             "n_bits": 8,
                    #             "rst_val": 0,
                    #             "log2n_items": 2,
                    #             "autoreg": True,
                    #             "descr": "Asymmetric write FIFO",
                    #         },
                    #     ],
                    # },
                ],
                "csr_if": "iob",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "control_if_s": "cbus_s",
                    "csrs_iob_o": "csrs_iob",
                    # Register interfaces
                    "reset": "reset",
                },
            },
        ],
    }

    return attributes_dict
