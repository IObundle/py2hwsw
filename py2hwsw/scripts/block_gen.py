#
#    blocks.py: instantiate Verilog modules and generate their documentation
#

from latex import write_table

import iob_colors
from iob_base import fail_with_msg
from iob_port import get_signal_name_with_dir_suffix
from iob_signal import get_real_signal
import param_gen


# Generate blocks.tex file with TeX table of blocks (Verilog modules instances)
def generate_blocks_table_tex(out_dir):
    blocks_file = open(f"{out_dir}/blocks.tex", "w")

    blocks_file.write(
        "The Verilog modules in the top-level entity of the core are \
        described in the following table. The table elements represent \
        the blocks in the Block Diagram.\n"
    )

    blocks_file.write(
        """
\\begin{table}[H]
  \\centering
  \\begin{tabularx}{\\textwidth}{|l|l|X|}

    \\hline
    \\rowcolor{iob-green}
    {\\bf Module} & {\\bf Name} & {\\bf Description}  \\\\ \\hline \\hline

    \\input blocks_module_tab

  \\end{tabularx}
  \\caption{Verilog modules in the top-level entity of the core}
  \\label{blocks_module_tab:is}
\\end{table}
"""
    )

    blocks_file.write("\\clearpage")
    blocks_file.close()


# Generate TeX table of blocks
def generate_blocks_tex(blocks, out_dir):
    # Create blocks.tex file
    generate_blocks_table_tex(out_dir)

    tex_table = []
    for block in blocks:
        if not block.instantiate:
            continue
        tex_table.append(
            [
                block.name,
                block.instance_name,
                block.instance_description,
            ]
        )

    write_table(f"{out_dir}/blocks_module", tex_table)


def generate_blocks(core):
    """Generate verilog code with verilog instances of this module.
    returns: Generated verilog code
    """
    code = ""
    for instance in core.blocks:
        if not instance.instantiate:
            continue
        # Open ifdef if conditional interface
        if instance.if_defined:
            code += f"`ifdef {instance.if_defined}\n"
        if instance.if_not_defined:
            code += f"`ifndef {instance.if_not_defined}\n"

        params_str = ""
        if instance.parameters:
            params_str = f"""#(
{param_gen.generate_inst_params(instance)}\
    ) """

        code += f"""\
    // {instance.instance_description}
    {instance.name} {params_str}{instance.instance_name} (
{get_instance_port_connections(instance)}\
    );

"""

        # Close ifdef if conditional interface
        if instance.if_defined or instance.if_not_defined:
            code += "`endif\n"

    return code


def generate_blocks_snippet(core):
    """Write verilog snippet ('.vs' file) with blocks of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_blocks(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_blocks.vs", "w+") as f:
        f.write(code)


def convert_int(val):
    """Try to convert val to int"""
    try:
        return int(val)
    except ValueError:
        return 0


def get_instance_port_connections(instance):
    """Returns a multi-line string with all port's signals connections
    for the given Verilog instance.
    """
    instance_portmap = ""
    for port_idx, port in enumerate(instance.ports):
        assert (
            port.e_connect
        ), f"{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' is not connected!{iob_colors.ENDC}"
        instance_portmap += f"        // {port.name} port\n"
        newlinechar = "\n"
        assert len(port.signals) == len(
            port.e_connect.signals
        ), f"""{iob_colors.FAIL}Port '{port.name}' of instance '{instance.name}' has different number of signals from external connection '{port.e_connect.name}'!
Port '{port.name}' has the following signals:
{newlinechar.join("- " + port.name for port in port.signals)}

External connection '{port.e_connect.name}' has the following signals:
{newlinechar.join("- " + port.name for port in port.e_connect.signals)}
{iob_colors.ENDC}"""
        # Connect individual signals
        for idx, signal in enumerate(port.signals):
            port_name = get_signal_name_with_dir_suffix(signal)
            real_e_signal = get_real_signal(port.e_connect.signals[idx])
            if real_e_signal.direction:
                # External signal belongs to a port. Use direction suffix.
                e_signal_name = get_signal_name_with_dir_suffix(real_e_signal)
            else:
                e_signal_name = real_e_signal.name

            comma = ""
            if port_idx < len(instance.ports) - 1 or idx < len(port.signals) - 1:
                comma = ","

            # Auto-generate bit selection if port is smaller than external signal
            # Most significant bits of external signal are discarded
            # NOTE: This will suppress warnings if connection was made by mistake with wrong width.
            #       Should we keep this functionality?
            port_width = ""
            signal_int = convert_int(signal.width)
            e_signal_int = convert_int(real_e_signal.width)
            if signal_int and e_signal_int and signal_int < e_signal_int:
                port_width = f" [{signal_int}-1:0]"
            if signal_int and e_signal_int and signal_int > e_signal_int:
                fail_with_msg(
                    f"Port '{port.name}' of instance '{instance.name}' has signal '{port_name}' with width '{signal.width}' which is greater than external signal width {real_e_signal.width}!"
                )

            instance_portmap += (
                f"        .{port_name}({e_signal_name}{port_width}){comma}\n"
            )

    return instance_portmap
