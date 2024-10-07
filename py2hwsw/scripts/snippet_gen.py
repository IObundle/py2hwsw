#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

def generate_snippets(core):
    """Generate verilog code with snippets of this module.
    returns: Generated verilog code
    """
    code = ""
    for snippet in core.snippets:
        code += snippet.verilog_code
        code += "\n"

    return code


def generate_snippets_snippet(core):
    """Write verilog snippet ('.vs' file) with snippets ('snippets' list) of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_snippets(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_snippets.vs", "w+") as f:
        f.write(code)
