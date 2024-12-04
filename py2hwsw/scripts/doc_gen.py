# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

#
#    doc_gen.py: generate documentation
#
import config_gen
import io_gen
import block_gen


def generate_docs(core):
    """Generate common documentation files"""
    if core.is_top_module:
        config_gen.generate_confs_tex(core.confs, core.build_dir + "/document/tsrc")
        io_gen.generate_ios_tex(core.ports, core.build_dir + "/document/tsrc")
        block_gen.generate_subblocks_tex(core.subblocks, core.build_dir + "/document/tsrc")
