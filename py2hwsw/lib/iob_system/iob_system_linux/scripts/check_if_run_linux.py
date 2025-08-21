#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""
This script checks if the SoC is running linux or not.
It will create the "<soc_name>_mem.config" file that specifies which binaries and addresses to load to RAM when INIT_MEM=0.
If running baremetal firmware, the config file will only specify the firmware file and its load address.
If running linux, the config file will specify the bootloader, linux kernel, dtb and rootfs.
"""

import sys

ROOT_DIR = sys.argv[1]
SOC_NAME = sys.argv[2]
FW_BASE_ADDR = sys.argv[3]
if len(sys.argv) > 4:
    RUN_LINUX = sys.argv[4]
else:
    RUN_LINUX = "0"


# If line contains "line_content", replace entire line with "new_line_content"
# If "line_content" is empty, append "new_line_content" to end of file
def replace_line(filename, line_content, new_line_content):
    with open(filename, "r") as file:
        lines = file.readlines()
    if line_content:
        for i in range(len(lines)):
            if line_content in lines[i]:
                lines[i] = new_line_content
    else:
        lines.append(new_line_content)

    with open(filename, "w") as file:
        file.writelines(lines)


# Generate "iob_mem.config" according to which binary firmware the SoC should load to RAM

iob_mem_file = f"{ROOT_DIR}/hardware/{SOC_NAME}_mem.config"
with open(iob_mem_file, "w") as file:
    if RUN_LINUX == "1":
        file.write(
            f"fw_jump.bin 0\nImage 400000\n{SOC_NAME}.dtb F80000\nrootfs.cpio.gz 1000000"
        )
    else:
        file.write(f"{SOC_NAME}_firmware.bin {FW_BASE_ADDR}")


# Fixes existing iob_bsp.h and iob_bsp.vh for Simulation

bsp_file = f"{ROOT_DIR}/software/src/iob_bsp.h"
with open(bsp_file, "r") as file:
    content = file.read()

if "define SIMULATION 1" in content:
    if RUN_LINUX == "1":
        # Change simulation baudrate
        # bsp_file = f"{ROOT_DIR}/hardware/simulation/src/iob_bsp.vh"
        # replace_line(bsp_file, "`define BAUD", "`define BAUD 115200\n")

        # Change simulation baudrate
        # bsp_file = f"{ROOT_DIR}/software/src/iob_bsp.h"
        # replace_line(bsp_file, "#define BAUD", "#define BAUD 115200\n")

        # Add RUN_LINUX macro to conf.vh
        # conf_file = f"{ROOT_DIR}/hardware/src/{SOC_NAME}_conf.vh"
        # replace_line(conf_file, "", "`define {SOC_NAME.upper()}_RUN_LINUX 1\n")

        # Add RUN_LINUX macro to conf.h
        conf_file = f"{ROOT_DIR}/software/src/{SOC_NAME}_conf.h"
        replace_line(
            conf_file,
            "#define H_{SOC_NAME.upper()}_CONF_H",
            "#define H_{SOC_NAME.upper()}_CONF_H\n#define {SOC_NAME.upper()}_RUN_LINUX 1\n",
        )
    else:
        # Change simulation baudrate
        # bsp_file = f"{ROOT_DIR}/hardware/simulation/src/iob_bsp.vh"
        # replace_line(bsp_file, "`define BAUD", "`define BAUD 3000000\n")

        # Change simulation baudrate
        # bsp_file = f"{ROOT_DIR}/software/src/iob_bsp.h"
        # replace_line(bsp_file, "#define BAUD", "#define BAUD 3000000\n")

        # Remove RUN_LINUX macro from conf.vh
        # conf_file = f"{ROOT_DIR}/hardware/src/{SOC_NAME}_conf.vh"
        # replace_line(conf_file, "`define {SOC_NAME.upper()}_RUN_LINUX", "")

        # Remove RUN_LINUX macro from conf.h
        conf_file = f"{ROOT_DIR}/software/src/{SOC_NAME}_conf.h"
        replace_line(conf_file, "#define {SOC_NAME.upper()}_RUN_LINUX", "")
