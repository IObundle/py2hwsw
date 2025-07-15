# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        # Note: This core currently has a manual verilog source! The generate_hw is true only because of the generated csrs subblock.
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "0",
                "max": "32",
                "descr": "Data bus width",
            },
            {
                "name": "PERIOD_W",
                "type": "D",
                "val": "2*DATA_W",
                "min": "0",
                "max": "32",
                "descr": "Period bus width",
            },
            {
                "name": "FRAC_W",
                "type": "D",
                "val": "DATA_W",
                "min": "0",
                "max": "32",
                "descr": "Bit-width of the fractional part of the period value. Used to differentiate between the integer and fractional parts of the period. ",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "clock, clock enable and reset",
            },
            {
                "name": "clk_gen_io",
                "descr": "Generated clock interface",
                "signals": [
                    {
                        "name": "clk_in_i",
                        "width": "1",
                        "descr": "Clock input",
                    },
                    {
                        "name": "clk_in_arst_i",
                        "width": "1",
                        "descr": "Clock input asynchronous reset",
                    },
                    {
                        "name": "clk_in_cke_i",
                        "width": "1",
                        "descr": "Clock input enable",
                    },
                    {
                        "name": "clk_out_o",
                        "width": "1",
                        "descr": "Generated clock output",
                    },
                ],
            },
        ],
        "buses": [
            # Register buses
            {
                "name": "soft_reset",
                "descr": "",
                "signals": [
                    {"name": "soft_reset_wr", "width": 1},
                ],
            },
            {
                "name": "enable",
                "descr": "",
                "signals": [
                    {"name": "enable_wr", "width": 1},
                ],
            },
            {
                "name": "period_int",
                "descr": "",
                "signals": [
                    {"name": "period_int_wdata_wr", "width": 32},
                    {"name": "period_int_wen_wr", "width": 1},
                    {"name": "period_int_ready_wr", "width": 1},
                ],
            },
            {
                "name": "period_frac",
                "descr": "",
                "signals": [
                    {"name": "period_frac_wdata_wr", "width": 32},
                    {"name": "period_frac_wen_wr", "width": 1},
                    {"name": "period_frac_ready_wr", "width": 1},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "nco",
                        "descr": "NCO software accessible registers.",
                        "regs": [
                            {
                                "name": "soft_reset",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Soft reset.",
                            },
                            {
                                "name": "enable",
                                "mode": "W",
                                "n_bits": 1,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "NCO enable",
                            },
                            {
                                "name": "period_int",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 32,
                                "rst_val": 5,
                                "log2n_items": 0,
                                "descr": "Integer part of the generated period. Period of the generated clock in terms of the number of system clock cycles + 1 implicit clock cycle. NOTE: need to write to both PERIOD_INT, PERIOD_FRAC registers to set internal period.",
                            },
                            {
                                "name": "period_frac",
                                "type": "NOAUTO",
                                "mode": "W",
                                "n_bits": 32,
                                "rst_val": 0,
                                "log2n_items": 0,
                                "descr": "Fractional part of the generated period. NOTE: need to write to both PERIOD_INT, PERIOD_FRAC registers to set internal period.",
                            },
                        ],
                    }
                ],
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    # Register interfaces
                    "soft_reset_o": "soft_reset",
                    "enable_o": "enable",
                    "period_int_io": "period_int",
                    "period_frac_io": "period_frac",
                },
            },
            {
                "core_name": "iob_acc_ld",
                "instantiate": False,
            },
            {
                "core_name": "iob_modcnt",
                "instantiate": False,
            },
            {
                "core_name": "iob_nco_sync",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg",
                "instantiate": False,
                "port_params": {
                    "clk_en_rst_s": "c_a_r_e",
                },
            },
            {
                "core_name": "iob_sync",
                "instantiate": False,
            },
            {
                "core_name": "iob_fifo_async",
                "instantiate": False,
            },
            {
                "core_name": "iob_regarray_at2p",
                "instantiate": False,
            },
            # For simulation
            {
                "core_name": "iob_tasks",
                "instance_name": "iob_tasks_inst",
                "dest_dir": "hardware/simulation/src",
                "instantiate": False,
            },
        ],
        "snippets": [],
    }

    return attributes_dict
