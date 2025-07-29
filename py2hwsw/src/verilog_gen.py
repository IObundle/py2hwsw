#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

import param_gen
import io_gen
import block_gen
import snippet_gen
import wire_gen
from iob_base import debug_print


def generate_verilog(core):
    """Generate main Verilog module of given core
    if it does not exist yet (may be defined manually or generated previously).
    """
    out_dir = os.path.join(core.build_dir, core.dest_dir)
    file_path = os.path.join(out_dir, f"{core.name}.v")

    if os.path.exists(file_path):
        debug_print(
            f"Not generating '{core.name}.v'. Module already exists (probably created manually or generated previously).",
            1,
        )
        return

    f_module = open(file_path, "w+")

    params = param_gen.generate_params(core)
    if params:
        params_line = f"#(\n{params}) ("
    else:
        params_line = "("

    module_body_lines = ""
    if core.wires:
        module_body_lines += wire_gen.generate_wires(core) + "\n"

    local_params = param_gen.generate_localparams(core)
    if local_params:
        module_body_lines += local_params + "\n"

    if core.snippets:
        module_body_lines += snippet_gen.generate_snippets(core) + "\n"

    if core.subblocks:
        module_body_lines += block_gen.generate_subblocks(core)

    f_module.write(
        f"""`timescale 1ns / 1ps
`include "{core.name}_conf.vh"

module {core.name} {params_line}
{io_gen.generate_ports(core)}\
);

{module_body_lines}
endmodule
"""
    )
    f_module.close()
