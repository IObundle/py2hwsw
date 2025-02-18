# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": False,
        "ports": [
            {
                "name": "clk_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "port_params": "arst",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "reg_interface_io",
                "descr": "",
                "signals": [
                    {"name": "rst_soft_i", "width": "1"},
                    {"name": "tx_en_i", "width": "1"},
                    {"name": "rx_en_i", "width": "1"},
                    {"name": "tx_ready_o", "width": "1"},
                    {"name": "rx_ready_o", "width": "1"},
                    {"name": "tx_data_i", "width": "8"},
                    {"name": "rx_data_o", "width": "8"},
                    {"name": "data_write_en_i", "width": "1"},
                    {"name": "data_read_en_i", "width": "1"},
                    {
                        "name": "bit_duration_i",
                        "width": "`IOB_UART_DIV_W",
                    },
                ],
            },
            {
                "name": "rs232_m",
                "signals": {
                    "type": "rs232",
                },
                "descr": "RS232 interface",
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_reg_e",
            },
        ],
    }

    return attributes_dict
