#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

from iob_base import find_obj_in_list, fail_with_msg


def get_core_params(confs, kinds=["P", "D"]):
    """Filter given 'confs' list for parameters of specified 'kinds'.
    Returns a new filtered list containing only parameters of specified 'kinds'.
    """
    core_parameters = []
    for conf in confs:
        if conf.kind in kinds:
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
        if parameter.kind == "D":
            p_comment = "  // Don't change this parameter value!"
        lines.append(f"    parameter {p_name} = `{core_prefix}{p_name},{p_comment}\n")

    # Remove comma from last line
    if lines:
        lines[-1] = lines[-1].replace(",", "", 1)

    return "".join(lines)


def generate_localparams(core):
    """Generate verilog code with verilog local parameters of this module.
    returns: Generated verilog code
    """
    localparams = get_core_params(core.confs, kinds=["L"])
    if not localparams:
        return ""
    lines = []
    for parameter in localparams:
        p_name = parameter.name.upper()
        lines.append(f"   localparam {p_name} = {parameter.value};")
    return "".join(lines)


def generate_inst_params(instance):
    """Generate verilog code with assignment of values for the verilog parameters of this instance.
    returns: Generated verilog code
    """
    validate_params(instance)
    instance_parameters = instance.parameters
    lines = []
    for p_name, p_value in instance_parameters.items():
        lines.append(f"        .{p_name}({p_value}),\n")
    if lines:
        lines[-1] = lines[-1].replace(",\n", "\n")

    return "".join(lines)


def validate_params(instance):
    """Check if all parameters are within the allowed range"""
    core_parameters = get_core_params(instance.core.confs)
    for p_name, p_value in instance.parameters.items():
        if isinstance(p_value, str):
            continue
        conf = find_obj_in_list(core_parameters, p_name)

        try:
            min_val = int(conf.min_value)
        except Exception:
            min_val = 0
        try:
            max_val = int(conf.max_value)
        except Exception:
            max_val = 2**31 - 1
        if p_value < min_val or p_value > max_val:
            fail_with_msg(
                f"Parameter '{p_name}' value '{p_value}' is out of range [{min_val}, {max_val}]"
            )
