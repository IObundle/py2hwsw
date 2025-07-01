# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import shutil
import json
from pathlib import Path
import copy
from types import SimpleNamespace
import pathlib

import iob_colors

import copy_srcs

import config_gen
import param_gen
import io_gen
import wire_gen
import block_gen
import comb_gen
import fsm_gen
import snippet_gen
import doc_gen
import verilog_gen
import ipxact_gen

from py2hwsw_version import PY2HWSW_VERSION
from iob_python_parameter import create_python_parameter_group
from if_gen import mem_if_names
from iob_module import iob_module, get_list_attr_handler
from iob_instance import iob_instance
from iob_base import (
    fail_with_msg,
    find_file,
    import_python_module,
    nix_permission_hack,
    add_traceback_msg,
    debug,
    get_lib_cores,
)
from iob_license import iob_license, update_license
import sw_tools
import verilog_format
import verilog_lint
from manage_headers import generate_headers


class iob_core(iob_module, iob_instance):
    """Generic class to describe how to generate a base IOb IP core"""

    # List of global wires.
    # See 'TODO' in iob_core.py for more info: https://github.com/IObundle/py2hwsw/blob/a1e2e2ee12ca6e6ad81cc2f8f0f1c1d585aaee73/py2hwsw/scripts/iob_core.py#L251-L259
    global_wires: list
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

    def __init__(self, *args, **kwargs):
        """Build a core (includes module and instance attributes)
        :param str dest_dir: Destination directory, within the build directory, for the core
        :param dict attributes: py2hwsw dictionary describing the core
            Notes:
                1) Each key/value pair in the dictionary describes an attribute name and
                   corresponding attribute value of the core.
                2) If the dictionary contains a key that does not match any attribute
                   of the core, then an error will be raised.
                3) The values will be processed by the `set_handler` method of the
                   corresponding attribute. This method will convert from the py2hwsw
                   dictionary datatypes into the internal IObundle datatypes.
                   For example, it converts a 'wire' dict into an `iob_wire` object.
                4) If another constructor argument is also given (like the argument
                   'dest_dir'), and this dictionary also contains a key for the same
                   attribute (like the key 'dest_dir'), then the value given in the
                   dictionary will override the one from the constructor argument.
        :param dict connect: External wires to connect to ports of this instance
                       Key: Port name, Value: Wire name
        :param iob_core issuer: Module that is instantiating this instance
        :param bool is_parent: If this core is a parent core
        """
        # Arguments used by this class
        dest_dir = kwargs.get("dest_dir", "hardware/src")
        attributes = kwargs.get("attributes", {})
        connect = kwargs.get("connect", {})
        self.issuer = kwargs.get("issuer", None)
        self.is_parent = kwargs.get("is_parent", False)

        # Store kwargs to allow access to python parameters after object has been created
        self.received_python_parameters = kwargs

        # Create core based on 'parent' core (if applicable)
        if self.handle_parent(*args, **kwargs):
            return

        # Inherit attributes from superclasses
        iob_module.__init__(self, *args, **kwargs)
        iob_instance.__init__(self, *args, **kwargs)
        # Ensure global top module is set
        self.update_global_top_module(attributes)
        self.set_default_attribute(
            "version",
            PY2HWSW_VERSION,
            str,
            descr="Core version. By default is the same as Py2HWSW version.",
        )
        self.set_default_attribute(
            "previous_version",
            self.version,
            str,
            descr="Core previous version.",
        )
        self.set_default_attribute(
            "setup_dir",
            kwargs.get("setup_dir", ""),
            str,
            descr="Path to root setup folder of the core.",
        )
        self.set_default_attribute(
            "build_dir",
            "",
            str,
            descr="Path to folder of build directory to be generated for this project.",
        )
        self.set_default_attribute(
            "instance_name",
            "",
            str,
            descr="Name of an instance of this class.",
        )
        self.set_default_attribute(
            "use_netlist",
            False,
            bool,
            descr="Copy `<SETUP_DIR>/CORE.v` netlist instead of `<SETUP_DIR>/hardware/src/*`",
        )
        self.set_default_attribute(
            "is_system",
            False,
            bool,
            descr="Sets `IS_FPGA=1` in config_build.mk",
        )
        self.set_default_attribute(
            "board_list",
            [],
            list,
            descr="List of FPGAs supported by this core. A standard folder will be created for each board in this list.",
        )
        self.set_default_attribute(
            "dest_dir",
            dest_dir,
            str,
            descr="Relative path inside build directory to copy sources of this core. Will only sources from `hardware/src/*`",
        )
        self.set_default_attribute(
            "ignore_snippets",
            [],
            list,
            descr="List of `.vs` file includes in verilog to ignore.",
        )
        self.set_default_attribute(
            "generate_hw",
            False,
            bool,
            descr="Select if should try to generate `<corename>.v` from py2hwsw dictionary. Otherwise, only generate `.vs` files.",
        )
        self.set_default_attribute(
            "parent",
            {},
            dict,
            descr="Select parent of this core (if any). If parent is set, that core will be used as a base for the current one. Any attributes of the current core will override/add to those of the parent.",
        )
        self.set_default_attribute(
            "is_top_module",
            __class__.global_top_module == self,
            bool,
            descr="Selects if core is top module. Auto-filled. DO NOT CHANGE.",
        )
        self.set_default_attribute(
            "is_superblock",
            kwargs.get("is_superblock", False),
            bool,
            descr="Selects if core is superblock of another. Auto-filled. DO NOT CHANGE.",
        )
        self.set_default_attribute(
            "is_tester",
            False,
            bool,
            descr="Generates makefiles and depedencies to run this core as if it was the top module. Used for testers (superblocks of top moudle).",
        )
        # List of core Python Parameters (for documentation)
        self.set_default_attribute(
            "python_parameters",
            [],
            list,
            get_list_attr_handler(self.create_python_parameter_group),
            descr="List of core Python Parameters. Used for documentation.",
        )
        self.set_default_attribute(
            "license",
            iob_license(),  # Create a default license
            iob_license,
            lambda y: update_license(self, **y),
            descr="License for the core.",
        )
        self.set_default_attribute(
            "doc_conf",
            "",
            str,
            descr="CSR Configuration to use",
        )
        self.set_default_attribute(
            "title",
            attributes.get("original_name", self.__class__.__name__),
            str,
            descr="Tile of this core. Used for documentation.",
        )

        if self.is_top_module and "reset_polarity" not in attributes:
            # Set default reset polarity to 'positive'
            if "reset_polarity" not in attributes:
                attributes["reset_polarity"] = "positive"

        self.attributes_dict = copy.deepcopy(attributes)

        self.abort_reason = None
        # Don't setup this core if using a project wide special target.
        if __class__.global_special_target:
            if __class__.global_special_target == "ipxact_gen":
                # Will cause setup to abort except for iob_csrs (to generate memory map)
                self.abort_reason = "ipxact_gen"
            else:
                self.abort_reason = "special_target"

        # Temporarily change global_build_dir to match tester's directory (for tester blocks)
        build_dir_backup = __class__.global_build_dir
        if attributes.get("is_tester", False):
            # If is tester, build dir is same "dest_dir". (default: tester)
            self.relative_path_to_tester = kwargs.get("dest_dir", "tester")
            __class__.global_build_dir = os.path.join(
                __class__.global_build_dir, self.relative_path_to_tester
            )
            self.dest_dir = "hardware/src"

        # Read 'attributes' dictionary and set corresponding core attributes
        superblocks = attributes.pop("superblocks", [])
        # Note: Parsing attributes (specifically the subblocks list) also initializes subblocks
        self.parse_attributes_dict(attributes)

        # Connect ports of this instance to external wires (wires of the issuer)
        self.connect_instance_ports(connect, self.issuer)

        # iob_csrs specific code
        if self.is_system:
            self.__fix_subblock_cbus_widths()

        # Create memory wrapper for top module if any memory interfaces are used
        if self.is_top_module or self.is_tester:
            if any(
                (port.interface.type in mem_if_names and port.name.endswith("m"))
                for port in self.ports
                if port.interface
            ):
                superblocks = self.__create_memwrapper(superblocks=superblocks)

        # Add 'VERSION' macro
        self.create_conf_group(
            name="VERSION",
            type="C",
            val="16'h" + self.version_str_to_digits(self.version),
            descr="Product version. This 16-bit macro uses nibbles to represent decimal numbers using their binary values. The two most significant nibbles represent the integral part of the version, and the two least significant nibbles represent the decimal part.",
        )

        # Ensure superblocks are instanciated last
        # and only for top module (or wrappers of it)
        if self.is_top_module or self.is_superblock:
            self.parse_attributes_dict({"superblocks": superblocks})
        if self.is_superblock:
            # Generate verilog parameters of issuer subblock
            param_gen.generate_inst_params(self.issuer)

        if not self.is_top_module:
            self.build_dir = __class__.global_build_dir
        # print(
        #     f"DEBUG: {self.name} {self.original_name} {self.build_dir} {self.is_top_module}",
        #     file=sys.stderr,
        # )

        # Restore global_build_dir (previously changed for tester blocks)
        if self.is_tester:
            __class__.global_build_dir = build_dir_backup

        if self.abort_reason:
            return

    def post_setup(self):
        """Scripts to run at the end of the top module's setup"""
        # Replace Verilog snippet includes
        self._replace_snippet_includes()
        # Clean duplicate sources in `hardware/src` and its subfolders (like `hardware/simulation/src`)
        self._remove_duplicate_sources()
        if self.is_tester:
            # Add callback to: Remove duplicate sources from tester dirs, that already exist in UUT's `hardware/src` folder
            __class__.global_post_setup_callbacks.append(
                lambda: self._remove_duplicate_sources(
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
        ipxact_gen.generate_ipxact_xml(self, self.build_dir + "/ipxact")
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
        custom_header=f"Py2HWSW Version {PY2HWSW_VERSION} has generated this code (https://github.com/IObundle/py2hwsw)."
        generate_headers(
            root=self.build_dir,
            copyright_holder=self.license.author,
            copyright_year=self.license.year,
            license_name=self.license.name,
            header_template="spdx",
            custom_header_suffix=custom_header,
            skip_existing_headers=True,
            verbose=False,
        )

    def create_python_parameter_group(self, *args, **kwargs):
        create_python_parameter_group(self, *args, **kwargs)

    def handle_parent(self, *args, **kwargs):
        """Create a new core based on parent core.
        returns: True if parent core was used. False otherwise.
        """
        attributes = kwargs.pop("attributes", {})
        child_attributes = kwargs.pop("child_attributes", {})
        if self.is_parent:
            self.append_child_attributes(attributes, child_attributes)

        # Don't setup parent core if this one does not have parent
        parent = attributes.get("parent")
        if not parent:
            return False

        assert parent["core_name"] != attributes["original_name"], fail_with_msg(
            f"Parent and child cannot have the same name: '{parent['core_name']}'"
        )

        belongs_to_top_module = not __class__.global_top_module
        # Check if this child module is the first one called (It is the leaf child of the top module. Does not have any other childs.)
        is_first_module_called = belongs_to_top_module and not self.is_parent

        name = attributes.get("name", attributes["original_name"])
        # Update global build dir to match this module's name and version
        if is_first_module_called and not __class__.global_build_dir:
            version = attributes.get("version", PY2HWSW_VERSION)
            __class__.global_build_dir = f"../{name}_V{version}"

        filtered_parent_py_params = dict(parent)
        filtered_parent_py_params.pop("core_name", None)
        filtered_parent_py_params.pop("py2hwsw_target", None)
        filtered_parent_py_params.pop("build_dir", None)
        filtered_parent_py_params.pop("issuer", None)
        filtered_parent_py_params.pop("py2hwsw_version", None)
        filtered_parent_py_params.pop("connect", None)
        filtered_parent_py_params.pop("parameters", None)
        filtered_parent_py_params.pop("is_superblock", None)
        if "name" not in filtered_parent_py_params:
            filtered_parent_py_params["name"] = name

        # print("DEBUG1", kwargs, file=sys.stderr)
        # print("DEBUG2", filtered_parent_py_params, file=sys.stderr)

        # Setup parent core
        parent_module = self.get_core_obj(
            parent["core_name"],
            **filtered_parent_py_params,
            is_parent=True,
            child_attributes=attributes,
            issuer=kwargs.get("issuer", None),
            connect=kwargs.get("connect", {}),
            parameters=kwargs.get("parameters", {}),
            is_superblock=kwargs.get("is_superblock", False),
        )

        # Copy (some) parent attributes to child
        self.__dict__.update(parent_module.__dict__)
        self.original_name = attributes["original_name"]
        self.setup_dir = attributes["setup_dir"]

        if self.abort_reason:
            return True

        # Copy files from the module's setup dir
        copy_srcs.copy_rename_setup_directory(self)

        # Run post setup
        if is_first_module_called:
            self.post_setup()

        return True

    def generate_build_dir(self, **kwargs):

        self.__create_build_dir()

        # subblock setup process
        for subblock in self.subblocks:
            if self.is_superblock:
                if subblock.original_name == self.issuer.original_name:
                    # skip build dir generation for issuer subblocks
                    continue
            subblock.generate_build_dir()

        # Ensure superblocks are set up only for top module (or wrappers of it)
        if self.is_top_module or self.is_superblock:
            for superblock in self.superblocks:
                superblock.generate_build_dir()

        if self.is_tester:
            self.relative_path_to_UUT = os.path.relpath(
                __class__.global_build_dir, self.build_dir
            )

        # Copy files from LIB to setup various flows
        # (should run before copy of files from module's setup dir)
        if self.is_top_module or self.is_tester:
            copy_srcs.flows_setup(self)

        # Copy files from the module's setup dir
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

        # Generate wires
        wire_gen.generate_wires_snippet(self)

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

        # TODO: Generate a global list of signals
        # This list is useful for a python based simulator
        # 1) Each input of the top generates a global signal
        # 2) Each output of a leaf generates a global signal
        # 3) Each output of a snippet generates a global signal
        #    A snippet is a piece of verilog code manually written (should also receive a list of outputs by the user).
        #    A snippet can also be any method that generates a new signal, like the `concat_bits`, or any other that performs logic in from other signals into a new one.
        # TODO as well: Each module has a local `snippets` list.
        # Note: The 'width' attribute of many module's signals are generaly not needed, because most of them will be connected to global wires (that already contain the width).

        if (self.is_top_module and not self.is_parent) or self.is_tester:
            self.post_setup()

    @staticmethod
    def append_child_attributes(parent_attributes, child_attributes):
        """Appends/Overrides parent attributes with child attributes"""
        for child_attribute_name, child_value in child_attributes.items():
            # Don't override child-specific attributes
            if child_attribute_name in ["original_name", "setup_dir", "parent"]:
                continue

            # Override other attributes of type string and bool
            if type(child_value) is str or type(child_value) is bool:
                parent_attributes[child_attribute_name] = child_value
                continue

            # Override or append elements from list attributes
            assert (
                type(child_value) is list
            ), f"Invalid type for attribute '{child_attribute_name}': {type(child_value)}"

            # Select identifier attribute. Used to compare if should override each element.
            identifier = "name"
            if child_attribute_name in ["subblocks", "superblocks", "sw_modules"]:
                identifier = "instance_name"
            elif child_attribute_name in ["board_list", "snippets", "ignore_snippets"]:
                # Elements in list do not have identifier, so just append them to parent list
                for child_obj in child_value:
                    parent_attributes[child_attribute_name].append(child_obj)
                continue

            # Process each object from list
            for child_obj in child_value:
                # Find object and override it
                for idx, obj in enumerate(parent_attributes[child_attribute_name]):
                    if obj[identifier] == child_obj[identifier]:
                        debug(f"Overriding {child_obj[identifier]}", 1)
                        parent_attributes[child_attribute_name][idx] = child_obj
                        break
                else:
                    # Didn't override, so append it to list
                    parent_attributes[child_attribute_name].append(child_obj)

    def update_global_top_module(self, attributes={}):
        """Update the global top module and the global build directory.
        param attributes: Py2hwsw dictionary describing the core
                          Will be used to get the core name and version if available.
        """
        super().update_global_top_module()
        # Ensure top module has a build dir (and associated attributes)
        if __class__.global_top_module == self:
            original_name = attributes.get("original_name", self.__class__.__name__)
            name = attributes.get("name", self.original_name)
            version = attributes.get("version", PY2HWSW_VERSION)
            # Set attributes
            if not hasattr(self, "original_name") or not self.original_name:
                self.original_name = original_name
            if not hasattr(self, "name") or not self.name:
                self.name = name
            if not hasattr(self, "version") or not self.version:
                self.version = version
            if not __class__.global_build_dir:
                __class__.global_build_dir = f"../{self.name}_V{self.version}"
            self.set_default_attribute("build_dir", __class__.global_build_dir)

    def __fix_subblock_cbus_widths(self):
        """Used specifically for iob_system type cores
        Goes through subblocks list, and fixes address widths of cbus interfaces to match the peripheral's cbus port
        Assumes peripheral has a cbus port of type "iob".
        """
        assert (
            self.is_system
        ), "Internal error: only iob_system type cores need fixing cbus width"
        for subblock in self.subblocks:
            for port in subblock.ports:
                if (
                    port.name == "iob_csrs_cbus_s"
                    and port.interface.type == "iob"
                    and port.e_connect
                ):
                    # print(
                    #     "DEBUG",
                    #     self.name,
                    #     port,
                    #     file=sys.stderr,
                    # )
                    port_width = port.interface.widths["ADDR_W"]
                    external_wire_prefix = port.e_connect.interface.prefix
                    port.e_connect_bit_slices = [
                        f"{external_wire_prefix}iob_addr[{port_width}-1:0]"
                    ]

    def __create_memwrapper(self, superblocks):
        """Create memory wrapper for top module"""
        new_superblocks = [
            {
                "core_name": "iob_memwrapper",
                "instance_name": f"{self.name}_memwrapper",
                "mem_if_names": mem_if_names,
                "superblocks": superblocks,
            },
        ]
        return new_superblocks

    def __create_build_dir(self):
        """Create build directory if it doesn't exist"""
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(os.path.join(self.build_dir, self.dest_dir), exist_ok=True)

        os.makedirs(f"{self.build_dir}/document", exist_ok=True)
        os.makedirs(f"{self.build_dir}/document/tsrc", exist_ok=True)

        shutil.copyfile(
            f"{copy_srcs.get_lib_dir()}/build.mk", f"{self.build_dir}/Makefile"
        )
        nix_permission_hack(f"{self.build_dir}/Makefile")

    def _remove_duplicate_sources(self, main_folder="hardware/src", subfolders=None):
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

    def _replace_snippet_includes(self):
        verilog_gen.replace_includes(
            self.setup_dir, self.build_dir, self.ignore_snippets
        )

    def parse_attributes_dict(self, attributes):
        """Parse attributes dictionary given, and build and set the corresponding
        attributes for this core, using the handlers stored in `ATTRIBUTE_PROPERTIES`
        dictionary.
        If there is no handler for an attribute then it will raise an error.
        """
        # For each attribute of the dictionary, check if there is a handler,
        # and use it to set the attribute
        for attr_name, attr_value in attributes.items():
            if attr_name in self.ATTRIBUTE_PROPERTIES:
                self.ATTRIBUTE_PROPERTIES[attr_name].set_handler(attr_value),
            else:
                fail_with_msg(
                    f"Unknown attribute '{attr_name}' in core {attributes['original_name']}"
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

    @classmethod
    def py2hw(cls, core_dict, **kwargs):
        """Generate a core based on the py2hw dictionary interface
        param core_dict: The core dictionary using py2hw dictionary syntax
        param kwargs: Optional additional arguments to pass directly to the core
        """
        try:
            return cls(attributes=core_dict, **kwargs)
        except Exception:
            add_traceback_msg(f"Failed to setup core '{core_dict['name']}'.")
            if "issuer" in kwargs and kwargs["issuer"]:
                raise
            exit(1)

    @classmethod
    def read_py2hw_json(cls, filepath, **kwargs):
        """Read JSON file with py2hw attributes build a core from it
        param filepath: Path to JSON file using py2hw json syntax
        param kwargs: Optional additional arguments to pass directly to the core
        """
        with open(filepath) as f:
            core_dict = json.load(f)

        default_core_name = os.path.splitext(os.path.basename(filepath))[0]
        py2_core_dict = {
            "original_name": default_core_name,
            "name": default_core_name,
            "setup_dir": os.path.dirname(filepath),
        }
        py2_core_dict.update(core_dict)

        return cls.py2hw(py2_core_dict, **kwargs)

    @staticmethod
    def clean_build_dir(core_name):
        """Clean build directory."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "clean"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name)
        # Don't try to clean if build dir doesn't exist
        if not os.path.exists(module.build_dir):
            return
        print(
            f"{iob_colors.INFO}Cleaning build directory: '{module.build_dir}'.{iob_colors.ENDC}"
        )
        os.system(f"make -C {module.build_dir} clean")
        shutil.rmtree(module.build_dir)
        print(
            f"{iob_colors.INFO}Cleaning complete. Removed: '{module.build_dir}'.{iob_colors.ENDC}"
        )

    @staticmethod
    def deliver_core(core_name):
        """Deliver core."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "deliver"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name)
        # Don't try to deliver if build dir doesn't exist
        if not os.path.exists(module.build_dir):
            # print error and exit
            print(
                f"{iob_colors.FAIL}Build directory not found: {module.build_dir}{iob_colors.ENDC}"
            )
            exit(1)
        print(f"{iob_colors.INFO}Delivering core: {core_name} {iob_colors.ENDC}")
        os.system(f"CORE={core_name} BUILD_DIR={module.build_dir} delivery.sh")

    @staticmethod
    def print_build_dir(core_name, **kwargs):
        """Print build directory."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_build_dir"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name, **kwargs)
        print(module.build_dir)

    def print_core_name(core_name, **kwargs):
        """Print build directory."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_core_name"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name, **kwargs)
        print(module.name)

    def print_core_version(core_name, **kwargs):
        """Print build directory."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_core_version"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name, **kwargs)
        print(module.version)

    @staticmethod
    def print_core_dict(core_name, **kwargs):
        """Print core attributes dictionary."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_core_dict"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name, **kwargs)
        print(json.dumps(module.attributes_dict, indent=4))

    @staticmethod
    def print_py2hwsw_attributes():
        """Print the supported attributes of the py2hwsw interface.
        The attributes listed can be used in the 'attributes' dictionary of cores.
        """
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_attributes"
        # Build a new dummy module instance, to obtain its attributes
        module = __class__()
        print("Attributes supported by the 'py2hwsw' core dictionary interface:")
        for name in module.ATTRIBUTE_PROPERTIES.keys():
            datatype = module.ATTRIBUTE_PROPERTIES[name].datatype
            descr = module.ATTRIBUTE_PROPERTIES[name].descr
            align_spaces = " " * (20 - len(name))
            align_spaces2 = " " * (18 - len(str(datatype)))
            print(f"- {name}:{align_spaces}{datatype}{align_spaces2}{descr}")

    @staticmethod
    def get_core_obj(core_name, **kwargs):
        """Generate an instance of a core based on given core_name and python parameters
        This method will search for the .py and .json files of the core, and generate a
        python object based on info stored in those files, and info passed via python
        parameters.
        Calling this method may also begin the setup process of the core, depending on
        the value of the `global_special_target` attribute.
        """
        core_dir, file_ext = find_module_setup_dir(core_name)

        if file_ext == ".py":
            import_python_module(
                os.path.join(core_dir, f"{core_name}.py"),
            )
            core_module = sys.modules[core_name]
            issuer = kwargs.pop("issuer", None)
            # Call `setup(<py_params_dict>)` function of `<core_name>.py` to
            # obtain the core's py2hwsw dictionary.
            # Give it a dictionary with all arguments of this function, since the user
            # may want to use any of them to manipulate the core attributes.
            core_dict = core_module.setup(
                {
                    # "core_name": core_name,
                    "build_dir": __class__.global_build_dir,
                    "py2hwsw_target": __class__.global_special_target or "setup",
                    "issuer": (
                        issuer.attributes_dict if issuer else ""
                    ),
                    "py2hwsw_version": PY2HWSW_VERSION,
                    **kwargs,
                }
            )
            py2_core_dict = {
                "original_name": core_name,
                "name": core_name,
                "setup_dir": core_dir,
            }
            py2_core_dict.update(core_dict)
            instance = __class__.py2hw(
                py2_core_dict,
                issuer=issuer,
                # Note, any of the arguments below can have their values overridden by
                # the py2_core_dict
                **kwargs,
            )
        elif file_ext == ".json":
            instance = __class__.read_py2hw_json(
                os.path.join(core_dir, f"{core_name}.json"),
                # Note, any of the arguments below can have their values overridden by
                # the json data
                **kwargs,
            )
        return instance

    @staticmethod
    def setup_py2_docs(py2_version):
        """Setup document directory for py2hwsw."""
        # Create temporary object to represent a "py2hwsw" core
        core = SimpleNamespace(
            original_name="py2hwsw",
            name="py2hwsw",
            setup_dir=os.path.join(os.path.dirname(__file__), "../py2hwsw_document"),
            build_dir="py2hwsw_generated_docs",
        )
        copy_srcs.doc_setup(core)
        copy_srcs.copy_rename_setup_subdir(core, "document")
        with open(f"{core.build_dir}/config_build.mk", "w") as f:
            f.write("NAME=Py2HWSW\n")
        with open(f"{core.build_dir}/document/tsrc/{core.name}_version.tex", "w") as f:
            f.write(py2_version)
        # Build a new dummy module instance, to obtain its attributes
        __class__.global_special_target = "print_attributes"
        dummy_module = __class__()
        doc_gen.generate_tex_py2hwsw_attributes(
            dummy_module, f"{core.build_dir}/document/tsrc"
        )
        doc_gen.generate_tex_core_lib(f"{core.build_dir}/document/tsrc")
        doc_gen.generate_tex_py2hwsw_standard_py_params(
            f"{core.build_dir}/document/tsrc"
        )
        doc_gen.process_tex_macros(f"{core.build_dir}/document/tsrc")

    @staticmethod
    def print_lib_cores():
        lib_path = os.path.join(os.path.dirname(__file__), "../lib")
        cores = get_lib_cores()
        print("Cores available in the Py2HWSW library:")
        for path in cores:
            file = os.path.basename(path)
            dir = os.path.dirname(path)
            print(f"- {os.path.splitext(file)[0]}: {os.path.relpath(dir, lib_path)}")

    @staticmethod
    def browse_lib():
        """Generate IP-XACT library with all lib cores"""
        # Set as special target to avoid setting up the cores
        __class__.global_special_target = "ipxact_gen"

        cores = get_lib_cores()
        for path in cores:
            file = os.path.basename(path)
            print(f"Generating IP-XACT for '{file}'.")
            # Create the core object as a top module to obtain its attributes.
            # Also, always set python parameter `demo=True`, since some lib cores use this parameter to generate a demo core.
            __class__.global_top_module = None
            module = __class__.get_core_obj(os.path.splitext(file)[0], demo=True)
            # Generate IP-XACT for the core
            ipxact_gen.generate_ipxact_xml(module, "ipxact_lib")

        print(
            f"{iob_colors.INFO}Generated IP-XACT library in './ipxact_lib/' folder.{iob_colors.ENDC}"
        )

    @staticmethod
    def version_str_to_digits(version_str):
        """Given a version string (like "V0.12"), return a 4 digit string representing
        the version (like "0012")"""
        version_str = version_str.replace("V", "")
        major_ver, minor_ver = version_str.split(".")
        return f"{int(major_ver):02d}{int(minor_ver):02d}"


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


def find_module_setup_dir(core_name):
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
        fail_with_msg(
            f"Python/JSON setup file of '{core_name}' core not found under path '{iob_core.global_project_root}'!",
            ModuleNotFoundError,
        )

    file_ext = os.path.splitext(file_path)[1]

    filepath = pathlib.Path(file_path)
    # Force core file to be contained in a folder with the same name.
    # Skip this check if we are the top module (no top defined) or trying to setup the top module again (same name as previous defined top)
    if filepath.parent.name != core_name and (
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
