# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    PLIC_SOURCE_ID = py_params_dict.get("plic_source_id", 1)

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
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
                "name": "interrupt_o",
                "signals": [
                    {
                        "name": "interrupt_o",
                        "width": 1,
                        "descr": "Timer interrupt source",
                    },
                ],
            },
        ],
        "wires": [
            # Register wires
            {
                "name": "reset",
                "descr": "",
                "signals": [
                    {"name": "reset_wr", "width": 1},
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
                "name": "sample",
                "descr": "",
                "signals": [
                    {"name": "sample_wr", "width": 1},
                ],
            },
            {
                "name": "data_low",
                "descr": "",
                "signals": [
                    {"name": "data_low_rd", "width": 32},
                ],
            },
            {
                "name": "data_high",
                "descr": "",
                "signals": [
                    {"name": "data_high_rd", "width": 32},
                ],
            },
            {
                "name": "interrupt_data_low",
                "descr": "",
                "signals": [
                    {"name": "interrupt_data_low_wr", "width": 32},
                ],
            },
            {
                "name": "interrupt_data_high",
                "descr": "",
                "signals": [
                    {"name": "interrupt_data_high_wr", "width": 32},
                ],
            },
            # Internal wires
            {
                "name": "time_now",
                "descr": "",
                "signals": [
                    {"name": "time_now", "width": 64},
                ],
            },
            # Timer core
            {
                "name": "iob_timer_core_reg_interface",
                "descr": "",
                "signals": [
                    {"name": "enable_wr"},
                    {"name": "reset_wr"},
                    {"name": "sample_wr"},
                    {"name": "time_now"},
                ],
            },
            {
                "name": "interrupt_threshold",
                "signals": [
                    {"name": "interrupt_data_low_wr"},
                    {"name": "interrupt_data_high_wr"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "csrs",
                "instance_description": "Control/Status Registers",
                "csrs": [
                    {
                        "name": "reset",
                        "mode": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Timer soft reset",
                    },
                    {
                        "name": "enable",
                        "mode": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Timer enable",
                    },
                    {
                        "name": "sample",
                        "mode": "W",
                        "n_bits": 1,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Sample time counter value into a readable register",
                    },
                    {
                        "name": "data_low",
                        "mode": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Low part of the timer value, which has twice the width of the data word width",
                    },
                    {
                        "name": "data_high",
                        "mode": "R",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "High part of the timer value, which has twice the width of the data word width",
                    },
                    {
                        "name": "interrupt_data_low",
                        "mode": "W",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "Low part of the timer interrupt threshold value, which has twice the width of the data word width. Interrupts disabled if low and high parts are set to zero.",
                    },
                    {
                        "name": "interrupt_data_high",
                        "mode": "W",
                        "n_bits": 32,
                        "rst_val": 0,
                        "log2n_items": 0,
                        "descr": "High part of the timer interrupt threshold value, which has twice the width of the data word width. Interrupts disabled if low and high parts are set to zero.",
                    },
                ],
                "csr_if": "iob",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    # Register interfaces
                    "reset_o": "reset",
                    "enable_o": "enable",
                    "sample_o": "sample",
                    "data_low_i": "data_low",
                    "data_high_i": "data_high",
                    "interrupt_data_low_o": "interrupt_data_low",
                    "interrupt_data_high_o": "interrupt_data_high",
                },
            },
            {
                "core_name": "iob_timer_core",
                "instance_name": "iob_timer_core_inst",
                "instance_description": "Timer core driver",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reg_interface_io": "iob_timer_core_reg_interface",
                    "interrupt_threshold_i": "interrupt_threshold",
                    "interrupt_o": "interrupt_o",
                },
            },
        ],
        "sw_modules": [
            # Software modules
            {
                "core_name": "iob_linux_device_drivers",
                # Extra device tree properties specific to this peripheral
                "dts_extra_properties": f"""
        interrupt-parent = < &PLIC0 >; // PLIC phandle (matches PLIC peripheral name in system's DT)
        interrupts = <{PLIC_SOURCE_ID}>; // PLIC source ID
""",
                # Enable interrupt support in the generated driver
                "support_interrupts": True,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign data_low_rd  = time_now[DATA_W-1:0];
    assign data_high_rd = time_now[2*DATA_W-1:DATA_W];
""",
            },
        ],
    }

    return attributes_dict
