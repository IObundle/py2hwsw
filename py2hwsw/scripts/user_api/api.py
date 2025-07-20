# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""
Here we define the user API for Py2HWSW.
"""

# User API for interfacing with Py2HWSW
#
# Py2HWSW has 3 user interfaces in total:
# - Dictionary/JSON interface
# - Short notation interface
# - API interface
#
# The classes specify the API interface. User may instantiate/use any of the classes,
# their attributes, and methods.
#
# The 'create_*_from_dict' methods allow creating API objects from the dictionary/JSON interface.
# The 'create_*_from_text' methods allow creating API objects from the short notation interface.


import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
)
from api_base import api_for, empty_list, empty_dict
import iob_port as py2hwsw_port
import iob_conf as py2hwsw_conf
import iob_wire as py2hwsw_wire
import iob_snippet as py2hwsw_snippet
import iob_core as py2hwsw_core
from py2hwsw_version import PY2HWSW_VERSION  # should be renamed to iob_version


#
# Confs
#


@api_for(py2hwsw_conf.iob_conf)
class iob_conf:
    """
    Class to represent a configuration option.

    Attributes:
        name (str): Configuration identifier name.
        kind (str): Configuration type, either M (Verilog macro), P (Verilog parameter), C (Constant) or D (Derived Parameter).
                    False-parameters are the same as verilog parameters except that the its value must not be overriden.
        value (str | int | bool): Configuration value.
        min_value (str | int): Minimum value supported by the configuration option (NA if not applicable).
        max_value (str | int): Maximum value supported by the configuration option (NA if not applicable).
        descr (str): Description of the configuration option.
        doc_only (bool): If enabled, configuration option will only appear in documentation. Not in the verilog code.
    """

    name: str = ""
    kind: str = "P"
    value: str | int | bool = ""
    min_value: str | int = "NA"
    max_value: str | int = "NA"
    descr: str = "Default description"
    doc_only: bool = False


@api_for(py2hwsw_conf.conf_from_dict)
def create_conf_from_dict(conf_dict):
    """
    Function to create iob_conf object from dictionary attributes.

    Attributes:
        conf_dict (dict): dictionary with values to initialize attributes of iob_conf object.
            This dictionary supports the following keys corresponding to the iob_conf attributes:
            - name           -> iob_conf.name
            - kind           -> iob_conf.kind
            - value          -> iob_conf.value
            - min_value      -> iob_conf.min_value
            - max_value      -> iob_conf.max_value
            - descr          -> iob_conf.descr
            - doc_only       -> iob_conf.doc_only

    Returns:
        iob_conf: iob_conf object
    """
    pass


#
# Wires
#


@api_for(py2hwsw_wire.iob_wire)
class iob_wire:
    """
    Class that represents a core's py2hwsw wire.

    Attributes:
        name (str): Name for the wire inside the core. Verilog wire will be generated with this name.
        width (str or int): Number of bits in the wire.
        descr (str): Description of the wire.
        isvar (bool): If enabled, wire will be generated with type `reg` in Verilog.
    """

    name: str = ""
    width: str or int = 1
    descr: str = "Default description"
    isvar: bool = False


@api_for(py2hwsw_wire.wire_from_dict)
def create_wire_from_dict(wire_dict):
    """
    Function to create iob_wire object from dictionary attributes.

    Attributes:
        wire_dict (dict): dictionary with values to initialize attributes of iob_wire object.
            This dictionary supports the following keys corresponding to the iob_wire attributes:
            - name          -> iob_wire.name
            - width         -> iob_wire.width
            - descr         -> iob_wire.descr
            - isvar         -> iob_wire.isvar

    Returns:
        iob_wire: iob_wire object
    """
    pass


#
# Ports
#


@api_for(py2hwsw_port.iob_port)
class iob_port:
    """
    Describes an IO port.

    Attributes:
        wire (iob_wire): Reference to the wire that is connected to the port.
        direction (str): Port direction
        doc_only (bool): Only add to documentation
        doc_clearpage (bool): If enabled, the documentation table for this port will be terminated by a TeX '\clearpage' command.
    """

    wire: iob_wire = None
    direction: str = ""
    doc_only: bool = False
    doc_clearpage: bool = False


@api_for(py2hwsw_port.port_from_dict)
def create_port_from_dict(port_dict):
    """
    Function to create iob_port object from dictionary attributes.

    Attributes:
        port_dict (dict): dictionary with values to initialize attributes of iob_port object.
            This dictionary supports the following keys corresponding to the iob_port attributes:
            - wire -> iob_port.wire
            - doc_only -> iob_port.doc_only
            - doc_clearpage -> iob_port.doc_clearpage

    Returns:
        iob_port: iob_port object
    """
    pass


#
# Snippets
#


@api_for(py2hwsw_snippet.iob_snippet)
class iob_snippet:
    """
    Class to represent a Verilog snippet in an iob module.

    Attributes:
        verilog_code (str): Verilog code string
    """

    verilog_code: str = ""


@api_for(py2hwsw_snippet.snippet_from_dict)
def create_snippet_from_dict(snippet_dict):
    """
    Function to create iob_snippet object from dictionary attributes.

    Attributes:
        snippet_dict (dict): dictionary with values to initialize attributes of iob_snippet object.
            This dictionary supports the following keys corresponding to the iob_snippet attributes:
            - verilog_code -> iob_snippet.verilog_code

    Returns:
        iob_snippet: iob_snippet object
    """
    pass


#
# Core
#


@api_for(py2hwsw_core.iob_core)
class iob_core:
    """
    Generic class to describe how to generate a base IOb IP core.

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
        comb (iob_comb): Combinational circuit
        fsm (iob_fsm): Finite state machine
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

    # Module attributes
    # FIXME: Remove original_name attribute. Create py2hwsw `get_original_name()` method that obtains class name dynamically.
    # The lack of this attribute may cause some issues for .json cores, or cores created with iob_core(core_dict).
    # But we can probably work around this by creating dynamic subclasses of iob_core with the correct name.
    original_name: str = None
    name: str = ""
    description: str = "Default description"
    # reset_polarity: str = "positive"
    confs: list[iob_conf] = empty_list()
    wires: list[iob_wire] = empty_list()
    ports: list[iob_port] = empty_list()
    # buses: list[iob_bus] = empty_list()
    # interfaces: list[iob_interface] = empty_list()
    snippets: list[iob_snippet] = empty_list()
    # comb: iob_comb | None = None
    # fsm: iob_fsm | None = None
    # subblocks: list[iob_instance] = empty_list()
    # superblocks: list[iob_core] = empty_list()
    # sw_modules: list[iob_core] = empty_list()

    # Core attributes
    # version: str = PY2HWSW_VERSION
    # previous_version: str = PY2HWSW_VERSION
    setup_dir: str = None
    build_dir: str = "build"
    # use_netlist: bool = False
    # is_system: bool = False
    # board_list: list[str] = empty_list()
    # ignore_snippets: list[str] = empty_list()
    generate_hw: bool = False
    # is_tester: bool = False
    # iob_parameters: list[iob_parameter_group] = empty_list()
    # license: iob_license = field(default_factory=iob_license)
    # doc_conf: str = ""
    # title: str = ""
    # dest_dir: str = "hardware/src"

    def __init__(self, core_dictionary: dict = {}):
        """
        Constructor for cores.

        Attributes:
            core_dictionary (dict): Optional dictionary to initialize core attributes.
        """
        pass

    def generate_build_dir(self):
        """
        Standard method to generate build directory.
        May be overridden by user subclasses to generate custom files or run scripts during the build directory generation process.
        """
        pass


@api_for(py2hwsw_core.core_from_dict)
def create_core_from_dict(core_dict):
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
            - confs -> iob_module.confs
            - wires -> iob_module.wires
            - ports -> iob_module.ports
            - buses -> iob_module.buses
            - interfaces -> iob_module.interfaces
            - snippets -> iob_module.snippets
            - comb -> iob_module.comb
            - fsm -> iob_module.fsm
            - subblocks -> iob_module.subblocks = [create_core_from_dict(i) for i in subblocks]
            - superblocks -> iob_module.superblocks = [create_core_from_dict(i) for i in superblocks]
            - sw_modules -> iob_module.sw_modules = [create_core_from_dict(i) for i in sw_modules]

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

    Returns:
        iob_core: iob_core object
    """
    pass
