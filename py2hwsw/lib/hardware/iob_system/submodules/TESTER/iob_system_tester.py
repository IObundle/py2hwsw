# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Py2hwsw dictionary describing current core
    core_dict = {
        # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
        "is_tester": True,
        "version": "0.1",
        "parent": {
            # Tester is a child core of iob_system: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_system
            # Tester will inherit all attributes/files from the iob_system core.
            "core_name": "iob_system",
            # Every parameter in the lines below will be passed to the iob_system parent core.
            **py_params_dict,
            "system_attributes": {
                # Every attribute in this dictionary will override/append to the ones of the iob_system parent core.
                "board_list": ["aes_ku040_db_g", "cyclonev_gt_dk", "zybo_z7"],
                "subblocks": [
                    {
                        # Instantiate SUT (usually iob_system or a child of it)
                        "core_name": py_params_dict["instantiator"]["original_name"],
                        "instance_name": "SUT",
                        "instance_description": "System Under Test (SUT) to be verified by this tester.",
                        # "peripheral_addr_w": 4,  # Width of cbus of this peripheral. Only applies if SUT has CSRs (via regfileif).
                        "parameters": {},
                        "connect": {
                            "clk_en_rst_s": "clk_en_rst_s",
                            # Cbus (if any) is connected automatically
                        },
                    },
                    # NOTE: Add other verification tools (tester peripherals) here.
                ],
            },
        },
    }

    return core_dict
