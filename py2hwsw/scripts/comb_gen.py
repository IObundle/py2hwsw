#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from api_base import convert2internal


def generate_comb(core):
    """Generate verilog code with the comb of this module.
    returns: Generated verilog code
    """
    if core.comb != None:
        return convert2internal(core.comb).verilog_code + "\n"

    return ""


def generate_comb_snippet(core):
    """Write verilog snippet ('.vs' file) with the comb of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_comb(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_comb.vs", "w+") as f:
        f.write(code)
