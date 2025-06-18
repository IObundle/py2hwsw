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
# The 'dict2python' dictionary maps between the dictionary/JSON interface and the API
# interface.
# The 'short2python' dictionary maps between the short notation interface and the API
# interface.
#
# The mapping between the two interfaces does not have to be 1:1. Some mapping keys
# may call special conversion methods instead of setting the attribute directly.


# To achieve backwards compatibility, consider the following best practices:
#
# - Add new methods, don't change existing ones:
#       When adding new functionality, introduce new methods or interfaces instead of
#       modifying existing ones. This ensures that existing user code will not break.
# - Use default values or optional parameters:
#       When adding new parameters to existing methods, use default values or make
#       them optional to avoid breaking existing user code.
# - Avoid removing methods or interfaces:
#       Once a method or interface is published, avoid removing it in future versions.
#       Instead, consider deprecating it and providing a replacement or alternative
#       implementation.
# - Document changes and deprecations:
#       Clearly document any changes, deprecations, or removals in your API, including
#       the version number or identifier where the change occurred. This helps users
#       understand the impact of updates and plan accordingly.


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import date

# NOTE: Update version every time API changes!
API_VERSION = "1.0"

#
# Confs
#

# Convert dict keys to python attributes
dict2python = {
    "name": "name",
    "type": "kind",
    "val": "value",
    "min": "min_value",
    "max": "max_value",
    "descr": "descr",
    "if_defined": "if_defined",
    "if_not_defined": "if_not_defined",
    "doc_only": "doc_only",
}

# Convert short notation to python attributes
short2python = [
    "name",
    ["-t", "kind"],
    ["-v", "value"],
    ["-m", "min_value"],
    ["-M", "max_value"],
]


@dataclass
class iob_conf:
    """Class to represent a configuration option."""

    # Identifier name for the configuration option.
    name: str = ""
    # Type of configuration option, either M (Verilog macro), P (Verilog parameter), C (Constant) or D (Derived Parameter).
    # False-parameters are the same as verilog parameters except that the its value must not be overriden.
    kind: str = "P"
    # Value of the configuration option.
    value: str | int | bool = ""
    # Minimum value supported by the configuration option (NA if not applicable).
    min_value: str | int = "NA"
    # Maximum value supported by the configuration option (NA if not applicable).
    max_value: str | int = "NA"
    # Description of the configuration option.
    descr: str = "Default description"
    # Only applicable to Verilog macros: Conditionally enable this configuration if the specified Verilog macro is defined/undefined.
    if_defined: str = ""
    if_not_defined: str = ""
    # If enabled, configuration option will only appear in documentation. Not in the verilog code.
    doc_only: bool = False


# Convert dict keys to python attributes
dict2python = {
    "name": "name",
    "descr": "descr",
    "confs": "confs",
    "doc_only": "doc_only",
    "doc_clearpage": "doc_clearpage",
}

# Convert short notation to python attributes
short2python = [
    "name",
    ["-c", "confs", {"nargs": "+"}],
]


@dataclass
class iob_conf_group:
    """Class to represent a group of configurations."""

    # Identifier name for the group of configurations.
    name: str = ""
    # Description of the configuration group.
    descr: str = "Default description"
    # List of configuration objects.
    confs: list[iob_conf]
    # If enabled, configuration group will only appear in documentation. Not in the verilog code.
    doc_only: bool = False
    # If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    doc_clearpage: bool = False


#
# Signals
#

# Convert dict keys to python attributes
dict2python = {
    "name": "name",
    "width": "width",
    "descr": "descr",
    "isvar": "isvar",
    "isreg": "isreg",
    "reg_signals": "reg_signals",
    "val": "value",
}

# Convert short notation to python attributes
short2python = [
    # TODO:
]


@dataclass
class iob_signal:
    """Class that represents a wire/port signal"""

    # Identifier name for the signal.
    name: str = ""
    # Number of bits in the signal.
    width: str or int = 1
    # Description of the signal.
    descr: str = "Default description"
    # If enabled, signal will be generated with type `reg` in Verilog.
    isvar: bool = False

    # Used for `iob_comb`: If enabled, iob_comb will infer a register for this signal.
    isreg: bool = False
    # Used for `iob_comb`: List of signals associated to the infered register.
    reg_signals: list[str] = field(default_factory=list)

    # Logic value for future simulation effort using global signals list.
    # See 'TODO' in iob_core.py for more info: https://github.com/IObundle/py2hwsw/blob/a1e2e2ee12ca6e6ad81cc2f8f0f1c1d585aaee73/py2hwsw/scripts/iob_core.py#L251-L259
    value: str or int = 0


#
# if_gen
#

# Convert dict keys to python attributes
dict2python = {
    "type": "kind",
    "prefix": "prefix",
    "mult": "mult",
    "params": "params",
    "widths": "widths",
    "file_prefix": "file_prefix",
    "portmap_port_prefix": "portmap_port_prefix",
}

# Convert short notation to python attributes
short2python = [
    # TODO:
]


# NOTE: artur: I believe the 'params' attribute could be merged with 'widths' attibute.
@dataclass
class interface:
    """Class to represent an interface for generation"""

    # Type/Name of interface to generate
    kind: str = ""
    # Prefix for signals of the interface
    prefix: str = ""
    # Width multiplier. Used when concatenating multiple instances of the interface.
    mult: str | int = 1
    # Generic string parameter that is passed to "get_<interface>_ports" function
    params: str = None
    # Dictionary of width properties of interface
    widths: dict[str, str] = field(default_factory=dict)
    # Prefix for generated "Verilog Snippets" of this interface
    file_prefix: str = ""
    # Prefix for "Verilog snippets" of portmaps of this interface:
    portmap_port_prefix: str = ""


#
# Wires
#

# Convert dict keys to python attributes
dict2python = {
    "type": "kind",
    "interface": "interface",
    "descr": "descr",
    "if_defined": "if_defined",
    "if_not_defined": "if_not_defined",
    "signals": "signals",
}

# Convert short notation to python attributes
short2python = [
    "name",
    ["-i", "signals&i", {"nargs": 1}, ("type",)],
    ["-s", "signals&s", {"nargs": "+"}, ["name:width"]],
]


@dataclass
class iob_wire:
    """Class to represent a wire in an iob module"""

    # Identifier name for the wire.
    name: str = ""
    # Name of the standard interface to auto-generate with `if_gen.py` script.
    interface: interface = None
    # Description of the wire.
    descr: str = "Default description"
    # Conditionally define this wire if the specified Verilog macro is defined/undefined.
    if_defined: str = ""
    if_not_defined: str = ""
    # List of signals belonging to this wire
    # (each signal represents a hardware Verilog wire).
    signals: list[iob_signal]


#
# Ports
#
# Convert dict keys to python attributes
dict2python = {
    "e_connect": "e_connect",
    "e_connect_bit_slices": "e_connect_bit_slices",
    "doc_only": "doc_only",
    "doc_clearpage": "doc_clearpage",
    # And others inherited from iob_wire
}

# Convert short notation to python attributes
short2python = [
    # Inherited from iob_wire
]


@dataclass
class iob_port(iob_wire):
    """Describes an IO port."""

    # External wire that connects this port
    e_connect: iob_wire
    # Dictionary of bit slices for external connections. Name: signal name; Value: bit slice
    e_connect_bit_slices: list[object]  # FIXME: Constrain values received by bit slices
    # If enabled, port will only appear in documentation. Not in the verilog code.
    doc_only: bool = False
    # If enabled, the documentation table for this port will be terminated by a TeX '\clearpage' command.
    doc_clearpage: bool = False


#
# Snippets
#
@dataclass
class iob_snippet:
    """Class to represent a Verilog snippet in an iob module"""

    # List of outputs of this snippet (use to generate global wires)
    verilog_code: str = ""


#
# Comb
#
@dataclass
class iob_comb(iob_snippet):
    """Class to represent a Verilog combinatory circuit in an iob module"""

    code: str = ""
    clk_if: str = "c_a"


#
# FSM
#
@dataclass
class iob_fsm(iob_comb):
    """Class to represent a Verilog finite state machine in an iob module"""

    kind: str = "prog"
    default_assignments: str = ""
    state_descriptions: str = ""


#
# Blocks
#
class iob_core:
    """Forward reference of iob_core class. Full declaration of iob_core class is available in below."""

    pass


@dataclass
class iob_block_group:
    """Class to represent a group of blocks."""

    name: str = ""
    descr: str = "Default description"
    blocks: list[iob_core] = field(default_factory=list)
    doc_clearpage: bool = False


#
# License
#
@dataclass
class iob_license:
    """Class that represents a license attribute"""

    # Identifier name for the license.
    name: str = "MIT"
    # Year of the license.
    year: int = date.today().year
    # Author of the license.
    author: str = "IObundle, Lda"


#
# Core
#
@dataclass
class iob_module:
    """Class to describe a (Verilog) module"""

    original_name: str
    name: str
    description: str
    reset_polarity: str
    confs: list[iob_conf_group]
    ports: list[iob_port]
    wires: list[iob_wire]
    snippets: list[iob_snippet]
    comb: iob_comb
    fsm: iob_fsm
    subblocks: list[iob_block_group]
    superblocks: list[iob_block_group]
    sw_modules: list[iob_block_group]


@dataclass
class iob_instance:
    """Class to describe a module's (Verilog) instance"""

    instance_name: str
    instance_description: str
    parameters: dict[str, int | str]
    if_defined: str
    if_not_defined: str
    instantiate: bool


@dataclass
class iob_core(iob_module, iob_instance):
    """Generic class to describe how to generate a base IOb IP core"""

    version: str
    previous_version: str
    setup_dir: str
    build_dir: str
    # instance_name: str
    use_netlist: bool
    is_system: bool
    board_list: list[str]
    dest_dir: str
    ignore_snippets: list[str]
    generate_hw: bool
    parent: dict  # FIXME: not sure if this will be needed in pythase?
    is_top_module: bool
    is_superblock: bool
    is_tester: bool
    python_parameters: list[object]
    license: iob_license
    doc_conf: str
    title: str
