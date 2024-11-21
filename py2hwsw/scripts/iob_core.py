# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import sys
import os
import shutil
import json
from pathlib import Path
import copy
from types import SimpleNamespace

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

from iob_module import iob_module
from iob_instance import iob_instance
from iob_base import (
    find_obj_in_list,
    fail_with_msg,
    find_file,
    import_python_module,
    nix_permission_hack,
    add_traceback_msg,
    debug,
    str_to_kwargs,
)
import sw_tools
import verilog_format
import verilog_lint


class iob_core(iob_module, iob_instance):
    """Generic class to describe how to generate a base IOb IP core"""

    global_wires: list
    # Project settings
    global_build_dir: str = ""
    global_project_root: str = "."
    global_project_vformat: bool = True
    global_project_vlint: bool = True
    # Project wide special target. Used when we don't want to run normal setup (for example, when cleaning).
    global_special_target: str = ""

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
        :param iob_core instantiator: Module that is instantiating this instance
        :param bool is_parent: If this core is a parent core
        """
        # Arguments used by this class
        dest_dir = kwargs.get("dest_dir", "hardware/src")
        attributes = kwargs.get("attributes", {})
        connect = kwargs.get("connect", {})
        instantiator = kwargs.get("instantiator", None)
        is_parent = kwargs.get("is_parent", False)

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
            "",
            str,
            descr="Core version.",
        )
        self.set_default_attribute(
            "previous_version",
            self.version,
            str,
            descr="Core previous version.",
        )
        self.set_default_attribute(
            "setup_dir",
            "",
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
            "use_netlist",
            False,
            bool,
            descr="Copy `<SETUP_DIR>/CORE.v` netlist instead of `<SETUP_DIR>/hardware/src/*`",
        )
        self.set_default_attribute(
            "is_top_module",
            __class__.global_top_module == self,
            bool,
            descr="Selects if core is top module. Auto-filled. DO NOT CHANGE.",
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
            True,
            bool,
            descr="Select if should try to generate `<corename>.v` from py2hwsw dictionary. Otherwise, only generate `.vs` files.",
        )
        self.set_default_attribute(
            "parent",
            {},
            dict,
            descr="Select parent of this core (if any). If parent is set, that core will be used as a base for the current one. Any attributes of the current core will override/add to those of the parent.",
        )

        self.attributes_dict = copy.deepcopy(attributes)

        self.abort_reason = None
        # Don't setup this core if using a project wide special target.
        if __class__.global_special_target:
            self.abort_reason = "special_target"
        # Don't setup this core if it is the same as the top module.
        # May happen if the top module is listed in 'blocks' of a submodule (likely wrapper).
        if (
            attributes["original_name"] == __class__.global_top_module.original_name
            and not self.is_top_module
        ):
            self.abort_reason = "duplicate_setup"

        # Read 'attributes' dictionary and set corresponding core attributes
        self.parse_attributes_dict(attributes)

        # Connect ports of this instance to external wires (wires of the instantiator)
        self.connect_instance_ports(connect, instantiator)

        if not self.is_top_module:
            self.build_dir = __class__.global_build_dir
        self.setup_dir = find_module_setup_dir(self.original_name)[0]
        # print(
        #     f"DEBUG: {self.name} {self.original_name} {self.build_dir} {self.is_top_module}",
        #     file=sys.stderr,
        # )

        if self.abort_reason:
            # Generate instance parameters when aborted due to duplicate setup
            if self.abort_reason == "duplicate_setup":
                param_gen.generate_inst_params(self)
            return

        self.__create_build_dir()

        # Copy files from LIB to setup various flows
        # (should run before copy of files from module's setup dir)
        if self.is_top_module:
            copy_srcs.flows_setup(self)

        # Copy files from the module's setup dir
        copy_srcs.copy_rename_setup_directory(self)

        # Generate config_build.mk
        if self.is_top_module:
            config_gen.config_build_mk(self)

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
            block_gen.generate_blocks_snippet(self)

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

        if self.is_top_module and not is_parent:
            self.post_setup()

    def post_setup(self):
        """Scripts to run at the end of the top module's setup"""
        # Replace Verilog snippet includes
        self._replace_snippet_includes()
        # Clean duplicate sources in `hardware/src` and its subfolders (like `hardware/simulation/src`)
        self._remove_duplicate_sources()
        # Generate docs
        doc_gen.generate_docs(self)
        # Generate ipxact file
        # if self.generate_ipxact: #TODO: When should this be generated?
        #    ipxact_gen.generate_ipxact_xml(self, reg_table, self.build_dir + "/ipxact")
        # Lint and format sources
        self.lint_and_format()

    def handle_parent(self, *args, **kwargs):
        """Create a new core based on parent core.
        returns: True if parent core was used. False otherwise.
        """
        is_parent = kwargs.pop("is_parent", False)
        attributes = kwargs.pop("attributes", {})
        child_attributes = kwargs.pop("child_attributes", {})
        if is_parent:
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
        is_first_module_called = belongs_to_top_module and not is_parent

        name = attributes.get("name", attributes["original_name"])
        # Update global build dir to match this module's name and version
        if is_first_module_called and not __class__.global_build_dir:
            version = attributes.get("version", "1.0")
            __class__.global_build_dir = f"../{name}_V{version}"

        filtered_parent_py_params = dict(parent)
        filtered_parent_py_params.pop("core_name", None)
        filtered_parent_py_params.pop("py2hwsw_target", None)
        filtered_parent_py_params.pop("build_dir", None)
        filtered_parent_py_params.pop("instantiator", None)
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
            instantiator=kwargs.get("instantiator", None),
        )

        # Copy parent attributes to child
        self.__dict__.update(parent_module.__dict__)
        self.setup_dir = find_module_setup_dir(attributes["original_name"])[0]

        if self.abort_reason:
            return True

        # Copy files from the module's setup dir
        copy_srcs.copy_rename_setup_directory(self)

        # Run post setup
        if is_first_module_called:
            self.post_setup()

        return True

    @staticmethod
    def append_child_attributes(parent_attributes, child_attributes):
        """Appends/Overrides parent attributes with child attributes"""
        for child_attribute_name, child_value in child_attributes.items():
            # Don't override child-specific attributes
            if child_attribute_name in ["original_name", "setup_dir", "parent"]:
                continue

            # Override other attributes of type string
            if type(child_value) is str:
                parent_attributes[child_attribute_name] = child_value
                continue

            # Override or append elements from list attributes
            assert (
                type(child_value) is list
            ), f"Invalid type for attribute '{child_attribute_name}': {type(child_value)}"

            # Select identifier attribute. Used to compare if should override each element.
            identifier = "name"
            if child_attribute_name in ["blocks", "sw_modules"]:
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
            version = attributes.get("version", "1.0")
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

    attrs = [
            "core_name",
		    "instance_name",
		    ["-p", "parameters", {"nargs": "+"}, "pairs"],
		    ["-c", "connect", {"nargs": "+"}, "pairs"],
		    ["--no_autoaddr", "autoaddr", {"action": "store_false"}],
		    ["--rw_overlap", "rw_overlap", {"action": "store_true"}],
		    ["--csr_if", "csr_if"],
		    {
		        "--csr-group&csrs": [
		            "name",
		            {
		                "-r&regs": [
		                    "name:n_bits",
                            ["-t", "type"],
		                    ["--rst_val", "rst_val"],
                            ["--addr", "addr", {"type":int}],
		                    ["--log2n_items", "log2n_items"],
		                    ["--no_autoreg", "autoreg", {"action": "store_false"}],
		                ],
		            },
		        ]
		    },
        ]

    @str_to_kwargs(attrs)
    def create_instance(self, core_name: str = "", instance_name: str = "", **kwargs):
        """Create an instante of a module, but only if we are not using a
        project wide special target (like clean)
        param core_name: Name of the core
        param instance_name: Verilog instance name
        """
        if self.abort_reason:
            return
        # Don't setup other destinations (like simulation) if this is a submodule and
        # the sub-submodule (we are trying to setup) is not for hardware/src/
        if not self.is_top_module and (
            self.dest_dir == "hardware/src"
            and "dest_dir" in kwargs
            and kwargs["dest_dir"] != "hardware/src"
        ):
            debug(f"Not setting up submodule '{core_name}' of '{self.name}' core!", 1)
            return

        assert core_name, fail_with_msg("Missing core_name argument", ValueError)
        # Ensure 'blocks' list exists
        self.set_default_attribute("blocks", [])
        # Ensure global top module is set
        self.update_global_top_module()

        # Set submodule destination dir equal to current module
        if "dest_dir" not in kwargs:
            kwargs["dest_dir"] = self.dest_dir

        try:
            instance = self.get_core_obj(
                core_name, instance_name=instance_name, instantiator=self, **kwargs
            )

            self.blocks.append(instance)
        except ModuleNotFoundError:
            add_traceback_msg(f"Failed to create instance '{instance_name}'.")
            raise

    def connect_memory(self, port, instantiator):
        """ Create memory port in instantiatior and connect it to self"""
        _name = f"{self.instance_name}_{port.interface.type}_s"
        _signals = {k: v for k, v in port.interface.__dict__.items() if k != "widths"}
        _signals.update(port.interface.widths)
        _signals.update({"prefix": f"{self.instance_name}_{port.interface.type}_"})
        instantiator.create_port(
            name=_name,
            signals = _signals,
            descr=port.descr
        )
        _port = find_obj_in_list(instantiator.ports, _name)
        port.connect_external(_port, bit_slices=[])

    def connect_instance_ports(self, connect, instantiator):
        """
        param connect: External wires to connect to ports of this instance
                       Key: Port name, Value: Wire name or tuple with wire name and signal bit slices
                       Tuple has format:
                       (wire_name, signal_name[bit_start:bit_end], other_signal[bit_start:bit_end], ...)
        param instantiator: Module that is instantiating this instance
        """
        # Connect instance ports to external wires
        for port_name, connection_value in connect.items():
            port = find_obj_in_list(self.ports, port_name)
            if not port:
                fail_with_msg(
                    f"Port '{port_name}' not found in instance '{self.instance_name}' of module '{instantiator.name}'!\n"
                    f"Available ports:\n- "
                    + "\n- ".join([port.name for port in self.ports])
                )

            bit_slices = []
            if type(connection_value) is str:
                wire_name = connection_value
            elif type(connection_value) is tuple:
                wire_name = connection_value[0]
                bit_slices = connection_value[1]
            else:
                fail_with_msg(f"Invalid connection value: {connection_value}")

            if type(bit_slices) is not list:
                fail_with_msg(
                    f"Second element of tuple must be a list of bit slices/connections: {connection_value}"
                )

            wire = find_obj_in_list(instantiator.wires, wire_name) or find_obj_in_list(
                instantiator.ports, wire_name
            )
            if not wire:
                fail_with_msg(
                    f"Wire/port '{wire_name}' not found in module '{instantiator.name}'!"
                )
            port.connect_external(wire, bit_slices=bit_slices)
        # find unconnected ports
        for port in self.ports:
            if not port.e_connect and port.interface:
                if port.interface.type in ["rom_sp", "rom_tdp", "ram_sp", "ram_tdp", "ram_2p"] and instantiator:
                    self.connect_memory(port, instantiator)

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

    def _remove_duplicate_sources(self):
        """Remove sources in the build directory from subfolders that exist in `hardware/src`"""
        # Go through all subfolders that may contain duplicate sources
        for subfolder in [
            "hardware/simulation/src",
            "hardware/fpga/src",
            "hardware/common_src",
        ]:

            # Get common srcs between `hardware/src` and current subfolder
            common_srcs = find_common_deep(
                os.path.join(self.build_dir, "hardware/src"),
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
            if path.name.endswith("version.vh") or "test_" in path.name:
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
        if __class__.global_project_vlint:
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
        sw_tools.run_tool("clang")
        sw_tools.run_tool("clang", self.build_dir)

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
            if "instantiator" in kwargs and kwargs["instantiator"]:
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
        py2_core_dict = {"original_name": default_core_name, "name": default_core_name}
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
            f"{iob_colors.INFO}Cleaning build directory: {module.build_dir}{iob_colors.ENDC}"
        )
        os.system(f"make -C {module.build_dir} clean")
        shutil.rmtree(module.build_dir)
        print(
            f"{iob_colors.INFO}Cleaning complete. Removed: {module.build_dir}{iob_colors.ENDC}"
        )

    @staticmethod
    def print_build_dir(core_name):
        """Print build directory."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_build_dir"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name)
        print(module.build_dir)

    @staticmethod
    def print_core_dict(core_name):
        """Print core attributes dictionary."""
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_core_dict"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name)
        print(json.dumps(module.attributes_dict, indent=4))

    @staticmethod
    def print_py2hwsw_attributes(core_name):
        """Print the supported py2hw attributes of this core.
        The attributes listed can be used in the 'attributes' dictionary of the
        constructor. This defines the information supported by the py2hw interface.
        """
        # Set project wide special target (will prevent normal setup)
        __class__.global_special_target = "print_attributes"
        # Build a new module instance, to obtain its attributes
        module = __class__.get_core_obj(core_name)
        print(
            f"Attributes supported by the '{module.name}' core's 'py2hwsw' interface:"
        )
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
            instantiator = kwargs.pop("instantiator", None)
            # Call `setup(<py_params_dict>)` function of `<core_name>.py` to
            # obtain the core's py2hwsw dictionary.
            # Give it a dictionary with all arguments of this function, since the user
            # may want to use any of them to manipulate the core attributes.
            core_dict = core_module.setup(
                {
                    # "core_name": core_name,
                    "build_dir": __class__.global_build_dir,
                    "py2hwsw_target": __class__.global_special_target or "setup",
                    "instantiator": (
                        instantiator.attributes_dict if instantiator else ""
                    ),
                    **kwargs,
                }
            )
            py2_core_dict = {"original_name": core_name, "name": core_name}
            py2_core_dict.update(core_dict)
            instance = __class__.py2hw(
                py2_core_dict,
                instantiator=instantiator,
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
            setup_dir=os.path.join(os.path.dirname(__file__), "../.."),
            build_dir="py2hwsw_docs",
        )
        copy_srcs.doc_setup(core)
        copy_srcs.copy_rename_setup_subdir(core, "document")
        with open(f"{core.build_dir}/config_build.mk", "w") as f:
            f.write("NAME=Py2HWSW\n")
        with open(f"{core.build_dir}/document/tsrc/{core.name}_version.tex", "w") as f:
            f.write(py2_version)


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
    # print("Found setup dir based on location of: " + file_path, file=sys.stderr)
    if file_ext == ".py" or file_ext == ".json":
        return os.path.dirname(file_path), file_ext
