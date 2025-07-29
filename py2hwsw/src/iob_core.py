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
import block_gen
import snippet_gen
import verilog_gen
import wire_gen

from iob_base import (
    fail_with_msg,
    find_file,
    nix_permission_hack,
    update_obj_from_dict,
    find_common_deep,
)
from py2hwsw_version import PY2HWSW_VERSION
import sw_tools
import verilog_format
import verilog_lint

from iob_module import iob_module
from iob_conf import iob_conf
from iob_wire import iob_wire
from iob_port import iob_port
from iob_snippet import iob_snippet
from iob_license import iob_license
from iob_parameter import iob_parameter_group


class iob_core(iob_module):
    """
    Generic class to describe how to generate a base IOb IP core.

    This class may be instantiated using 3 different interfaces:
    - Object interface:          by calling the `__init__()` constructor.
    - Dictionary/JSON interface: by calling the `create_from_dict()` method.
    - Short Notation interface:  by calling the `create_from_text()` method.

    To see the arguments supported by the constructor that initializes this class, refer to the `__init__()` method of this class.
    To see the keys supported by the dictionary that initializes this class, refer to the `create_from_dict()` method of this class.
    To see the syntax supported by the short notation that initializes this class, refer to the `create_from_text()` method of this class.

    Attributes:
        # Module attributes
        original_name (str): Original name of the module. Usually auto-filled by Py2HWSW.
                             Must match name of the core's .py file and its class (if any);
                             Must match name of the core's .json file (if any).
                             Only manually needed if core is built directly from iob_core (like `my_core = iob_core(<core_attributes>)`).
        name (str): Name of the generated module. Usually the same as 'original_name' attribute.
                    The core's generated verilog module, sources, and files will have this name.
                    If the core has files in its setup directory, containing strings matching the 'original_name', they will all be renamed to this 'name' when copied to the build directory.
        description (str): Description of the module.
        reset_polarity (str): Global reset polarity of the module. Can be 'positive' or 'negative'. (Will override all subblocks' reset polarities).
        confs (list): List of module macros and Verilog (false-)parameters
        wires (list): List of module wires
        ports (list): List of module ports
        buses (list): List of module buses
        interfaces (list): List of module interfaces
        snippets (list): List of Verilog code snippets
        subblocks (list): List of instances of other cores inside this core.
        superblocks (list): List of wrappers for this core. Will only be setup if this core is a top module, or a wrapper of the top module.
        sw_modules (list): List of software modules required by this core.

        # Core attributes
        version (str): Core version. By default is the same as Py2HWSW version.
        previous_version (str): Core previous version.
        setup_dir (str): Path to root folder (setup directory) of the core. Usually auto-filled by Py2HWSW.
                         By default this directory matches the directory of the core's .py/.json file.
        build_dir (str): Path to folder of build directory to be generated for this project.
        use_netlist (bool): Copy `<SETUP_DIR>/CORE.v` netlist instead of `<SETUP_DIR>/hardware/src/*`
        is_system (bool): Sets `IS_FPGA=1` in config_build.mk
        board_list (list): List of FPGAs supported by this core. A standard folder will be created for each board in this list.
        ignore_snippets (list): List of `.vs` file includes in verilog to ignore.
        generate_hw (bool): Select if should try to generate `<corename>.v` from py2hwsw dictionary. Otherwise, only generate `.vs` files.
        is_tester (bool): Generates makefiles and depedencies to run this core as if it was the top module. Used for testers (superblocks of top moudle).
        supported_iob_parameters (list): List of core IOb Parameters. Used for documentation.
        license (iob_license): License for the core.
        doc_conf (str): CSR Configuration to use.
        title (str): Title of this core. Used for documentation.
        dest_dir (str): Relative path to the destination inside build directory to copy sources of this core (from this core's hardware/src/ folder).
                        Only applicable to subblocks/superblocks. Never the top module.
                        For example, if this core contains dest_dir="hardware/simulation/src", this core's sources (from the hardware/src/ folder) will be copied to <build_dir>/hardware/simulation/src, during the build directory generation process.
                        Note: Even though this is a core attribute (each instantiated core only has one copy of it), it is usually specified by the instantiator/issuer of this core.

    """

    # List of global wires. Similar concept to 'netlist' in HDL terminology: https://vhdlwhiz.com/terminology/net/#net
    global_wires: list = []
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
        Constructor for cores.

        Attributes:
            core_dictionary (dict): Optional dictionary to initialize core attributes.
                                    The format of this dictionary is the same as the dictionary received by the `create_from_dict` method.
        """

        # Inherit attributes from superclasses
        iob_module.__init__(self)

        # For debug:
        # print("Iob-core: called")
        # print("Iob-core attributes:", self.__class__.__annotations__)

        # Module attributes
        # FIXME: Remove original_name attribute. Create py2hwsw `get_original_name()` method that obtains class name dynamically.
        # The lack of this attribute may cause some issues for .json cores, or cores created with iob_core(core_dict).
        # But we can probably work around this by creating dynamic subclasses of iob_core with the correct name.
        self.original_name: str = None
        self.name: str = ""
        self.description: str = "Default description"
        self.reset_polarity: str = "positive"
        self.confs: list[iob_conf] = []
        self.wires: list[iob_wire] = []
        self.ports: list[iob_port] = []
        self.buses: list[iob_bus] = []
        self.snippets: list[iob_snippet] = []
        self.subblocks: list[iob_instance] = []
        self.superblocks: list[iob_core] = []
        self.sw_modules: list[iob_core] = []

        # Core attributes
        self.version: str = PY2HWSW_VERSION
        self.previous_version: str = PY2HWSW_VERSION
        self.setup_dir: str = None
        self.build_dir: str = "build"
        self.use_netlist: bool = False
        self.is_system: bool = False
        self.board_list: list[str] = []
        self.ignore_snippets: list[str] = []
        self.generate_hw: bool = False
        self.is_tester: bool = False
        self.iob_parameters: list[iob_parameter_group] = []
        self.license: iob_license = iob_license()
        self.doc_conf: str = ""
        self.title: str = ""
        self.dest_dir: str = "hardware/src"

        # Set internal attributes
        "Selects if core is top module."
        self.is_top_module = __class__.global_top_module == self
        "Selects if core is superblock of another."
        self.is_superblock = False # FIXME: Auto fill
        "Store reference to the issuer block."
        self.issuer = None # FIXME: Auto fill
        "Selects if core is parent of another."
        self.is_parent = False # FIXME: Do we still need this?

        # Attributes with automatic default values
        # self.previous_version = self.version # FIXME: Should this be updated later? (For example, if version is changed afterwards?)

        # Update current core's attributes with values from given core_dictionary
        if core_dictionary:
            # Lazy import instance to avoid circular dependecy
            iob_instance = getattr(importlib.import_module('iob_instance'), 'iob_instance')
            # Sanity check. These keys are only used to instantiate other user-defined/lib cores. Not iob_core directly.
            if "core" in core_dictionary or "iob_parameters" in core_dictionary:
                fail_with_msg("The 'core' and 'iob_parameters' keys cannot be used in core dictionaries passed directly to the core constructor!")
            # Convert core dictionary elements to objects
            core_dict_with_objects = core_dictionary.copy()
            for c in core_dictionary.get("confs", []):
                if "type" in c:
                    breakpoint()
            core_dict_with_objects["confs"] = [iob_conf.create_from_dict(i) for i in core_dictionary.get("confs", [])]
            core_dict_with_objects["ports"] = [iob_port.create_from_dict(i) for i in core_dictionary.get("ports", [])]
            core_dict_with_objects["wires"] = [iob_wire.create_from_dict(i) for i in core_dictionary.get("wires", [])]
            core_dict_with_objects["buses"] = [iob_bus.create_from_dict(i) for i in core_dictionary.get("buses", [])]
            core_dict_with_objects["snippets"] = [iob_snippet.create_from_dict(i) for i in core_dictionary.get("snippets", [])]
            core_dict_with_objects["subblocks"] = [iob_instance.create_from_dict(i) for i in core_dictionary.get("subblocks", [])]
            core_dict_with_objects["superblocks"] = [__class__.create_from_dict(i) for i in core_dictionary.get("superblocks", [])]
            core_dict_with_objects["sw_modules"] = [__class__.create_from_dict(i) for i in core_dictionary.get("sw_modules", [])]
            core_dict_with_objects["iob_parameters"] = [iob_parameter_group.create_from_dict(i) for i in core_dictionary.get("iob_parameters", [])]
            update_obj_from_dict(self, core_dict_with_objects)  # valid_attributes_list=...)

        # Set global build directory
        if self.is_top_module:
            # FIXME: Ideally make this copy by reference, so that updates to the top's build dir are reflected across all cores
            __class__.global_build_dir = self.build_dir

        # Get name of (user's) subclass that is inheriting from iob_core
        # FIXME: subclass_name=type(self.get_api_obj()).__name__
        # TEMPFIX:
        subclass_name = self.__class__.__name__

        # Auto-fill original_name based on user subclass's name (if any). May not have subclass if defined via JSON or direct constructor call.
        if not self.original_name and subclass_name != "iob_core":
            self.original_name = subclass_name

        # Try to find core's setup directory based on original name (try to find .py and .json files for it)
        core_dir, _ = __class__.find_module_setup_dir(self.original_name, error_on_not_found=False)
        # Auto-fill setup_dir based on found core directory.
        if not self.setup_dir and core_dir:
            self.setup_dir = core_dir

        # Use original name as default name
        self.name = self.name or self.original_name

        return

    def generate_build_dir(self, **kwargs):
        """
        Standard method to generate build directory.
        May be overridden by user subclasses to generate custom files or run scripts during the build directory generation process.
        """
        self.validate_attributes()

        # Delete existing old build directory
        if self.is_top_module:
            __class__.clean_build_dir(self.build_dir)

        self.__create_build_dir()

        # Generate build dir of subblocks
        for subblock in self.subblocks:
            if self.is_superblock:
                if subblock.original_name == self.issuer.original_name:
                    # skip build dir generation for issuer subblocks
                    continue
            subblock.core.generate_build_dir()

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

        # Generate parameters and local parameters
        param_gen.generate_params_snippets(self)
        param_gen.generate_localparams_snippets(self)

        # Generate ios
        io_gen.generate_ports_snippet(self)

        # Generate wires
        wire_gen.generate_wires_snippet(self)

        # Generate instances
        if self.generate_hw:
            block_gen.generate_subblocks_snippet(self)

        # Generate snippets
        snippet_gen.generate_snippets_snippet(self)

        # Generate main Verilog module
        if self.generate_hw:
            verilog_gen.generate_verilog(self)

        if (self.is_top_module and not self.is_parent) or self.is_tester:
            self.post_setup()

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

        # Lint and format sources
        self.lint_and_format()
        print(
            f"{iob_colors.INFO}Setup of '{self.original_name}' core successful. Generated build directory: '{self.build_dir}'.{iob_colors.ENDC}"
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

    @staticmethod
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

    @staticmethod
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
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(core_dict):
        """
        Function to create iob_core object from dictionary attributes.

        Attributes:
            core_dict (dict): dictionary with values to initialize attributes of iob_core object.
                This dictionary supports the following keys corresponding to the iob_core attributes:

                # Module keys
                - original_name -> iob_module.original_name
                - name -> iob_module.name
                - description -> iob_module.description
                - reset_polarity -> iob_module.reset_polarity
                - confs -> iob_module.confs = [iob_conf.create_from_dict(i) for i in confs]
                - wires -> iob_module.wires = [iob_wire.create_from_dict(i) for i in wires]
                - ports -> iob_module.ports = [iob_port.create_from_dict(i) for i in ports]
                - buses -> iob_module.buses = [iob_bus.create_from_dict(i) for i in buses]
                - snippets -> iob_module.snippets = [iob_snippet.create_from_dict(i) for i in snippets]
                - subblocks -> iob_module.subblocks = [iob_instance.create_from_dict(i) for i in subblocks]
                - superblocks -> iob_module.superblocks = [iob_core.create_from_dict(i) for i in superblocks]
                - sw_modules -> iob_module.sw_modules = [iob_core.create_from_dict(i) for i in sw_modules]

                # Core keys
                - version -> iob_core.version
                - previous_version -> iob_core.previous_version
                - setup_dir -> iob_core.setup_dir
                - build_dir -> iob_core.build_dir
                - use_netlist -> iob_core.use_netlist
                - is_system -> iob_core.is_system
                - board_list -> iob_core.board_list
                - ignore_snippets -> iob_core.ignore_snippets
                - generate_hw -> iob_core.generate_hw
                - is_tester -> iob_core.is_tester
                - iob_parameters -> iob_core.iob_parameters  # FIXME: Cant have two keys with the same name
                - license -> iob_core.license
                - doc_conf -> iob_core.doc_conf
                - title -> iob_core.title
                - dest_dir -> iob_core.dest_dir

                Some keys (like confs) may contain (sub-)dictionaries as values.
                Refer to the corresponding `<class_name>.create_from_dict()` methods for info about the format and supported keys of these dictionaries.
                For example, type `help(iob_conf.create_from_dict)` to view the keys supported by the dictionary that initializes the iob_conf object.

        Returns:
            iob_core: iob_core object
        """
        return iob_core(core_dict)
