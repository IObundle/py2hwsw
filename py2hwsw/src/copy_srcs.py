# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This module copies sources to the build directory
import os
import subprocess
from pathlib import Path
import shutil

# IObundle scripts imported:
import iob_colors
from iob_base import nix_permission_hack


def get_lib_dir():
    return os.path.join(os.path.dirname(__file__), "..")


# This function sets up the flows for this core
def flows_setup(python_module):
    # Setup simulation
    sim_setup(python_module)

    # Setup py2 scripts
    python_setup(python_module.build_dir)


# Setup simulation related files/modules
# module: python module representing a *_setup.py file of the root directory of the core/system.
def sim_setup(python_module):
    build_dir = python_module.build_dir

    sim_dir = "hardware/simulation"

    # Copy LIB sim files
    shutil.copytree(
        f"{get_lib_dir()}/{sim_dir}",
        f"{build_dir}/{sim_dir}",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("*.pdf", "*.py"),
    )
    nix_permission_hack(f"{build_dir}/{sim_dir}")

    if python_module.is_tester:
        # Append UUT's verilog sources in Tester's simulation Makefile
        replace_str_in_file(
            f"{build_dir}/{sim_dir}/Makefile",
            "VSRC+=$(wildcard ../src/*.v)",
            f"""\
VSRC+=$(wildcard ../src/*.v)
#include the UUT's headers and sources
VHDR+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.vh)
VSRC+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.v)
INCLUDE_DIRS+=../../{python_module.relative_path_to_UUT}/hardware/src
""",
        )
        # Replace remote simulation dir
        replace_str_in_file(
            f"{build_dir}/{sim_dir}/Makefile",
            "REMOTE_SIM_DIR=$(REMOTE_BUILD_DIR)/hardware/simulation",
            f"REMOTE_SIM_DIR=$(REMOTE_BUILD_DIR)/{python_module.relative_path_to_tester}/{sim_dir}",
        )
        # Replace ROOT_DIR for rsync to remote machine
        replace_str_in_file(
            f"{build_dir}/{sim_dir}/Makefile",
            "-avz --force --delete --exclude 'software/tb' ../..",
            f"-avz --force --delete --exclude 'software/tb' ../../{python_module.relative_path_to_UUT}",
        )
        # Append UUT's verilog paths in verilator.mk includes
        replace_str_in_file(
            f"{build_dir}/{sim_dir}/verilator.mk",
            "# verilator  flags",
            f"""\
#include the UUT's headers
VLTINCLUDES+=-I../../{python_module.relative_path_to_UUT}/hardware/src

# verilator  flags
""",
        )


def python_setup(build_dir):
    dest_dir = f"{build_dir}/scripts"
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    copy_files(get_lib_dir(), dest_dir, ["iob_colors.py"], "*.py")
    for file in [
        "board_client.py",
        "console.py",
        "console_ethernet.py",
        "makehex.py",
        "hex_join.py",
    ]:
        shutil.copy(f"{get_lib_dir()}/scripts/{file}", f"{dest_dir}/{file}")
        os.chmod(f"{dest_dir}/{file}", 0o755)


def write_git_revision_short_hash(dst_dir):
    file_name = "shortHash.tex"
    setup_dir_file = os.path.join(os.path.dirname(__file__), "..", file_name)
    # Use the shortHash.tex from the setup directory if it exists
    # This file is present in pip installations (cannot use git rev-parse in pip installations)
    if os.path.isfile(setup_dir_file):
        shutil.copy2(
            setup_dir_file,
            f"{dst_dir}/{file_name}",
        )
        nix_permission_hack(f"{dst_dir}/{file_name}")
        return

    # Alternatively generate short hash based on git command
    text = (
        subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=os.path.dirname(__file__)
        )
        .decode("ascii")
        .strip()
    )

    if not (os.path.exists(dst_dir)):
        os.makedirs(dst_dir)
    with open(f"{dst_dir}/{file_name}", "w") as file:
        file.write(text)


def copy_files(src_dir, dest_dir, sources=[], pattern="*", copy_all=False):
    files_copied = []
    print(src_dir)
    if (sources != []) or copy_all:
        os.makedirs(dest_dir, exist_ok=True)
        for path in Path(src_dir).rglob(pattern):
            file = path.name
            if (file in sources) or copy_all:
                src_file = path.resolve()
                dest_file = f"{dest_dir}/{file}"
                if os.path.isfile(src_file) and (
                    not (os.path.isfile(dest_file))
                    or (os.stat(src_file).st_mtime < os.stat(dest_file).st_mtime)
                ):
                    shutil.copy(src_file, dest_file)
                    nix_permission_hack(dest_file)
                    files_copied.append(file)
                elif not (os.path.isfile(src_file)):
                    print(
                        f"{iob_colors.WARNING}{src_file} is not a file.{iob_colors.ENDC}"
                    )
                else:
                    print(
                        f"{iob_colors.INFO}Not copying file. File in build directory is newer than the one in the source directory.{iob_colors.ENDC}"
                    )
    else:
        print(
            f"{iob_colors.WARNING}'copy_files' function did nothing.{iob_colors.ENDC}"
        )
    return files_copied


def copy_with_rename(old_core_name, new_core_name):
    """Creates a function that:
    - Renames any '<old_core_name>' string inside the src file and in its filename,
    to the given '<new_core_name>' string argument.
    """

    def copy_func(src, dst):
        # Add write permission due to Nix hack
        nix_permission_hack(os.path.dirname(dst))
        dst = os.path.join(
            os.path.dirname(dst),
            os.path.basename(
                dst.replace(old_core_name, new_core_name).replace(
                    old_core_name.upper(), new_core_name.upper()
                )
            ),
        )
        try:
            file_perms = os.stat(src).st_mode
            with open(src, "r") as file:
                lines = file.readlines()
            for idx in range(len(lines)):
                lines[idx] = (
                    lines[idx]
                    .replace(old_core_name, new_core_name)
                    .replace(old_core_name.upper(), new_core_name.upper())
                )
            with open(dst, "w") as file:
                file.writelines(lines)
        except Exception:
            shutil.copyfile(src, dst)
        # Set file permissions equal to source file
        # and add write permission due to Nix hack
        os.chmod(dst, file_perms | 0o200)

    return copy_func


def copy_rename_setup_subdir(core, directory, exclude_file_list=[]):
    """Copy and rename files from a given setup subdirectory to the build directory
    :param core: The core object
    :param directory: The directory to copy
    :param exclude_file_list: List of wildcards for files to exclude
    """
    # Skip this directory if it does not exist
    if not os.path.isdir(os.path.join(core.setup_dir, directory)):
        return

    # If we are handling the `hardware/src` directory,
    # copy to the correct destination based on 'dest_dir' attribute.
    if directory == "hardware/src":
        dst_directory = core.dest_dir
        if core.use_netlist:
            # copy SETUP_DIR/CORE.v netlist instead of
            # SETUP_DIR/hardware/src
            shutil.copyfile(
                os.path.join(core.setup_dir, f"{core.name}.v"),
                os.path.join(core.build_dir, dst_directory, f"{core.name}.v"),
            )
            nix_permission_hack(os.path.join(core.build_dir, dst_directory))
            return
    elif directory == "hardware/fpga":
        # Skip if board_list is empty
        if not core.board_list:
            return

        tools_list = ["quartus", "vivado"]

        # Copy everything except the tools directories
        shutil.copytree(
            os.path.join(core.setup_dir, directory),
            os.path.join(core.build_dir, directory),
            dirs_exist_ok=True,
            copy_function=copy_with_rename(core.original_name, core.name),
            ignore=shutil.ignore_patterns(*exclude_file_list, *tools_list),
        )

        # if it is the fpga directory, only copy the directories in the cores board_list
        for fpga in core.board_list:
            # search for the fpga directory in the cores setup_dir/hardware/fpga
            # in both quartus and vivado directories
            for tools_dir in tools_list:
                setup_tools_dir = os.path.join(core.setup_dir, directory, tools_dir)
                build_tools_dir = os.path.join(core.build_dir, directory, tools_dir)
                setup_fpga_dir = os.path.join(setup_tools_dir, fpga)
                build_fpga_dir = os.path.join(build_tools_dir, fpga)

                # if the fpga directory is found, copy it to the build_dir
                if os.path.isdir(setup_fpga_dir):
                    # Copy the tools directory files only
                    for file in os.listdir(setup_tools_dir):
                        setup_file = os.path.join(setup_tools_dir, file)
                        if os.path.isfile(setup_file):
                            copy_with_rename(core.name, core.name)(
                                setup_file,
                                os.path.join(build_tools_dir, file),
                            )
                    # Copy the fpga directory
                    shutil.copytree(
                        setup_fpga_dir,
                        build_fpga_dir,
                        dirs_exist_ok=True,
                        copy_function=copy_with_rename(core.original_name, core.name),
                        ignore=shutil.ignore_patterns(*exclude_file_list),
                    )
                    break
            else:
                print(
                    f"Note: The setup FPGA directory '{fpga}' not found in subdirectories of '{core.setup_dir}/hardware/fpga/'"
                )

        nix_permission_hack(os.path.join(core.build_dir, directory))
        # No need to copy any more files in this directory
        return

    else:
        dst_directory = directory

    # Copy tree of this directory, renaming files, and overriding destination ones.
    # Note: The `copy_with_rename` may throw errors when
    #       trying to rename binary files from the doc dir.
    #       The main branch used a dedicated script to copy doc files
    #       without renaming them. Maybe here we should try to
    #       implement it with a try catch block.
    shutil.copytree(
        os.path.join(core.setup_dir, directory),
        os.path.join(core.build_dir, dst_directory),
        dirs_exist_ok=True,
        copy_function=copy_with_rename(core.original_name, core.name),
        ignore=shutil.ignore_patterns(*exclude_file_list),
    )
    nix_permission_hack(os.path.join(core.build_dir, dst_directory))


def copy_rename_setup_directory(core, exclude_file_list=["*.py"]):
    """Copy and rename files from the module's setup dir.
    Any string from the files in the setup dir that matches the
    module's class name (core.original_name) will be replaced by the
    module's name (core.name).
    For example, if we create a new IOb-SoC module with
    `iob_soc(name="iob_soc_sut")` then the `iob_soc.v` file from
    the iob-soc setup dir will have all instances of the string 'iob_soc'
    replaced with the new string 'iob_soc_sut'.

    :param list exclude_file_list: list of strings, each string representing an ignore pattern for the source files.
                                   For example, using the ignore pattern '*.v' would prevent from copying every Verilog source file.
                                   Note, if want to ignore a file that is going to be renamed with the new core name,
                                   we would still use the old core name in the ignore patterns.
                                   For example, if we dont want it to generate the 'new_name_firmware.c' based on the 'old_name_firmware.c',
                                   then we should add 'old_name_firmware.c' to the ignore list.
    """

    # Files that should always be copied
    dir_list = [
        "hardware/src",
        "software",
    ]
    # Files that should only be copied if it is top module
    if core.is_top_module or core.is_tester:
        dir_list += [
            "hardware/simulation",
            "hardware/common_src",
            "document",
        ]

    # Copy sources
    for directory in dir_list:
        copy_rename_setup_subdir(core, directory, exclude_file_list)

    # Copy custom_config_build.mk file if it exists
    if os.path.isfile(os.path.join(core.setup_dir, "custom_config_build.mk")):
        shutil.copyfile(
            os.path.join(core.setup_dir, "custom_config_build.mk"),
            os.path.join(core.build_dir, "custom_config_build.mk"),
        )


def replace_str_in_file(file_path, old_str, new_str):
    """Replace string old_str with new_str in file_path
    :param file_path: Path of the file to be modified
    :param old_str: The string to be replaced
    :param new_str: The new string
    """
    # Read in the file
    with open(file_path) as f:
        file_str = f.read()

    # Replace all occurrences
    new_file_str = file_str.replace(old_str, new_str)

    with open(file_path, "w") as f:
        f.write(new_file_str)
