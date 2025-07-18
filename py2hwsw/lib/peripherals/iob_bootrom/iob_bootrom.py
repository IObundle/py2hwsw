# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    BOOTROM_ADDR_W = (
        py_params_dict["bootrom_addr_w"] if "bootrom_addr_w" in py_params_dict else 12
    )

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "D",
                "val": "32",
                "min": "0",
                "max": "32",
            },
            {
                "name": "ADDR_W",
                "descr": "Address bus width",
                "type": "D",
                "val": BOOTROM_ADDR_W - 2,
                "min": "0",
                "max": "32",
            },
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": "1",
                "min": "0",
                "max": "4",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "8",
            },
        ],
        #
        # Ports
        #
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock and reset",
                "wires": {
                    "type": "iob_clk",
                },
            },
            # Implicit 'rom_bus_m' port generated automatically for external memory wrapper
        ],
        #
        # Blocks
        #
        "subblocks": [
            {
                "core_name": "iob_csrs",
                "instance_name": "iob_csrs",
                "csrs": [
                    {
                        "name": "rom",
                        "descr": "ROM access.",
                        "regs": [
                            {
                                "name": "rom",
                                "descr": "Bootloader ROM (read).",
                                "type": "ROM",
                                "mode": "R",
                                "n_bits": "DATA_W",
                                "rst_val": 0,
                                "addr": -1,
                                "log2n_items": BOOTROM_ADDR_W - 2,
                            },
                        ],
                    }
                ],
                "csr_if": "axi",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # 'control_if_m' port connected automatically
                    # 'rom_bus_m' port for external memory connected automatically
                },
            },
        ],
    }

    copy_sw_srcs_with_rename(py_params_dict)

    return attributes_dict


def copy_sw_srcs_with_rename(py_params):
    """Copy software sources, and rename them based on correct SoC name."""
    SOC_NAME = py_params.get("soc_name", "iob_system")

    # Don't create files for other targets (like clean)
    if py_params.get("py2hwsw_target") != "setup":
        return

    SRC_DIR = os.path.join(os.path.dirname(__file__), "software_templates/src")
    DEST_DIR = os.path.join(py_params.get("build_dir"), "software/src")
    os.makedirs(DEST_DIR, exist_ok=True)

    for filename in os.listdir(SRC_DIR):
        new_filename = filename.replace("iob_system", SOC_NAME)
        src = os.path.join(SRC_DIR, filename)
        dst = os.path.join(DEST_DIR, new_filename)

        # Read file, replace strings with SoC name, and write new file
        with open(src, "r") as file:
            lines = file.readlines()
        for idx in range(len(lines)):
            lines[idx] = (
                lines[idx]
                .replace("iob_system", SOC_NAME)
                .replace("iob_system".upper(), SOC_NAME.upper())
            )
        with open(dst, "w") as file:
            file.writelines(lines)
