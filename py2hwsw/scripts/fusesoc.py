# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import shutil

import iob_colors

OUTPUT_DIR = "fusesoc_exports"


def export_core(core):
    """Export core as a fusesoc core.
    This function will use the given core's attributes to generate the corresponding fusesoc `.core` yaml file.
    This function expects the  build directory for the core to have been generated previously.
    """

    # Don't try to export if build dir doesn't exist
    if not os.path.exists(core.build_dir):
        # print error and exit
        print(
            f"{iob_colors.FAIL}Build directory not found: {core.build_dir}. Core's build directory must be generated first before exporting.{iob_colors.ENDC}"
        )
        exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Copy build directory to OUTPUT_DIR
    shutil.copytree(core.build_dir, f"{OUTPUT_DIR}/{core.name}", dirs_exist_ok=True)

    core_file_content = f"""\
CAPI=2:

name: iobundle:py2hwsw:{core.name}:{core.version}
description : {core.description}

filesets:
  rtl:
    files:
{get_source_list(OUTPUT_DIR, core.name + "/hardware/src")}
    file_type : verilogSource
  sim:
    files:
{get_source_list(OUTPUT_DIR, core.name + "/hardware/simulation/src")}
    file_type : verilogSource

targets:
  default:
    filesets:
      - rtl
  sim:
    toplevel: {core.name}_tb
    description: Simulate the design
    default_tool: icarus
    filesets:
      - rtl
      - sim
"""

    # Write the core description to the .core file
    core_file_path = f"{OUTPUT_DIR}/{core.name}.core"
    with open(core_file_path, "w") as f:
        f.write(core_file_content)

    print(f"FuseSoC core file generated at: {core_file_path}")


def get_source_list(export_path, subdir):
    """Return yaml list of sources in specified subdir of given export_path
    :return: yaml list of verilog sources
    """
    source_path = f"{export_path}/{subdir}"

    sources = ""
    if os.path.isdir(source_path):
        for file in os.listdir(source_path):
            if file.endswith(".v"):
                sources += f"      - {os.path.join(subdir, file)}\n"
            if file.endswith(".vh"):
                sources += f"      - {os.path.join(subdir, file)}: {{is_include_file : true}}\n"

    return sources
