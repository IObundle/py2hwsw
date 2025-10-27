# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
import shutil

import iob_colors

OUTPUT_DIR = "fusesoc_exports"


def export_core(core):
    # Don't try to export if build dir doesn't exist
    if not os.path.exists(core.build_dir):
        # print error and exit
        print(
            f"{iob_colors.FAIL}Build directory not found: {core.build_dir}. Core's build directory must be generated first before exporting.{iob_colors.ENDC}"
        )
        exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Copy build directory to OUTPUT_DIR
    shutil.copytree(core.build_dir, f"{OUTPUT_DIR}/{core.name}")

    core_file_content = f"""\
CAPI=2:

name: iobundle:py2hwsw:{core.name}:{core.version}
description : {core.description}

filesets:
  rtl:
{dependency_list(core)}
    files:
      - {core.name}/hardware/src/{core.name}.v
      - {core.name}/hardware/src/{core.name}_conf.vh: {{is_include_file : true}}
    file_type : verilogSource
  sim:
    files:
      - {core.name}/hardware/simulation/src/{core.name}_tb.v
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


def dependency_list(core):
    """Return yaml list of subblocks for given core"""
    dependencies = ""
    for subblock in core.subblocks:
        dependencies += f"      - {subblock.original_name}\n"

    if dependencies:
        dependencies = "    depend:\n" + dependencies

    return dependencies
