# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This module copies sources to the build directory
import os
import sys
import subprocess
from pathlib import Path
import shutil
import importlib.util

# IObundle scripts imported:
import iob_colors
from iob_base import nix_permission_hack


def get_lib_dir():
    return os.path.join(os.path.dirname(__file__), "..")


# This function sets up the flows for this core
def flows_setup(python_module):
    # Setup simulation
    sim_setup(python_module)

    # Setup fpga
    fpga_setup(python_module)

    # Setup harware
    hw_setup(python_module)

    lint_setup(python_module)

    syn_setup(python_module)

    # Setup software
    sw_setup(python_module)

    # Setup documentation if it is top module
    doc_setup(python_module)


def hw_setup(python_module):
    # Create module's version TeX file
    if python_module.is_top_module:
        version_file(python_module)


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
CPP_INCLUDES+=-I../../../{python_module.relative_path_to_UUT}/hardware/src

# verilator  flags
""",
        )


# Setup fpga files, but only the ones in the board_list
def fpga_setup(python_module):
    # If board_list is empty, then do nothing
    if not python_module.board_list:
        return

    build_dir = python_module.build_dir
    fpga_dir = "hardware/fpga"
    src_dir = f"{get_lib_dir()}/{fpga_dir}"
    dst_dir = f"{build_dir}/{fpga_dir}"
    tools_list = ["quartus", "vivado"]

    # Copy common fpga files in the fpga_dir (except for the directories in the tools list)
    shutil.copytree(
        src_dir,
        dst_dir,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("*.pdf", "*.py", *tools_list),
    )
    nix_permission_hack(dst_dir)

    if python_module.is_tester:
        # Append UUT's verilog sources in Tester's simulation Makefile
        replace_str_in_file(
            f"{build_dir}/{fpga_dir}/Makefile",
            "VSRC += $(wildcard ../common_src/*.v)",
            f"""\
VSRC += $(wildcard ../common_src/*.v)
#include the UUT's headers and sources
VHDR+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.vh)
VSRC+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.v)
INCLUDE_DIRS+=../../{python_module.relative_path_to_UUT}/hardware/src
""",
        )
        # Replace remote fpga dir
        replace_str_in_file(
            f"{build_dir}/{fpga_dir}/Makefile",
            "REMOTE_FPGA_DIR=$(REMOTE_BUILD_DIR)/hardware/fpga",
            f"REMOTE_FPGA_DIR=$(REMOTE_BUILD_DIR)/{python_module.relative_path_to_tester}/{fpga_dir}",
        )
        # Replace ROOT_DIR for rsync to remote machine
        replace_str_in_file(
            f"{build_dir}/{fpga_dir}/Makefile",
            "-avz --force --delete --exclude 'software/tb' ../..",
            f"-avz --force --delete --exclude 'software/tb' ../../{python_module.relative_path_to_UUT}",
        )

    # Copy LIB fpga directories only if their name is present in the board_list
    for fpga in python_module.board_list:
        for tool in tools_list:
            setup_fpga_dir = os.path.join(src_dir, tool, fpga)
            if os.path.isdir(setup_fpga_dir):
                os.makedirs(os.path.join(dst_dir, tool), exist_ok=True)
                setup_tool_dir = os.path.join(src_dir, tool)
                # Copy only files (not directories) in tool directory
                for file in os.listdir(setup_tool_dir):
                    setup_tool_file = os.path.join(setup_tool_dir, file)
                    dst_file = os.path.join(dst_dir, tool, file)
                    if os.path.isfile(setup_tool_file):
                        shutil.copy2(setup_tool_file, dst_file)
                        nix_permission_hack(dst_file)
                # then copy the fpga directory (excluding 'doc' directory)
                shutil.copytree(
                    setup_fpga_dir,
                    os.path.join(dst_dir, tool, fpga),
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("doc", "*.py"),
                )
                nix_permission_hack(os.path.join(dst_dir, tool, fpga))


def lint_setup(python_module):
    build_dir = python_module.build_dir
    lint_dir = "hardware/lint"

    # Copy LIB lint files
    shutil.copytree(
        f"{get_lib_dir()}/{lint_dir}",
        f"{build_dir}/{lint_dir}",
        dirs_exist_ok=True,
    )
    nix_permission_hack(f"{build_dir}/{lint_dir}")

    # Write header of verilator lint config file
    file_path = f"{build_dir}/{lint_dir}/verilator_config.vlt"
    # create default verilator_config if file does not exist
    if not os.path.isfile(file_path):
        with open(file_path, "w") as file:
            file.write(
                f"""
// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

// Header lines generated by {os.path.basename(__file__)}
`verilator_config
"""
            )

    if python_module.is_tester:
        # Append UUT's verilog sources in Tester's simulation Makefile
        replace_str_in_file(
            f"{build_dir}/{lint_dir}/Makefile",
            "VSRC=$(wildcard ../src/*.v)",
            f"""\
VSRC=$(wildcard ../src/*.v)
#include the UUT's headers and sources
VHDR+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.vh)
VSRC+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.v)
INCLUDE_DIRS+=../../{python_module.relative_path_to_UUT}/hardware/src
""",
        )
        # Replace remote lint dir
        replace_str_in_file(
            f"{build_dir}/{lint_dir}/Makefile",
            "REMOTE_LINT_DIR=$(REMOTE_BUILD_DIR)/hardware/lint",
            f"REMOTE_LINT_DIR=$(REMOTE_BUILD_DIR)/{python_module.relative_path_to_tester}/{lint_dir}",
        )
        # Replace ROOT_DIR for rsync to remote machine
        replace_str_in_file(
            f"{build_dir}/{lint_dir}/Makefile",
            "RSYNC_ROOT_DIR=../..",
            f"RSYNC_ROOT_DIR=../../{python_module.relative_path_to_UUT}",
        )


# synthesis
def syn_setup(python_module):
    build_dir = python_module.build_dir
    syn_dir = "hardware/syn"

    for file in Path(f"{get_lib_dir()}/{syn_dir}").rglob("*"):
        src_file = file.as_posix()
        dest_file = os.path.join(
            build_dir, src_file.replace(get_lib_dir(), "").strip("/")
        )
        if os.path.isfile(src_file):
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copyfile(f"{src_file}", f"{dest_file}")
            nix_permission_hack(dest_file)

    if python_module.is_tester:
        # Append UUT's verilog sources in Tester's simulation Makefile
        replace_str_in_file(
            f"{build_dir}/{syn_dir}/Makefile",
            "VSRC+=$(wildcard ../src/*.v)",
            f"""\
VSRC+=$(wildcard ../src/*.v)
#include the UUT's headers and sources
VHDR+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.vh)
VSRC+=$(wildcard ../../{python_module.relative_path_to_UUT}/hardware/src/*.v)
INCLUDE_DIRS+=../../{python_module.relative_path_to_UUT}/hardware/src
""",
        )
        # Replace remote syn dir
        replace_str_in_file(
            f"{build_dir}/{syn_dir}/Makefile",
            "REMOTE_SYN_DIR=$(REMOTE_BUILD_DIR)/hardware/syn",
            f"REMOTE_SYN_DIR=$(REMOTE_BUILD_DIR)/{python_module.relative_path_to_tester}/{syn_dir}",
        )
        # Replace ROOT_DIR for rsync to remote machine
        replace_str_in_file(
            f"{build_dir}/{syn_dir}/Makefile",
            "-avz --force --delete ../..",
            f"-avz --force --delete ../../{python_module.relative_path_to_UUT}",
        )


# Check if any *_setup.py modules exist (like sim_setup.py, fpga_setup.py, ...).
# If so, get a function to execute them and run them
# This will allow these modules to be executed during setup
#    python_module: python module of *_setup.py of the core/system, should contain setup_dir
#    **kwargs: set of objects that will be accessible from inside the modules when they are executed
def run_setup_functions(python_module, module_type, **kwargs):
    # Check if any *_setup.py modules exist. If so, get a function to execute them and add them to the 'modules' list
    module_path = {
        "sim_setup": "hardware/simulation/sim_setup.py",
        "fpga_setup": "hardware/fpga/fpga_setup.py",
        "sw_setup": "software/sw_setup.py",
        "doc_setup": "document/doc_setup.py",
    }[module_type]
    full_module_path = os.path.join(python_module.setup_dir, module_path)
    if os.path.isfile(full_module_path):
        # Get and run function of this file
        get_module_function(full_module_path, **kwargs)()


# Get an executable function to run a given python module
#    module_path: python module path
#    **kwargs: set of objects that will be accessible from inside the module when it is executed
# Example: get_module_function("sim_setup.py",setup_module=python_module)
def get_module_function(module_path, **kwargs):
    # Create function to execute module if it exists
    def module_function():
        if os.path.isfile(module_path):
            module_name = os.path.basename(module_path).split(".")[0]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            # Define module objects given via kwargs
            for key, value in kwargs.items():
                vars(module)[key] = value
            spec.loader.exec_module(module)

    return module_function


# Setup simulation related files/modules
# module: python module representing a *_setup.py file of the root directory of the core/system.
def sw_setup(python_module):
    build_dir = python_module.build_dir
    setup_dir = python_module.setup_dir

    # os.makedirs(build_dir + "/software/src",
    # Copy LIB software Makefile
    shutil.copytree(
        f"{get_lib_dir()}/software", f"{build_dir}/software", dirs_exist_ok=True
    )
    nix_permission_hack(f"{build_dir}/software")

    # Create 'scripts/' directory
    python_setup(build_dir)


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


def doc_setup(python_module):
    build_dir = python_module.build_dir

    doc_subdirs = ["tsrc", "figures", "doxygen"]
    for subdir in doc_subdirs:
        # Copy LIB tex subdir files if not present
        os.makedirs(f"{build_dir}/document/{subdir}", exist_ok=True)
        for file in os.listdir(f"{get_lib_dir()}/document/{subdir}"):
            shutil.copy2(
                f"{get_lib_dir()}/document/{subdir}/{file}",
                f"{build_dir}/document/{subdir}/{file}",
            )
            nix_permission_hack(f"{build_dir}/document/{subdir}/{file}")

    # Copy document Makefile
    shutil.copy2(f"{get_lib_dir()}/document/Makefile", f"{build_dir}/document/Makefile")
    nix_permission_hack(f"{build_dir}/document/Makefile")

    # General documentation
    write_git_revision_short_hash(f"{build_dir}/document/tsrc")


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


# Include headers and srcs from given python module (module_name)
# headers: List of headers that will be appedend by the list of headers in the .py module.
# srcs: List of srcs that will be appedend by the list of srcs in the .py module.
# module_name: name of the python module to include. Can also be the name of a src module (with the same extension as passed in the module_extension parameter).
# lib_dir: root directory of the LIB
# add_sim_srcs: If True, then the list of simulation sources will be appended to the srcs list
# add_fpga_srcs: If True, then the list of FPGA sources will be appended to the srcs list
# module_parameters: optional argument. Allows passing an optional object with parameters to a hardware module.
# module_extension: Select module file extension (.v for hardware, .c for software)
def lib_module_setup(
    headers,
    srcs,
    module_name,
    lib_dir=get_lib_dir(),
    add_sim_srcs=False,
    add_fpga_srcs=False,
    module_parameters=None,
    module_extension=".v",
):
    module_path = None

    # Search for module_name.py
    for mod_path in Path(lib_dir).rglob(f"{module_name}.py"):
        module_path = mod_path
        break
    # If module_name.py is not found, search for module_name.module_extension
    if not module_path:
        for mod_path in Path(lib_dir).rglob(f"{module_name}{module_extension}"):
            module_path = mod_path
            break
    # Exit if module is not found
    if not module_path:
        sys.exit(
            f"{iob_colors.FAIL} {module_name} is not a LIB module.{iob_colors.ENDC}"
        )

    extension = os.path.splitext(module_path)[1]
    # If module_name.py is found, import the headers and srcs lists from it
    if extension == ".py":
        lib_module_name = os.path.basename(module_path).split(".")[0]
        spec = importlib.util.spec_from_file_location(lib_module_name, module_path)
        lib_module = importlib.util.module_from_spec(spec)
        sys.modules[lib_module_name] = lib_module
        if module_parameters:
            lib_module.module_parameters = module_parameters
        spec.loader.exec_module(lib_module)
        headers.extend(lib_module.headers)
        srcs.extend(lib_module.modules)
        if add_sim_srcs and (
            hasattr(lib_module, "sim_headers") and hasattr(lib_module, "sim_modules")
        ):
            headers.extend(lib_module.sim_headers)
            srcs.extend(lib_module.sim_modules)
        if add_fpga_srcs and (
            hasattr(lib_module, "fpga_headers") and hasattr(lib_module, "fpga_modules")
        ):
            headers.extend(lib_module.fpga_headers)
            srcs.extend(lib_module.fpga_modules)
    # If module_name.module_extension is found, add it to the srcs list
    elif extension == module_extension:
        srcs.append(f"{module_name}{module_extension}")


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


# Create TeX files with the version of the core
def version_file(
    python_module,
    create_version_header=True,
):
    core_name = python_module.name
    core_version = python_module.version
    core_previous_version = python_module.previous_version
    build_dir = python_module.build_dir

    tex_dir = f"{build_dir}/document/tsrc"
    verilog_dir = f"{build_dir}/hardware/src"

    os.makedirs(tex_dir, exist_ok=True)
    tex_file = f"{tex_dir}/{core_name}_version.tex"
    with open(tex_file, "w") as tex_f:
        tex_f.write(core_version)
    tex_file = f"{tex_dir}/{core_name}_previous_version.tex"
    with open(tex_file, "w") as tex_f:
        tex_f.write(core_previous_version)


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
        # print(f"### DEBUG: {src} {dst}", file=sys.stderr)
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

def copytree_with_rename(src, dst, original_name, new_name, ignore=None, symlinks=False):
    """
    Recursively copy a directory tree from src to dst, while renaming any 'original_name' strings to 'new_name'.
    Any directories or files containing 'original_name' in their name will be renamed to 'new_name'.
    Any strings inside the copied files containing 'original_name' will be replaced by 'new_name'.

    Parameters:
        src (str): Source directory path.
        dst (str): Destination directory path.
        original_name (str): The string to replace.
        new_name (str): The replacement string.
        ignore (callable): A function that takes a directory path and list of its contents,
                           and returns a set of names to ignore (like shutil.ignore_patterns).
                           Example: shutil.ignore_patterns('*.pyc', 'tmp*').
        symlinks (bool): Whether to copy symlinks as symlinks (True) or file contents (False).
    """
    if not os.path.isdir(src):
        raise ValueError(f"Source directory {src} does not exist or is not a directory")

    # If dst folder contains the original_name, rename it to new_name
    dst = os.path.join(os.path.dirname(dst), os.path.basename(dst).replace(original_name, new_name).replace(original_name.upper(), new_name.upper()))
    os.makedirs(dst, exist_ok=True)

    entries = os.listdir(src)
    ignored_names = set()
    if ignore:
        ignored_names = set(ignore(src, entries))

    for entry in entries:
        if entry in ignored_names:
            continue

        s = os.path.join(src, entry)
        d = os.path.join(dst, entry)

        if symlinks and os.path.islink(s):
            linkto = os.readlink(s)
            os.symlink(linkto, d)
        elif os.path.isdir(s):
            copytree_with_rename(s, d, original_name, new_name, ignore=ignore, symlinks=symlinks)
        else:
            copy_with_rename(original_name, new_name)(s, d)

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
                os.path.join(core.setup_dir, f"{core.original_name}.v"),
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
        copytree_with_rename(
            os.path.join(core.setup_dir, directory),
            os.path.join(core.build_dir, directory),
            core.original_name, core.name,
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
                    os.makedirs(build_tools_dir, exist_ok=True)
                    # Copy the tools directory files only
                    for file in os.listdir(setup_tools_dir):
                        setup_file = os.path.join(setup_tools_dir, file)
                        if os.path.isfile(setup_file):
                            copy_with_rename(core.name, core.name)(
                                setup_file,
                                os.path.join(build_tools_dir, file),
                            )
                    # Copy the fpga directory
                    copytree_with_rename(
                        setup_fpga_dir,
                        build_fpga_dir,
                        core.original_name, core.name,
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
    elif directory == "software" and core.dest_dir.startswith("hardware/simulation"):
        # Copy software sources into 'software/simulation' directory, if the core has a destination dir somewhere inside the hardware/simulation folder.
        dst_directory = "software/simulation"
    else:
        dst_directory = directory

    # Copy tree of this directory, renaming directories/files, and overriding destination ones.
    copytree_with_rename(
        os.path.join(core.setup_dir, directory),
        os.path.join(core.build_dir, dst_directory),
        core.original_name, core.name,
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
            "hardware/fpga",
            "hardware/syn",
            "hardware/lint",
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
