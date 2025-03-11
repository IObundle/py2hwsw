# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Py2hwsw dictionary describing current core
    core_dict = {
        "parent": {
            # Tester is a child core of iob_system: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_system
            # Tester will inherit all attributes/files from the iob_system core.
            "core_name": "iob_system",
            "include_tester": False,
            # Every parameter in the lines below will be passed to the iob_system parent core.
            **py_params_dict,
            "system_attributes": {
                # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
                "is_tester": True,
                # Every attribute in this dictionary will override/append to the ones of the iob_system parent core.
                "board_list": [
                    "iob_aes_ku040_db_g",
                    "iob_cyclonev_gt_dk",
                ],
                "subblocks": [
                    {
                        "core_name": "iob_uart",
                        "instance_name": "UART0",
                        "instance_description": "UART peripheral",
                        "is_peripheral": True,
                        "parameters": {},
                        "connect": {
                            # "clk_en_rst_s": "clk_en_rst_s",
                            # Cbus connected automatically
                            "rs232_m": "rs232_m",
                        },
                    },
                    # NOTE: Add other test instruments here
                ],
            },
        },
    }

    return core_dict
