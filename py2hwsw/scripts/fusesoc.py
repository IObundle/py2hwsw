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
    This function expects the build directory for the core to have been generated previously.
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

    tb_top = f"{core.name}_tb"
    sim_cmd = "make run"
    console_cmd = ""
    # Check if core contains Py2HWSW's universal testbench
    if os.path.isfile(f"{OUTPUT_DIR}/{core.name}/hardware/simulation/src/iob_v_tb.v"):
        tb_top = "iob_v_tb"
        sim_cmd = f"./src/iobundle_py2hwsw_{core.name}_{core.version}/{core.name}/software/tb & make run && (kill $$! >/dev/null 2>&1; true) || (kill $$! >/dev/null 2>&1; false)"

    has_software = False
    if os.path.isdir(f"{OUTPUT_DIR}/{core.name}/software"):
        has_software = True

    # console_cmd = "rm -f soc2cnsl cnsl2soc; ../../scripts/console.py -L"

    core_file_content = f"""\
CAPI=2:

name: iobundle:py2hwsw:{core.name}:{core.version}
license: {core.license.name}
description: "{core.description}"

filesets:
  rtl:
    files:
{get_source_list(OUTPUT_DIR, core.name + "/hardware/src", source_extensions=['.v'], header_extensions=['.vh'])}\
    file_type : verilogSource
  sim:
    files:
{get_source_list(OUTPUT_DIR, core.name + "/hardware/simulation/src", source_extensions=['.v'], header_extensions=['.vh'])}\
    file_type : verilogSource
  scripts:
    files:
{get_source_list(OUTPUT_DIR, core.name + "/scripts", source_extensions=['.py'])}\
"""
    if has_software:
        core_file_content += f"""\
  sw:
    files:
      - {core.name}/config_build.mk
{get_all_files(OUTPUT_DIR, core.name + "/software")}\
"""
    core_file_content += f"""

targets:
"""
    if tb_top == "iob_v_tb": # Universal Testbench (with board_client.py and parallel processes)
        core_file_content += f"""\
  default:
    toplevel: {tb_top}
    description: Simulate the design.
    # Generic flow only runs the build step by default.
    flow: generic
    flow_options:
      tool: icarus
      iverilog_options:
        - -W
        - all
        - -g2005-sv
    filesets:
      - rtl
      - sim
    hooks:
      post_build:
{"        - sw_build\n" if has_software else ""}\
        - clean
        - board_client
"""
    else: # Standard testbench (no parallel processes nor board_client.py)
        core_file_content += f"""\
  default:
    description: Simulate the design.
    filesets:
      - rtl
"""
    core_file_content += f"""
scripts:
"""
    if tb_top == "iob_v_tb": # Universal Testbench
        core_file_content += f"""\
  clean:
    cmd:
      - rm
      - -f
      - c2v.txt
      - v2c.txt

"""
    if has_software:
        core_file_content += f"""
  sw_build:
    cmd:
      - make
      - -C
      - src/iobundle_py2hwsw_{core.name}_{core.version}/{core.name}/software
      - build
      #- USE_FPGA=$(USE_FPGA)
    filesets:
      - sw

"""

    if tb_top == "iob_v_tb": # Universal Testbench
        # Maybe there is a way to import variables from sim_build.mk (like GRAB_TIMEOUT)?
        core_file_content += f"""\
  board_client:
    cmd:
      - src/iobundle_py2hwsw_{core.name}_{core.version}/{core.name}/scripts/board_client.py
      - grab
      - "300"
      - -s
      #run the C testbench in background and kill it when simulator exits
      - "'{sim_cmd}'"
"""
        if console_cmd:
            core_file_content += f"""\
      - -c
      #run the console
      - {console_cmd}
"""
        core_file_content += f"""\
    filesets:
      - scripts
"""

    # Write the core description to the .core file
    core_file_path = f"{OUTPUT_DIR}/{core.name}.core"
    with open(core_file_path, "w") as f:
        f.write(core_file_content)

    print(f"FuseSoC core file generated at: {core_file_path}")


def get_source_list(export_path, subdir, source_extensions=[], header_extensions=[]):
    """Return yaml list of sources in specified subdir of given export_path
    :return: yaml list of verilog sources
    """
    source_path = f"{export_path}/{subdir}"

    sources = ""
    if os.path.isdir(source_path):
        for file in os.listdir(source_path):
            if any(file.endswith(ext) for ext in header_extensions):
                sources += f"      - {os.path.join(subdir, file)}: {{is_include_file : true}}\n"
            elif any(file.endswith(ext) for ext in source_extensions):
                sources += f"      - {os.path.join(subdir, file)}\n"

    return sources


def get_all_files(export_path, subdir):
    """Return yaml list of all files (recursively) in specified subdir of given export_path
    :return: yaml list of files
    """
    search_path = f"{export_path}/{subdir}"

    yaml_files = ""
    for root, dirs, files in os.walk(search_path):
        for file in files:
            yaml_files += (
                f"      - {os.path.join(os.path.relpath(root, export_path), file)}\n"
            )

    return yaml_files
