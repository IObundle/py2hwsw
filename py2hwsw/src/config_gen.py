#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def conf_vh(macros, top_module, out_dir):
    """Given a list with macros, generate a `*_conf.vh` file with the Verilog macro definitions.
    :param macros: list with macros (iob_conf class).
    :param top_module: top module name
    :param out_dir: output directory
    """
    file2create = open(f"{out_dir}/{top_module}_conf.vh", "w")
    core_prefix = f"{top_module}_".upper()

    # These ifndefs cause issues when this file is included in multiple files and it contains other ifdefs inside this block.
    # For example, assume this file is included in another one that does not have `MACRO1` defined. Now assume that inside this block there is an `ifdef MACRO1` block.
    # Since `MACRO1` is not defined in the file that is including this, the `ifdef MACRO1` wont be executed.
    # Now assume this file is included in another file that has `MACRO1` defined. Now, this block
    # wont execute because of the `ifndef` added here, therefore the `ifdef MACRO1` block will also not execute when it should have.
    # file2create.write(f"`ifndef VH_{fname}_VH\n")
    # file2create.write(f"`define VH_{fname}_VH\n\n")

    # Sort macros macros by type, P first, M second, C third, D last
    sorted_macros = []
    for macro in macros:
        if macro.kind == "P":
            sorted_macros.append(macro)
    for macro in macros:
        if macro.kind == "M":
            sorted_macros.append(macro)
    for macro in macros:
        if macro.kind == "C":
            sorted_macros.append(macro)
    for macro in macros:
        if macro.kind == "D":
            sorted_macros.append(macro)

    prev_type = ""
    for macro in sorted_macros:
        macro_type = macro.kind
        # If the type of the macro is different from the previous one, add a comment
        if macro_type != prev_type:
            if macro_type == "P":
                file2create.write("// Core Configuration Parameters Default Values\n")
            elif macro_type == "M":
                file2create.write("// Core Configuration Macros.\n")
            elif macro_type == "C":
                file2create.write("// Core Constants. DO NOT CHANGE\n")
            elif macro_type == "D":
                file2create.write("// Core Derived Parameters. DO NOT CHANGE\n")
            prev_type = macro_type

        # If macro has 'doc_only' attribute set to True, skip it
        if macro.doc_only:
            continue

        # Only insert macro if its is not a bool define, and if so only insert it if it is true
        if type(macro.value) is not bool:
            m_name = macro.name.upper()
            m_default_val = macro.value
            file2create.write(f"`define {core_prefix}{m_name} {m_default_val}\n")
        elif macro.value:
            m_name = macro.name.upper()
            file2create.write(f"`define {core_prefix}{m_name} 1\n")


def config_build_mk(python_module, top_module):
    file2create = open(f"{python_module.build_dir}/config_build.mk", "w")
    file2create.write(f"NAME={python_module.name}\n")
    file2create.write("CSR_IF ?=iob\n")
    file2create.write(f"BUILD_DIR_NAME={top_module.build_dir.split('/')[-1]}\n")
    file2create.write(f"IS_FPGA={int(python_module.is_system)}\n")
    file2create.write(
        """
CONFIG_BUILD_DIR = $(dir $(lastword $(MAKEFILE_LIST)))
ifneq ($(wildcard $(CONFIG_BUILD_DIR)/custom_config_build.mk),)
include $(CONFIG_BUILD_DIR)/custom_config_build.mk
endif
"""
    )

    if python_module.is_tester:
        file2create.write(
            f"RELATIVE_PATH_TO_UUT={python_module.relative_path_to_UUT}\n"
        )

    file2create.close()


def generate_confs(core):
    """Generate Verilog and software macros based on the core's 'confs' list.
    :param core: core object
    """
    confs = core.confs
    conf_vh(
        confs,
        core.name,
        os.path.join(core.build_dir, core.dest_dir),
    )
