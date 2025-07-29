#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
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
