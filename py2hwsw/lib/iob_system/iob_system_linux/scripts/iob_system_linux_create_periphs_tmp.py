#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Creates periphs_tmp.h

import os
import math
import iob_colors
import copy_srcs


def create_periphs_tmp(name, addr_w, peripherals_list, out_file):
    n_subordinates = len(peripherals_list) + 1  # +1 for boot_ctr

    template_contents = []
    # Peripheral base addresses
    for instance in peripherals_list:
        template_contents.extend(
            f"#define {instance.name}_BASE (({name.upper()}_{instance.name}<<({addr_w}-4-{name.upper()}_N_SUBORDINATES_W))|(0xf<<({addr_w}-4)))\n"
        )

    # PLIC and CLINT base addresses
    template_contents.extend(
        f"#define CLINT0_BASE (({name.upper()}_N_SUBORDINATES-2<<({addr_w}-4-{name.upper()}_N_SUBORDINATES_W))|(0xf<<({addr_w}-4)))\n"
    )
    template_contents.extend(
        f"#define PLIC0_BASE (({name.upper()}_N_SUBORDINATES-1<<({addr_w}-4-{name.upper()}_N_SUBORDINATES_W))|(0xf<<({addr_w}-4)))\n"
    )

    # Write output file
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    periphs_tmp_file = open(out_file, "w")
    periphs_tmp_file.writelines(template_contents)
    periphs_tmp_file.close()


# Get dictionary with peripheral addresses in hex
def get_periphs_hardcoded_addr(name, addr_w, peripherals_list):
    addr_w = int(addr_w)
    n_subordinates = len(peripherals_list) + 1  # +1 for boot_ctr
    n_subordinates_w = math.ceil(
        math.log(n_subordinates + 2, 2)
    )  # +2 for PLIC and CLINT

    periphs_addr = {}
    # Peripheral base addresses
    for idx, instance in enumerate(peripherals_list):
        periphs_addr[instance.name] = format(
            (idx + 1 << (addr_w - 4 - n_subordinates_w)) | (0xF << (addr_w - 4)), "x"
        )

    # PLIC and CLINT base addresses
    periphs_addr["CLINT0"] = format(
        (n_subordinates << (addr_w - 4 - n_subordinates_w)) | (0xF << (addr_w - 4)), "x"
    )
    periphs_addr["PLIC0"] = format(
        ((n_subordinates + 1) << (addr_w - 4 - n_subordinates_w))
        | (0xF << (addr_w - 4)),
        "x",
    )

    return periphs_addr


def check_linux_build_macros(python_module, iob_linux_setup_dir):
    setup_dir = python_module.setup_dir
    board_paths = [
        "hardware/simulation",
        "hardware/fpga/vivado/AES-KU040-DB-G",
        "hardware/fpga/quartus/CYCLONEV-GT-DK",
    ]
    board_paths_with_prefix = []
    for board_path in board_paths:
        board_paths_with_prefix.append(setup_dir + "/" + board_path)

    macros_filename = "linux_build_macros.txt"

    peripheral_addresses = get_periphs_hardcoded_addr(
        python_module.name,
        next(i["val"] for i in python_module.confs if i["name"] == "ADDR_W"),
        python_module.peripherals,
    )

    ### Functions

    # Extract a macro value from a bsp.vh file
    def extract_macro_value_from_bsp(file_path, macro_name):
        with open(file_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("`define " + macro_name):
                return line.split()[-1]

    # Update Linux build macros
    def update_build_macros():
        lib_dir = copy_srcs.LIB_DIR

        # Delete dtb and openSBI files to ensure user create new ones
        for path in board_paths_with_prefix:
            if os.path.exists(f"{path}/iob_soc.dtb"):
                os.remove(f"{path}/iob_soc.dtb")
            if os.path.exists(f"{path}/fw_jump.bin"):
                os.remove(f"{path}/fw_jump.bin")

        for path in board_paths:
            os.makedirs(f"{setup_dir}/{path}", exist_ok=True)
            with open(f"{setup_dir}/{path}/{macros_filename}", "w") as f:
                lines = []
                for address in peripheral_addresses.items():
                    lines.append(f"{address[0]}_ADDR {address[1]}\n")
                src = "/src" if "simulation" == path.split("/")[-1] else ""
                lines.append(
                    "FREQ "
                    + extract_macro_value_from_bsp(
                        f"{lib_dir}/{path}{src}/bsp.vh", "FREQ"
                    )
                    + "\n"
                )
                lines.append(
                    "BAUD "
                    + extract_macro_value_from_bsp(
                        f"{lib_dir}/{path}{src}/bsp.vh", "BAUD"
                    )
                    + "\n"
                )
                f.writelines(lines)

    # Print build info
    def print_build_info():
        linux_setup_dir_rel = os.path.relpath(iob_linux_setup_dir)
        # Print info about how to build new linux files
        print(
            f"{iob_colors.INFO}Use the following commands to build new Linux files, and re-run setup:{iob_colors.ENDC}"
        )
        print("```")
        for path in board_paths_with_prefix:
            rel_path = os.path.relpath(path, linux_setup_dir_rel)
            print(
                f"nix-shell {linux_setup_dir_rel}/default.nix --run 'make -C {linux_setup_dir_rel} build-dts MACROS_FILE={rel_path}/{macros_filename} OS_BUILD_DIR={rel_path}/'"
            )
            print(
                f"nix-shell {linux_setup_dir_rel}/default.nix --run 'make -C {linux_setup_dir_rel} build-opensbi MACROS_FILE={rel_path}/{macros_filename} OS_BUILD_DIR={rel_path}/'"
            )
        print("```\n")

    ### Code

    # Check if Linux macros build file exists
    if not os.path.exists(board_paths_with_prefix[0] + "/" + macros_filename):
        update_build_macros()
        print(f"{iob_colors.FAIL}Linux macros were missing!{iob_colors.ENDC}")
        print_build_info()
        exit(1)

    # Check if any peripheral addresses changed since last build
    with open(board_paths_with_prefix[0] + "/" + macros_filename, "r") as f:
        macro_lines = f.readlines()
    if len(macro_lines) != len(peripheral_addresses) + 2:
        update_build_macros()
        print(
            f"{iob_colors.FAIL}Peripheral addresses changed since last Linux build!{iob_colors.ENDC}"
        )
        print_build_info()
        exit(1)
    for idx, address in enumerate(peripheral_addresses.items()):
        if macro_lines[idx] != f"{address[0]}_ADDR {address[1]}\n":
            update_build_macros()
            print(
                f"{iob_colors.FAIL}Peripheral addresses changed since last Linux build!{iob_colors.ENDC}"
            )
            print_build_info()
            exit(1)

    # Check if Linux files are missing
    for path in board_paths_with_prefix:
        if not os.path.exists(f"{path}/iob_soc.dtb") or not os.path.exists(
            f"{path}/fw_jump.bin"
        ):
            print(f"{iob_colors.FAIL}Linux files missing!{iob_colors.ENDC}")
            print_build_info()
            exit(1)
