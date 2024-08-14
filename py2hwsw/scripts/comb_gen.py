#!/usr/bin/env python3


def generate_combs(core):
    """Generate verilog code with combs of this module.
    returns: Generated verilog code
    """
    code = ""
    for comb in core.combs:
        code += comb.verilog_code
        code += "\n"

    return code


def generate_combs_snippet(core):
    """Write verilog snippet ('.vs' file) with combs of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_combs(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_combs.vs", "w+") as f:
        f.write(code)
