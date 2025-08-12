#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Python3 script to parse directories to search and create lists of files for each combination of the directories
# Example directory combinations:
#  [ hardware/src, hardware/simulation/src ]                            -> The 'base' directory is 'hardware/simulation/src'
#  [ hardware/src, hardware/fpga/src, hardware/fpga/vivado/basys3/ ]    -> The 'base' directory is 'hardware/fpga/vivado/BASYS3/'
#  [ hardware/src, hardware/fpga/src, hardware/fpga/quartus/cyclonev/ ] -> The 'base' directory is 'hardware/fpga/quartus/CYCLONEV/'
#  ...
import os
import sys
import subprocess

import iob_colors

linters = [
    {
        "command": "verilator --lint-only -Wall --timing",
        "include_flag": "-I",
        "config_command": "",
        "config_file": "verilator_config.vlt",
        "waiver_command": "",
        "waiver_file": "verilator_waiver.vlt",
    },
    # {
    #     "command": "svlint",
    #     "include_flag": "-i",
    #     "config_command": "--config",
    #     "config_file": ".svlint.toml",
    #     "waiver_command": "",
    #     "waiver_file": "", # svlint waivers in config file
    # },
]


def lint_files(files_list, extra_flags="", config_path="."):
    """Run Linter on given list of files, while grouping them according to their location in the IObundle standard directory structure."""
    print(f"Linting files: {files_list}", file=sys.stderr)  # DEBUG
    # Group files by their directories
    dir_file_list = {}
    for file in files_list:
        file_dir = os.path.dirname(file)

        if file_dir not in dir_file_list:
            dir_file_list[file_dir] = []

        dir_file_list[file_dir].append(file)

    # print(dir_file_list, file=sys.stderr) #DEBUG

    files_to_lint = {}
    directories_to_lint = {}
    parent_dirs = []
    for child_dir in dir_file_list.keys():
        # print(f"debug: {child_dir}", file=sys.stderr) #DEBUG
        files_to_lint[child_dir] = []
        directories_to_lint[child_dir] = []

        # Find parents of this directory
        for directory, file_list in dir_file_list.items():
            dir_name = directory
            if os.path.basename(directory) == "src":
                dir_name = os.path.dirname(directory)
            elif directory.rstrip("/").endswith("hardware/common_src"):
                dir_name = os.path.dirname(directory)

            # If this directory is a parent (or equal) to the child_dir, add files to the list
            if (
                os.path.commonprefix([dir_name, child_dir]) == dir_name
                and directory != child_dir + "/src"
            ):
                files_to_lint[child_dir] += file_list
                directories_to_lint[child_dir].append(directory)
                # print(f"   {directory}", file=sys.stderr) #DEBUG

                # Add this directory to the list of parent directories if it is not the child
                if directory not in parent_dirs and directory != child_dir:
                    # print(f'PARENT: {directory}', file=sys.stderr)
                    parent_dirs.append(directory)

    # Remove parent directories from dictionary
    for directory in parent_dirs:
        del files_to_lint[directory]
        del directories_to_lint[directory]

    for linter in linters:
        # Lint files for each directory combination
        for directory, files in files_to_lint.items():
            print(
                f'\n{iob_colors.INFO}Linting from base directory "{directory}"{iob_colors.ENDC}'
            )
            linter_cmd = f"{linter['command']}"
            linter_cmd = f"{linter_cmd} {extra_flags}"
            linter_cmd = f"{linter_cmd} {linter['include_flag']}{(' '+linter['include_flag']).join(directories_to_lint[directory])}"
            linter_cmd = f"{linter_cmd} {linter['config_command']} {config_path}/{linter['config_file']}"
            waiver_file = f"{config_path}/{linter['waiver_file']}"
            if linter['waiver_file'] and os.path.exists(waiver_file):
                linter_cmd = f"{linter_cmd} {linter['waiver_command']} {waiver_file}"
            linter_cmd = f"{linter_cmd} {' '.join(files)}"
            print(linter_cmd)
            result = subprocess.run(linter_cmd, shell=True)
            if result.returncode != 0:
                exit(result.returncode)
            print(f"{iob_colors.INFO}Lint successful!{iob_colors.ENDC}")

    # DEBUG: Print child directories and files to lint
    #    print("Base dir: "+directory, file=sys.stderr)
    #    print("Parent dirs: "+directories_to_lint[directory], file=sys.stderr)
    #    print("Files from dirs:"+files, file=sys.stderr)
    #    print("\n", file=sys.stderr)


if __name__ == "__main__":
    files_list = sys.argv[1:]
    lint_files(files_list)
