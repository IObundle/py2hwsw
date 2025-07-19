# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import importlib
import os
import shutil
from pathlib import Path
import pathlib

import iob_colors

import copy_srcs

import config_gen
import param_gen
import io_gen
import bus_gen
import block_gen
import comb_gen
import fsm_gen
import snippet_gen
import doc_gen
import verilog_gen
import ipxact_gen

from iob_base import (
    fail_with_msg,
    find_file,
    nix_permission_hack,
    update_obj_from_dict,
    parse_short_notation_text,
)
from api_base import internal_api_class, convert2internal
from py2hwsw_version import PY2HWSW_VERSION
from iob_module import iob_module
import sw_tools
import verilog_format
import verilog_lint
from manage_headers import generate_headers

from iob_conf import conf_from_dict
from iob_wire import iob_global_wire
from iob_port import port_from_dict
from iob_bus import bus_from_dict
from iob_snippet import snippet_from_dict
from iob_python_parameter import python_parameter_group_from_dict


@internal_api_class("user_api.api", "iob_core", allow_unknown_args=True)
class iob_core(iob_module):
    """Generic class to describe how to generate a base IOb IP core"""

    # List of global wires. Similar concept to 'netlist' in HDL terminology: https://vhdlwhiz.com/terminology/net/#net
    global_wires: list[iob_global_wire] = []
    # Project settings
    global_build_dir: str = ""
    global_project_root: str = "."
    global_project_vformat: bool = True
    global_project_vlint: bool = True
    # Project wide special target. Used when we don't want to run normal setup (for example, when cleaning).
    global_special_target: str = ""
    # Clang format rules
    global_clang_format_rules_filepath: str = None
    # List of callbacks to run at post setup stage
    global_post_setup_callbacks: list = []

    def __init__(self, core_dictionary: dict = {}):
        """
        Constructor of IP core.

        Attributes:
            core_dictionary (dict): Dictionary to initialize core attributes.
                                    Supports the same keys as the ones supported by the API's `create_core_from_dict()` method, except for `core` and `python_parameters`. The `core` and `python_parameters` keys are only used to instantiate other user-defined/lib cores (not iob_core directly).
        """

        # Inherit attributes from superclasses
        iob_module.__init__(self)

        # For debug:
        # print("Iob-core: called")
        # print("Iob-core attributes:", self.__class__.__annotations__)

        # Set internal attributes
        "Selects if core is top module."
        self.is_top_module = __class__.global_top_module == self
        "Selects if core is superblock of another."
        self.is_superblock = False # FIXME: Auto fill
        "Store reference to the issuer block."
        self.issuer = None # FIXME: Auto fill
        "Selects if core is parent of another."
        self.is_parent = False # FIXME: Do we still need this?

        # API attributes with automatic default values
        # self.previous_version = self.version # FIXME: Should this be updated later? (For example, if version is changed afterwards?)

        # Update current core's attributes with values from given core_dictionary
        if core_dictionary:
            # Lazy import instance to avoid circular dependecy
            instance_from_dict = getattr(importlib.import_module('iob_instance'), 'instance_from_dict')
            # Sanity check. These keys are only used to instantiate other user-defined/lib cores. Not iob_core directly.
            if "core" in core_dictionary or "python_parameters" in core_dictionary:
                fail_with_msg("The 'core' and 'python_parameters' keys cannot be used in core dictionaries passed directly to the core constructor!")
            # Convert core dictionary elements to objects
            core_dict_with_objects = core_dictionary.copy()
            for c in core_dictionary.get("confs", []):
                if "type" in c:
                    breakpoint()
            core_dict_with_objects["confs"] = [conf_from_dict(i) for i in core_dictionary.get("confs", [])]
            core_dict_with_objects["ports"] = [port_from_dict(i) for i in core_dictionary.get("ports", [])]
            core_dict_with_objects["buses"] = [bus_from_dict(i) for i in core_dictionary.get("buses", [])]
            core_dict_with_objects["snippets"] = [snippet_from_dict(i) for i in core_dictionary.get("snippets", [])]
            core_dict_with_objects["subblocks"] = [instance_from_dict(i) for i in core_dictionary.get("subblocks", [])]
            core_dict_with_objects["superblocks"] = [core_from_dict(i) for i in core_dictionary.get("superblocks", [])]
            core_dict_with_objects["sw_modules"] = [core_from_dict(i) for i in core_dictionary.get("sw_modules", [])]
            core_dict_with_objects["python_parameters"] = [python_parameter_group_from_dict(i) for i in core_dictionary.get("python_parameters", [])]
            update_obj_from_dict(self, core_dict_with_objects, valid_attributes_list=self.get_api_obj().get_supported_attributes().keys())

        # Set global build directory
        if self.is_top_module:
            # FIXME: Ideally make this copy by reference, so that updates to the top's build dir are reflected across all cores
            __class__.global_build_dir = self.build_dir

        # Get name of (user's) subclass that is inheriting from iob_core
        subclass_name=type(self.get_api_obj()).__name__
        # Auto-fill original_name based on user subclass's name (if any). May not have subclass if defined via JSON or direct constructor call.
        if not self.original_name and subclass_name != "iob_core":
            self.original_name = subclass_name

        # Try to find core's setup directory based on original name (try to find .py and .json files for it)
        core_dir, _ = find_module_setup_dir(self.original_name, error_on_not_found=False)
        # Auto-fill setup_dir based on found core directory.
        if not self.setup_dir and core_dir:
            self.setup_dir = core_dir

        # Use original name as default name
        self.name = self.name or self.original_name

        return

    def generate_build_dir(self, **kwargs):
        self.validate_attributes()

        # Delete existing old build directory
        if self.is_top_module:
            clean_build_dir(self.build_dir)

        self.__create_build_dir()

        # Generate build dir of subblocks
        for subblock in self.subblocks:
            if self.is_superblock:
                if subblock.original_name == self.issuer.original_name:
                    # skip build dir generation for issuer subblocks
                    continue
            subblock.get_core().generate_build_dir()

        # Generate build dir of superblocks. Ensure superblocks are set up only for top module (or wrappers of it)
        if self.is_top_module or self.is_superblock:
            for superblock in self.superblocks:
                superblock.generate_build_dir()

        if self.is_tester:
            # FIXME: Tester hack? Is this still needed?
            self.relative_path_to_UUT = os.path.relpath(
                __class__.global_build_dir, self.build_dir
            )

        # Copy files from LIB to setup various flows
        # (should run before copy of files from module's setup dir)
        if self.is_top_module or self.is_tester:
            copy_srcs.flows_setup(self)

        # Copy files from the module's setup dir
        # FIXME: Setup dir needs to be defined for top module!
        copy_srcs.copy_rename_setup_directory(self)

        # Generate config_build.mk
        if self.is_top_module or self.is_tester:
            config_gen.config_build_mk(self, __class__.global_top_module)

        # Generate configuration files
        config_gen.generate_confs(self)

        # Generate parameters
        param_gen.generate_params_snippets(self)

        # Generate ios
        io_gen.generate_ports_snippet(self)

        # Generate buses
        bus_gen.generate_buses_snippet(self)

        # Generate instances
        if self.generate_hw:
            block_gen.generate_subblocks_snippet(self)

        # Generate comb
        comb_gen.generate_comb_snippet(self)

        # Generate fsm
        fsm_gen.generate_fsm_snippet(self)

        # Generate snippets
        snippet_gen.generate_snippets_snippet(self)

        # Generate main Verilog module
        if self.generate_hw:
            verilog_gen.generate_verilog(self)

        if (self.is_top_module and not self.is_parent) or self.is_tester:
            self.post_setup()

    ##############################################################################
    #
    # Other non-API methods
    #
    ##############################################################################

    def validate_attributes(self):
        if not self.original_name:
            fail_with_msg(f"Original name is not defined for core {self}", ValueError)
        if not self.name:
            fail_with_msg(f"Name is not defined for core {self.original_name}", ValueError)
        if not self.setup_dir:
            fail_with_msg(f"Setup directory is not defined for core {self.original_name}", ValueError)
        if not self.build_dir:
            fail_with_msg(f"Build directory is not defined for core {self.original_name}", ValueError)
        pass

    def post_setup(self):
        """Scripts to run at the end of the top module's setup"""
        # Replace Verilog snippet includes
        self.__replace_snippet_includes()
        # Clean duplicate sources in `hardware/src` and its subfolders (like `hardware/simulation/src`)
        self.__remove_duplicate_sources()
        if self.is_tester:
            # Add callback to: Remove duplicate sources from tester dirs, that already exist in UUT's `hardware/src` folder
            __class__.global_post_setup_callbacks.append(
                lambda: self.__remove_duplicate_sources(
                    main_folder=os.path.join(self.relative_path_to_UUT, "hardware/src"),
                    subfolders=[
                        "hardware/src",
                        "hardware/simulation/src",
                        "hardware/fpga/src",
                        "hardware/common_src",
                    ],
                )
            )
        else:  # Not tester
            # Run post setup callbacks
            for callback in __class__.global_post_setup_callbacks:
                callback()
        # Generate docs
        doc_gen.generate_docs(self)
        # Generate ipxact file

        # FIXME: IPXACT disabled during wires/buses/global_wires/ports/interfaces rework
        #ipxact_gen.generate_ipxact_xml(self, self.build_dir + "/ipxact")

        # Remove 'iob_v_tb.v' from build dir if 'iob_v_tb.vh' does not exist
        sim_src_dir = "hardware/simulation/src"
        if "iob_v_tb.vh" not in os.listdir(os.path.join(self.build_dir, sim_src_dir)):
            os.remove(f"{self.build_dir}/{sim_src_dir}/iob_v_tb.v")
        # Lint and format sources
        self.lint_and_format()
        print(
            f"{iob_colors.INFO}Setup of '{self.original_name}' core successful. Generated build directory: '{self.build_dir}'.{iob_colors.ENDC}"
        )
        # Add SPDX license headers to every file in build dir
        custom_header = f"Py2HWSW Version {PY2HWSW_VERSION} has generated this code (https://github.com/IObundle/py2hwsw)."
        lic = convert2internal(self.license)
        generate_headers(
            root=self.build_dir,
            copyright_holder=lic.author,
            copyright_year=lic.year,
            license_name=lic.name,
            header_template="spdx",
            custom_header_suffix=custom_header,
            skip_existing_headers=True,
            verbose=False,
        )

    def __create_build_dir(self):
        """Create minimal build directory if it doesn't exist"""
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(os.path.join(self.build_dir, self.dest_dir), exist_ok=True)

        os.makedirs(f"{self.build_dir}/document", exist_ok=True)
        os.makedirs(f"{self.build_dir}/document/tsrc", exist_ok=True)

        shutil.copyfile(
            f"{copy_srcs.get_lib_dir()}/build.mk", f"{self.build_dir}/Makefile"
        )
        nix_permission_hack(f"{self.build_dir}/Makefile")

    def __remove_duplicate_sources(self, main_folder="hardware/src", subfolders=None):
        """Remove sources in the build directory from subfolders that exist in `hardware/src`"""
        if not subfolders:
            subfolders = [
                "hardware/simulation/src",
                "hardware/fpga/src",
                "hardware/common_src",
            ]

        # Go through all subfolders that may contain duplicate sources
        for subfolder in subfolders:
            # Get common srcs between main_folder and current subfolder
            common_srcs = find_common_deep(
                os.path.join(self.build_dir, main_folder),
                os.path.join(self.build_dir, subfolder),
            )
            # Remove common sources
            for src in common_srcs:
                os.remove(os.path.join(self.build_dir, subfolder, src))
                # print(f'{iob_colors.INFO}Removed duplicate source: {os.path.join(subfolder, src)}{iob_colors.ENDC}')

    def __replace_snippet_includes(self):
        verilog_gen.replace_includes(
            self.setup_dir, self.build_dir, self.ignore_snippets
        )

    def lint_and_format(self):
        """Run Linters and Formatters in setup and build directories."""
        # Find Verilog sources and headers from build dir
        verilog_headers = []
        verilog_sources = []
        for path in Path(os.path.join(self.build_dir, "hardware")).rglob("*.vh"):
            # Skip specific Verilog headers
            if "test_" in path.name:
                continue
            # Skip synthesis directory # TODO: Support this?
            if "/syn/" in str(path):
                continue
            verilog_headers.append(str(path))
            # print(str(path))
        for path in Path(os.path.join(self.build_dir, "hardware")).rglob("*.v"):
            # Skip synthesis directory # TODO: Support this?
            if "/syn/" in str(path):
                continue
            verilog_sources.append(str(path))
            # print(str(path))

        # Run Verilog linter
        # FIXME: Don't run for tester since iob_system is still full of warnings (and we may not even need to lint tester files?)
        if __class__.global_project_vlint and not self.is_tester:
            verilog_lint.lint_files(verilog_headers + verilog_sources)

        # Run Verilog formatter
        if __class__.global_project_vformat:
            verilog_format.format_files(
                verilog_headers + verilog_sources,
                os.path.join(os.path.dirname(__file__), "verible-format.rules"),
            )

        # Run Python formatter
        sw_tools.run_tool("black")
        sw_tools.run_tool("black", self.build_dir)

        # Run C formatter
        sw_tools.run_tool(
            "clang", rules_file_path=__class__.global_clang_format_rules_filepath
        )
        sw_tools.run_tool(
            "clang",
            self.build_dir,
            rules_file_path=__class__.global_clang_format_rules_filepath,
        )

#
# Non iob_core methods
#

def find_common_deep(path1, path2):
    """Find common files (recursively) inside two given directories
    Taken from: https://stackoverflow.com/a/51625515
    :param str path1: Directory path 1
    :param str path2: Directory path 2
    """
    return set.intersection(
        *(
            set(
                os.path.relpath(os.path.join(root, file), path)
                for root, _, files in os.walk(path)
                for file in files
            )
            for path in (path1, path2)
        )
    )

def find_module_setup_dir(core_name, error_on_not_found=True):
    """Searches for a core's setup directory
    param core_name: The core_name object
    returns: The path to the setup directory
    returns: The file extension
    """
    file_path = find_file(
        iob_core.global_project_root, core_name, [".py", ".json"]
    ) or find_file(
        os.path.join(os.path.dirname(__file__), ".."),
        core_name,
        [".py", ".json"],
    )
    if not file_path:
        if error_on_not_found:
            fail_with_msg(
                f"Python/JSON setup file of '{core_name}' core not found under path '{iob_core.global_project_root}'!",
                ModuleNotFoundError,
            )
        else:
            return None, None

    file_ext = os.path.splitext(file_path)[1]

    filepath = pathlib.Path(file_path)
    # Force core file to be contained in a folder with the same name.
    # Skip this check if we are the top module (no top defined) or trying to setup the top module again (same name as previous defined top)
    if filepath.parent.resolve().name != core_name and (
        iob_core.global_top_module
        and core_name != iob_core.global_top_module.original_name
    ):
        fail_with_msg(
            f"Setup file of '{core_name}' must be contained in a folder with the same name!\n"
            f"It should be in a path like: '{filepath.parent.resolve()}/{core_name}/{filepath.name}'.\n"
            f"But found incorrect path:    '{filepath.resolve()}'."
        )

    # print("Found setup dir based on location of: " + file_path, file=sys.stderr)
    if file_ext == ".py" or file_ext == ".json":
        return os.path.dirname(file_path), file_ext

def clean_build_dir(build_dir):
    """
        Clean and delete given build directory

        Attributes:
            build_dir (str): Path to the build directory
    """
    if not os.path.exists(build_dir):
        return
    print(
        f"{iob_colors.INFO}Cleaning build directory: '{build_dir}'.{iob_colors.ENDC}"
    )
    os.system(f"make -C {build_dir} clean")
    shutil.rmtree(build_dir)
    print(
        f"{iob_colors.INFO}Cleaning complete. Removed: '{build_dir}'.{iob_colors.ENDC}"
    )


#
# API methods
#


def core_from_dict(core_dict):
    return iob_core(core_dict)


def core_text2dict(core_text):
    core_flags = [
        # iob_module attributes
        "original_name",
        "name",
        ['-d', {'dest': 'descr'}],
        ['--rst_pol', {'dest': 'rst_policy'}],
        ['--conf', {'dest': 'confs', 'action': 'append'}],
        ['--port', {'dest': 'ports', 'action': 'append'}],
        ['--bus', {'dest': 'buses', 'action': 'append'}],
        ['--snippet', {'dest': 'snippets', 'action': 'append'}],
        ['--comb', {'dest': 'comb'}],
        ['--fsm', {'dest': 'fsm'}],
        ['--subblock', {'dest': 'subblocks', 'action': 'append'}],
        ['--superblock', {'dest': 'superblocks', 'action': 'append'}],
        ['--sw_module', {'dest': 'sw_modules', 'action': 'append'}],
        # iob_instance attributes
        ['--inst_name', {'dest': 'instance_name'}],
        ['--inst_d', {'dest': 'instance_description'}],
        ['-c', {'dest': 'connect', 'action': 'append'}],  # port:ext format
        ['--param', {'dest': 'parameters', 'action': 'append'}],  # PARAM:VALUE format
        ['--no-instantiate', {'dest': 'instantiate', 'action': 'store_false'}],
        ['--dest_dir', {'dest': 'dest_dir'}],
        # iob_core attributes
        ['-v', {'dest': 'version'}],
        ['--prev_v', {'dest': 'previous_version'}],
        ['--setup_dir', {'dest': 'setup_dir'}],
        ['--build_dir', {'dest': 'build_dir'}],
        ['--use_netlist', {'dest': 'use_netlist', 'action': 'store_true'}],
        ['--system', {'dest': 'is_system', 'action': 'store_true'}],
        ['--board', {'dest': 'board_list', 'action': 'append'}],
        ['--ignore_snippet', {'dest': 'ignore_snippets', 'action': 'append'}],
        ['--gen_hw', {'dest': 'generate_hw', 'action': 'store_true'}],
        ['--parent', {'dest': 'parent'}],
        ['--tester', {'dest': 'is_tester', 'action': 'store_true'}],
        ['--py_param', {'dest': 'python_parameters', 'action': 'append'}],
        ['--lic', {'dest': 'license'}],
        ['--doc_conf', {'dest': 'doc_conf'}],
        ['--title', {'dest': 'title'}],
    ]
    core_dict = parse_short_notation_text(core_text, core_flags)
    # TODO: process core_dict:
    #   - confs, ports, buses, snippets, comb, fsm,
    #   - subblocks, superblocks, sw_modules
    #   - connect -> portmap_connections, parameters, ignore_snippets?
    #   - parent?, python_parameters
    return core_dict


def core_from_text(core_text):
    return core_from_dict(core_text2dict(core_text))


def get_global_wires_list():
    return iob_core.global_wires
