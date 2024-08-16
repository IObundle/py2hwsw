#!/usr/bin/env python3


def generate_fsms(core):
    """Generate verilog code with fsms of this module.
    returns: Generated verilog code
    """
    if core.fsms != None:
        code = core.fsms.verilog_code + "\n"

    return code


def generate_fsms_snippet(core):
    """Write verilog snippet ('.vs' file) with fsms of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_fsms(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_fsms.vs", "w+") as f:
        f.write(code)
