#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

from iob_base import find_obj_in_list, fail_with_msg


def get_core_params(confs):
    """Filter given 'confs' list for 'P' and 'F' parameters.
    Returns a new filtered list containing only 'P' and 'F' parameters.
    """
    core_parameters = []
    for group in confs:
        for conf in group.confs:
            if conf.type in ["P", "F"]:
                core_parameters.append(conf)
    return core_parameters


def generate_params(core):
    """Generate verilog code with verilog parameters of this module.
    returns: Generated verilog code
    """
    core_parameters = get_core_params(core.confs)

    if not core_parameters:
        return ""

    lines = []
    core_prefix = f"{core.name}_".upper()
    for idx, parameter in enumerate(core_parameters):
        # If parameter has 'doc_only' attribute set to True, skip it
        if parameter.doc_only:
            continue

        p_name = parameter.name.upper()
        p_comment = ""
        if parameter.type == "F":
            p_comment = "  // Don't change this parameter value!"
        lines.append(f"    parameter {p_name} = `{core_prefix}{p_name},{p_comment}\n")

    # Remove comma from last line
    if lines:
        lines[-1] = lines[-1].replace(",", "", 1)

    return "".join(lines)


def generate_inst_params(core):
    """Generate verilog code with assignment of values for the verilog parameters of this instance.
    returns: Generated verilog code
    """
    validate_params(core)
    instance_parameters = core.parameters
    lines = []
    for p_name, p_value in instance_parameters.items():
        lines.append(f"        .{p_name}({p_value}),\n")
    if lines:
        lines[-1] = lines[-1].replace(",\n", "\n")

    return "".join(lines)


def generate_params_snippets(core):
    """Write verilog snippets ('.vs' files) with verilog parameters of this core.
    These snippets may be included manually in verilog modules if needed.
    """
    code = generate_params(core)
    out_dir = core.build_dir + "/hardware/src"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/{core.name}_params.vs", "w") as f:
        f.write(code)

    code = generate_inst_params(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.instance_name}_{id(core)}_inst_params.vs", "w") as f:
        f.write(code)


def validate_params(core):
    """Check if all parameters are within the allowed range"""
    core_parameters = get_core_params(core.confs)
    for p_name, p_value in core.parameters.items():
        if isinstance(p_value, str):
            continue
        conf = find_obj_in_list(core_parameters, p_name)

        try:
            min_val = int(conf.min)
        except Exception:
            min_val = 0
        try:
            max_val = int(conf.max)
        except Exception:
            max_val = 2**31 - 1
        if p_value < min_val or p_value > max_val:
            fail_with_msg(
                f"Parameter '{p_name}' value '{p_value}' is out of range [{min_val}, {max_val}]"
            )
