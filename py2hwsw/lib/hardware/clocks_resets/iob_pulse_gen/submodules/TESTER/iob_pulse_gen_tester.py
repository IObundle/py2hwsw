# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Py2hwsw dictionary describing current core
    core_dict = {
        "version": "0.1",
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
                "board_list": ["aes_ku040_db_g", "cyclonev_gt_dk", "zybo_z7"],
                "wires": [
                    {
                        "name": "gpio_input",
                        "descr": "",
                        "signals": [
                            {"name": "gpio_input", "width": 1},
                        ],
                    },
                    {
                        "name": "gpio_output",
                        "descr": "",
                        "signals": [
                            {"name": "gpio_output", "width": 1},
                        ],
                    },
                ],
                "subblocks": [
                    {
                        # Instantiate SUT (usually iob_system or a child of it)
                        "core_name": py_params_dict["instantiator"]["original_name"],
                        "instance_name": "pulse_gen_uut",
                        "instance_description": "Unit Under Test (UUT) to be verified by this tester.",
                        "parameters": {
                            "START": 2,
                            "DURATION": 10,
                        },
                        "connect": {
                            "clk_en_rst_s": "clk_en_rst_s",
                            "start_i": "gpio_output",
                            "pulse_o": "gpio_input",
                        },
                    },
                    {
                        # Instantiate a GPIO core to verify pulse_gen
                        "core_name": "iob_gpio",
                        "instance_name": "GPIO0",
                        "instance_description": "GPIO verification tool",
                        "is_peripheral": True,
                        "parameters": {
                            "INPUT_GPIO_W": 1,
                            "OUTPUT_GPIO_W": 1,
                        },
                        "connect": {
                            "clk_en_rst_s": "clk_en_rst_s",
                            # Cbus connected automatically
                            "input_0_i": "gpio_input",
                            "output_0_o": "gpio_output",
                        },
                    },
                    # NOTE: Add other verification tools (tester peripherals) here.
                ],
            },
        },
    }

    return core_dict
