# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    doc_gen.py: generate documentation
#
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
