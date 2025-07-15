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
                    "iob_zybo_z7",
                ],
                "buses": [
                    {
                        "name": "sut_rs232",
                        "descr": "rs232 bus for SUT",
                        "signals": {
                            "type": "rs232",
                            "prefix": "sut_",
                        },
                    },
                    {
                        "name": "sut_rs232_inverted",
                        "descr": "Invert order of rs232 signals",
                        "signals": [
                            {"name": "sut_rs232_txd"},
                            {"name": "sut_rs232_rxd"},
                            {"name": "sut_rs232_cts"},
                            {"name": "sut_rs232_rts"},
                        ],
                    },
                ],
                "subblocks": [
                    {
                        # Instantiate SUT (usually iob_system or a child of it)
                        "core_name": py_params_dict["issuer"]["original_name"],
                        "instance_name": "SUT",
                        "instance_description": "System Under Test (SUT) to be verified by this tester.",
                        # "is_peripheral": True,  # Only applies if SUT has CSRs (via regfileif).
                        "parameters": {
                            "AXI_ID_W": "AXI_ID_W",
                            "AXI_LEN_W": "AXI_LEN_W",
                            "AXI_ADDR_W": "AXI_ADDR_W",
                            "AXI_DATA_W": "AXI_DATA_W",
                        },
                        "connect": {
                            "clk_en_rst_s": "clk_en_rst_s",
                            # Cbus (if any) is connected automatically
                            "rs232_m": "sut_rs232",
                        },
                    },
                    {
                        # Instantiate a UART core to communicate with SUT
                        "core_name": "iob_uart",
                        "instance_name": "UART1",
                        "instance_description": "UART peripheral for communication with SUT.",
                        "is_peripheral": True,
                        "parameters": {},
                        "connect": {
                            "clk_en_rst_s": "clk_en_rst_s",
                            # Cbus connected automatically
                            "rs232_m": "sut_rs232_inverted",
                        },
                    },
                    # NOTE: Add other verification instruments (tester peripherals) here.
                ],
            },
        },
    }

    return core_dict
