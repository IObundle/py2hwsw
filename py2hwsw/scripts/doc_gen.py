# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    doc_gen.py: generate documentation
#
import os

import config_gen
import io_gen
import block_gen

from latex import write_table


def generate_docs(core):
    """Generate common documentation files"""
    if core.is_top_module:
        config_gen.generate_confs_tex(core.confs, core.build_dir + "/document/tsrc")
        io_gen.generate_ios_tex(core.ports, core.build_dir + "/document/tsrc")
        block_gen.generate_subblocks_tex(
            core.subblocks, core.build_dir + "/document/tsrc"
        )


def generate_tex_py2hwsw_attributes(iob_core_class, out_dir):
    """Generate TeX table of supported attributes of the py2hwsw interface.
    The attributes listed can be used in the 'attributes' dictionary of cores.
    :param iob_core_class: Reference to the IOb core class. Used to instantiate dummy module.
    :param out_dir: Path to the output directory
    """

    # Set project wide special target (will prevent normal setup)
    iob_core_class.global_special_target = "print_attributes"
    # Build a new dummy module instance, to obtain its attributes
    module = iob_core_class()

    tex_table = []
    for name in module.ATTRIBUTE_PROPERTIES.keys():
        tex_table.append(
            [
                name,
                module.ATTRIBUTE_PROPERTIES[name].datatype,
                module.ATTRIBUTE_PROPERTIES[name].descr,
            ]
        )

    write_table(f"{out_dir}/py2hwsw_attributes", tex_table)


def generate_tex_core_lib(out_dir):
    """Generate TeX table of cores available in py2hwsw library.
    :param out_dir: Path to the output directory
    """
    lib_path = os.path.join(os.path.dirname(__file__), "../lib")

    tex_table = []
    # Find all .py files under lib_path
    for root, dirs, files in os.walk(lib_path):
        # Skip specific directories
        if os.path.basename(root) in ["scripts", "test", "document"]:
            dirs[:] = []
            continue
        for file in files:
            if file.endswith(".py"):
                tex_table.append(
                    [
                        os.path.splitext(file)[0],
                        os.path.relpath(root, lib_path),
                    ]
                )

    write_table(f"{out_dir}/py2hwsw_core_lib", tex_table)


def generate_tex_py_params(core):
    """Generate TeX section for python parameters of given core.
    :param iob_core core: core object
    """

    py_params_file = open(f"{core.build_dir}/document/tsrc/py_params.tex", "w")

    py_params_file.write(
        """
The following table describe the \\textit{Python Parameters} supported by the IP core.

\\begin{table}[H]
  \\centering
  \\begin{tabularx}{\\textwidth}{|l|c|X|}

    \\hline
    \\rowcolor{iob-green}
    {\\bf Name} & {\\bf Default Value} & {\\bf Description} \\\\ \\hline \\hline

    \\input """
        + core.original_name
        + """_py_params_tab

  \\end{tabularx}
  \\caption{\\textit{Python Parameters} supported by this IP core.}
  \\label{"""
        + core.original_name
        + """_py_params_tab:is}
\\end{table}
"""
    )

    py_params_file.write("\\clearpage")
    py_params_file.close()

    generate_tex_py_params_table(core)


def generate_tex_py_params_table(core):
    tex_table = []
    for param in core.python_parameters:
        tex_table.append(
            [
                param.name,
                param.value,
                param.description,
            ]
        )

    out_dir = core.build_dir + "/document/tsrc"
    write_table(f"{out_dir}/{core.original_name}_py_params", tex_table)
