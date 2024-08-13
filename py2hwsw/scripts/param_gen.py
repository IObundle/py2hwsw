#!/usr/bin/env python3


def has_params(confs):
    """Check if given 'confs' list has any parameters"""
    for conf in confs:
        if conf.type in ["P", "F"]:
            return True
    return False


def generate_params(core):
    """Generate verilog code with verilog parameters of this module.
    returns: Generated verilog code
    """
    module_parameters = [p for p in core.confs if p.type in ["P", "F"]]

    if not has_params(core.confs):
        return ""

    lines = []
    core_prefix = f"{core.name}_".upper()
    for parameter in module_parameters:
        p_name = parameter.name.upper()
        lines.append(f"    parameter {p_name} = `{core_prefix}{p_name},\n")
    lines[-1] = lines[-1].replace(",\n", "\n")

    return "".join(lines)


def generate_inst_params(core):
    """Generate verilog code with assignment of values for the verilog parameters of this instance.
    returns: Generated verilog code
    """
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
    with open(f"{out_dir}/{core.name}_params.vs", "w") as f:
        f.write(code)

    code = generate_inst_params(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.instance_name}_{id(core)}_inst_params.vs", "w") as f:
        f.write(code)
