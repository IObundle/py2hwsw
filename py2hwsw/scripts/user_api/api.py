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
from pydantic import BaseModel
from datetime import date
import os
import sys
import inspect
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')))
import iob_conf as internal_conf

#
# Utilities used by API
#
# TODO: Move these utilities to another file (maybe iob_base.py)


def _empty_list():
    return field(default_factory=list)


def _empty_dict():
    return field(default_factory=dict)


class ValidatingBaseModel(BaseModel):
    """
    Similar to BaseModel class of pydantic, but with validate_assignment=True.
    Also add '__post_init__' method for subclasses, for similar purpose as dataclasses __post_init__.
    """

    # Configure validate_assignment to validate all attributes when they are set.
    class Config:
        validate_assignment = True

    def __init__(self, **data):
        super().__init__(**data)
        # Additional initialization logic here
        self.__post_init__(**data)

    def __post_init__(self, **data):
        """
        A __post_init__ method, similar to the one in dataclasses, that can be overridden in subclasses.
        """
        pass


# NOTE: Update py2hwsw version every time API changes!
#       Must change major version if new API is not backwards compatible.
#       Change minor version when adding new API methods or other non-breaking changes.

#
# Confs
#

# Convert dict keys to python attributes
conf_dict2python = {
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
conf_short2python = [
    "name",
    ["-t", "kind"],
    ["-v", "value"],
    ["-m", "min_value"],
    ["-M", "max_value"],
]


# These functions should be called by py2 every time it exchanges objects with user.
def convert2api(internal_obj):
    """
    Convert given internal object to corresponding API object.

    Attributes:
        internal_obj (object): internal object
    Returns:
        object: api object
    """
    pass


def convert2internal(api_obj):
    """
    Convert given API object to corresponding internal object.

    Attributes:
        api_obj (object): API object
    Returns:
        object: internal object
    """
    pass


def get_methods(cls):
    """
    Returns all non-default methods in a class (includes ones inherited from superclasses)

    Attributes:
        cls (class): class
    Returns:
        dict: methods of the class and their type hints
    """
    methods = {}
    for name in dir(cls):
        attr = getattr(cls, name)
        if inspect.isfunction(attr) and not name.startswith("__"):
            signature = inspect.signature(attr)
            methods[name] = signature
    return methods


def has_body(func):
    """Check if a function has a body."""
    source = inspect.getsource(func)
    # Remove leading and trailing whitespace
    source = source.strip()
    # Remove the function definition line
    lines = source.split('\n')
    if len(lines) < 2:
        return False
    body = '\n'.join(lines[1:])
    return body.strip() != 'pass'


def api_for(internal_cls):
    """
    Decorator for creating API interface. Apply this decorator to every function in the API.

    This decorator:
    1) Passes attributes defined in the API class to the internal class (via arguments to the internal classes's constructor)
    2) Creates setters/getters for every attribute of API class, but actually accessing internal classes's attributes.
    3) Replaces (abstract) API methods with functions that call the corresponding internal class methods.
    4) Removes attributes from API class. This prevents user from trying to access attributes directly.

    From point of view of the user (even when checking api.py code), he only sees API class with the (getters/setters of the) attributes and methods defined in it.
    The user may instantiate any API class and use its attributes/methods. This decorator will handle the instantiation of the internal class and hide it from user.

    With this decorator, when the user instantiates API class, two objects are created: the API object and the internal object.
    The API object is returned to user. The internal object is stored internally by py2.
    The API and internal objects have a unique id and are associated with each other in a mapping stored internally by py2.

    When py2 needs to pass objects to the user, py2 should only pass API objects (converting from internal objects if needed).
    When the user needs to pass objects to py2, he passes API objects, which py2 will convert to internal objects.

    Attributes:
        internal_cls (class): Reference to internal class that will extend functionality of API class being decorated.
    Returns:
        class: Updated API class
    """

    # Create decorator dynamically for the API class
    def decorator(cls):
        # Get attributes and their default values
        attributes = {k: cls.__dict__[k] for k in cls.__annotations__}
        methods = get_methods(cls)

        # Update constructor of the API class
        def new_init(self, *args, **kwargs):
            print("API class constructor called: ", cls.__name__)
            print("Attributes: ", attributes) # Dictionary with attributes and their types
            print("Annotations: ", cls.__annotations__) # Dictionary with attributes and their types
            print("Methods: ", methods) # Dictionary with methods and their types

            # Instantiate internal class with API attributes
            internal_obj = internal_cls(attributes, cls.__annotations__, args, kwargs)

            # Store reference to internal object
            self.__internal_obj = internal_obj

        cls.__init__ = new_init

        # Local utility functions
        def _generate_setter(attribute_name):
            """
            Function to generate setter for a given attribute.
            Setter will pass the given value to the corresponding attribute in the internal object.
            """

            def setter(self, value):
                # print("Setter called for attribute: ", attribute_name)
                setattr(self.__internal_obj, attribute_name, value)
            return setter

        def _generate_getter(attribute_name):
            """
            Function to generate getter for a given attribute.
            Getter will get value from the corresponding attribute in the internal object.
            """

            def getter(self):
                # print("Getter called for attribute: ", attribute_name)
                return getattr(self.__internal_obj, attribute_name)
            return getter

        def _generate_method_wrapper(method_name):
            """
            Function to generate wrapper for a given method.
            Wrapper will call the corresponding method in the internal object.
            """

            def wrapper(self, *args, **kwargs):
                assert hasattr(self.__internal_obj, method_name), f"[Py2HWSW bug]: Missing implementation for API method '{method_name}' of class '{cls.__name__}'!"
                # print("Method called: ", method_name)
                return getattr(self.__internal_obj, method_name)(*args, **kwargs)
            return wrapper

        # Generate and add setters/getters for each attribute of API class, referencing values from corresponding attribute in internal object
        for name in cls.__annotations__:
            setattr(cls, f"set_{name}", _generate_setter(name))
            setattr(cls, f"get_{name}", _generate_getter(name))

        # Replace API methods by calls to the internal methods
        for name in methods:
            # Ensure method is abstract (does not have body) in API class
            assert not has_body(getattr(cls, name)), f"API method '{name}' must be abstract."

            # Call corresponding method in internal class
            setattr(cls, name, _generate_method_wrapper(name))

        # Remove class attributes from API class
        # This will make sure user cannot access them directly.
        for name in cls.__annotations__:
            delattr(cls, name)

        return cls

    return decorator

#
# API classes, attributes, and methods
#
# Notes:
# - Every attribute must be accessed via setter/getter methods.
#   Users should use corresponding getters/setters [like `get_<attribute_name>()`/`set_<attribute_name>()`].
#   Some of these methods may be automatically generated by the decorator.
# - Classes have similar structure to python's '@dataclasses'
# - Methods are abstract. They do not contain implementation.


@api_for(internal_conf.iob_conf)
class iob_conf():
    """
    Class to represent a configuration option.

    Attributes:
        name (str): Configuration identifier name.
        kind (str): Configuration type, either M (Verilog macro), P (Verilog parameter), C (Constant) or D (Derived Parameter).
                    False-parameters are the same as verilog parameters except that the its value must not be overriden.
        value (str): Configuration value.
        min_value (str): Minimum value supported by the configuration option (NA if not applicable).
        max_value (str): Maximum value supported by the configuration option (NA if not applicable).
        descr (str): Description of the configuration option.
        if_defined (str): Only applicable to Verilog macros: Conditionally enable this configuration if the specified Verilog macro is defined.
        if_not_defined (str): Only applicable to Verilog macros: Conditionally enable this configuration if the specified Verilog macro is undefined.
        doc_only (bool): If enabled, configuration option will only appear in documentation. Not in the verilog code.
    """

    name: str = ""
    kind: str = "P"
    value: str | int | bool = ""
    min_value: str | int = "NA"
    max_value: str | int = "NA"
    descr: str = "Default description"
    if_defined: str = ""
    if_not_defined: str = ""
    doc_only: bool = False

    def test_method(self, var1: str, var2: int) -> list:
        pass


# Convert dict keys to python attributes
conf_group_dict2python = {
    "name": "name",
    "descr": "descr",
    "confs": "confs",
    "doc_only": "doc_only",
    "doc_clearpage": "doc_clearpage",
}

# Convert short notation to python attributes
conf_group_short2python = [
    "name",
    ["-c", "confs", {"nargs": "+"}],
]


@api_for(internal_conf.iob_conf_group)
class iob_conf_group(ABC):
    """
    Class to represent a group of configurations.

    Attributes:
        name (str): Configuration group identifier name.
        descr (str): Description of the configuration group.
        confs (list): List of configuration objects.
        doc_only (bool): If enabled, configuration group will only appear in documentation. Not in the verilog code.
        doc_clearpage (bool): If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    """

    name: str = ""
    descr: str = "Default description"
    confs: list[iob_conf] = _empty_list()
    doc_only: bool = False
    doc_clearpage: bool = False


#
# Signals
#

# Convert dict keys to python attributes
signal_dict2python = {
    "name": "name",
    "width": "width",
    "descr": "descr",
    "isvar": "isvar",
    "isreg": "isreg",
    "reg_signals": "reg_signals",
    "val": "value",
}

# Convert short notation to python attributes
signal_short2python = [
    # TODO:
]


@dataclass
class iob_signal(ABC):
    """
    Class that represents a wire/port signal.

    Attributes:
        name (str): Identifier name for the signal.
        width (str or int): Number of bits in the signal.
        descr (str): Description of the signal.
        isvar (bool): If enabled, signal will be generated with type `reg` in Verilog.
        # isreg (bool): Used for `iob_comb`: If enabled, iob_comb will infer a register for this signal.
        # reg_signals (list): Used for `iob_comb`: List of signals associated to the infered register.
        # value (str or int): Logic value for future simulation effort using global signals list.
    """

    name: str = ""
    width: str or int = 1
    descr: str = "Default description"
    isvar: bool = False

    # # Used for `iob_comb`: If enabled, iob_comb will infer a register for this signal.
    # isreg: bool = False
    # # Used for `iob_comb`: List of signals associated to the infered register.
    # reg_signals: list[str] = _empty_list()

    # Logic value for future simulation effort using global signals list.
    # See 'TODO' in iob_core.py for more info: https://github.com/IObundle/py2hwsw/blob/a1e2e2ee12ca6e6ad81cc2f8f0f1c1d585aaee73/py2hwsw/scripts/iob_core.py#L251-L259
    # value: str or int = 0


#
# if_gen
#

# Convert dict keys to python attributes
interface_dict2python = {
    "type": "kind",
    "prefix": "prefix",
    "mult": "mult",
    "params": "params",
    "widths": "widths",
    "file_prefix": "file_prefix",
    "portmap_port_prefix": "portmap_port_prefix",
}

# Convert short notation to python attributes
interface_short2python = [
    # TODO:
]


# NOTE: artur: I believe the 'params' attribute could be merged with 'widths' attibute.
@dataclass
class interface(ABC):
    """
    Class to represent an interface for generation.

    Attributes:
        kind (str): Type/Name of interface to generate.
        prefix (str): Prefix for signals of the interface.
        mult (str or int): Width multiplier. Used when concatenating multiple instances of the interface.
        params (str): Generic string parameter that is passed to "get_<interface>_ports" function
        widths (dict[str, str]): Dictionary of width properties of interface.
        file_prefix (str): Prefix for generated "Verilog Snippets" of this interface.
        portmap_port_prefix (str): Prefix for "Verilog snippets" of portmaps of this interface:
    """

    kind: str = ""
    prefix: str = ""
    mult: str | int = 1
    params: str = None
    widths: dict[str, str] = _empty_dict()
    file_prefix: str = ""
    portmap_port_prefix: str = ""


#
# Wires
#

# Convert dict keys to python attributes
wire_dict2python = {
    "type": "kind",
    "interface": "interface",
    "descr": "descr",
    "if_defined": "if_defined",
    "if_not_defined": "if_not_defined",
    "signals": "signals",
}

# Convert short notation to python attributes
wire_short2python = [
    "name",
    ["-i", "signals&i", {"nargs": 1}, ("type",)],
    ["-s", "signals&s", {"nargs": "+"}, ["name:width"]],
]


@dataclass
class iob_wire(ABC):
    """
    Class to represent a wire in an iob module.

    Attributes:
        name (str): Identifier name for the wire.
        interface (interface): Name of the standard interface to auto-generate with `if_gen.py` script.
        descr (str): Description of the wire.
        if_defined (str): Conditionally define this wire if the specified Verilog macro is defined/undefined.
        if_not_defined (str): Conditionally define this wire if the specified Verilog macro is defined/undefined.
        signals (list): List of signals belonging to this wire
                        (each signal represents a hardware Verilog wire).
    """

    name: str = ""
    interface: interface = None
    descr: str = "Default description"
    if_defined: str = ""
    if_not_defined: str = ""
    signals: list[iob_signal] = _empty_list()

    @abstractmethod
    def get_signal(self, signal_name: str) -> iob_signal:
        """
        Find a signal by name and return it.

        Args:
            signal_name (str): Name of the signal to find

        Returns:
            iob_signal: The found signal.
        """
        pass


#
# Ports
#

# Convert dict keys to python attributes
port_dict2python = {
    "e_connect": "e_connect",
    "e_connect_bit_slices": "e_connect_bit_slices",
    "doc_only": "doc_only",
    "doc_clearpage": "doc_clearpage",
    # And others inherited from iob_wire
}

# Convert short notation to python attributes
port_short2python = [
    # Inherited from iob_wire
]


@dataclass
class iob_port(iob_wire):
    """
    Describes an IO port.

    Attributes:
        e_connect (iob_wire): External wire to connect to.
        e_connect_bit_slices (list): List of bit slices of signals in e_connect
        doc_only (bool): Only add to documentation
        doc_clearpage (bool): If enabled, the documentation table for this port will be terminated by a TeX '\clearpage' command.
    """

    e_connect: iob_wire = None
    # FIXME: Constrain values received by bit slices
    e_connect_bit_slices: list[object] = _empty_list()
    doc_only: bool = False
    doc_clearpage: bool = False


#
# Snippets
#

# Convert dict keys to python attributes
snippet_dict2python = {
    "verilog_code": "verilog_code",
}

# Convert short notation to python attributes
snippet_short2python = [
    # TODO:
]


@dataclass
class iob_snippet(ABC):
    """
    Class to represent a Verilog snippet in an iob module.

    Attributes:
        verilog_code (str): Verilog code string
    """

    verilog_code: str = ""


#
# Comb
#

# Convert dict keys to python attributes
comb_dict2python = {
    "code": "code",
    "clk_if": "clk_if",
}

# Convert short notation to python attributes
comb_short2python = [
    # TODO:
]


@dataclass
class iob_comb(iob_snippet):
    """
    Class to represent a Verilog combinatory circuit in an iob module.

    Attributes:
        code (str): Verilog code string
        clk_if (str): Clock interface
    """

    code: str = ""
    clk_if: str = "c_a"


#
# FSM
#

# Convert dict keys to python attributes
fsm_dict2python = {
    "type": "kind",
    "default_assignments": "default_assignments",
    "state_descriptions": "state_descriptions",
}

# Convert short notation to python attributes
fsm_short2python = [
    # TODO:
]


@dataclass
class iob_fsm(iob_comb):
    """
    Class to represent a Verilog finite state machine in an iob module.

    Attributes:
        kind (str): Type of the finite state machine.
        default_assignments (str): Verilog code string to be assigned to the state register on reset.
        state_descriptions (str): Verilog code string to be used for state description
    """

    kind: str = "prog"
    default_assignments: str = ""
    state_descriptions: str = ""


#
# Blocks
#
class iob_core(ABC):
    """Forward reference of iob_core class. Full declaration of iob_core class is available in below."""

    pass


# Convert dict keys to python attributes
block_group_dict2python = {
    "name": "name",
    "descr": "descr",
    "blocks": "blocks",
    "doc_clearpage": "doc_clearpage",
}

# Convert short notation to python attributes
block_group_short2python = [
    "name",
    ["-b", "blocks", {"nargs": "+"}],
]


@dataclass
class iob_block_group(ABC):
    """
    Class to represent a group of blocks.

    Attributes:
        name (str): Name of the block group.
        descr (str): Description of the block group.
        blocks (list): List of blocks in the block group.
        doc_clearpage (bool): If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    """

    name: str = ""
    descr: str = "Default description"
    blocks: list[iob_core] = _empty_list()
    doc_clearpage: bool = False


#
# License
#

# Convert dict keys to python attributes
license_dict2python = {
    "name": "name",
    "year": "year",
    "author": "author",
}

# Convert short notation to python attributes
license_short2python = [
    # TODO:
]


@dataclass
class iob_license(ABC):
    """
    Class that represents a license attribute.

    Attributes:
        name (str): Name of the license.
        year (int): Year of the license.
        author (str): Author of the license.
    """

    name: str = "MIT"
    year: int = date.today().year
    author: str = "IObundle, Lda"


#
# Core
#

# Convert dict keys to python attributes
module_dict2python = {
    "original_name": "original_name",
    "name": "name",
    "description": "description",
    "reset_polarity": "reset_polarity",
    "confs": "confs",
    "ports": "ports",
    "wires": "wires",
    "snippets": "snippets",
    "comb": "comb",
    "fsm": "fsm",
    "subblocks": "subblocks",
    "superblocks": "superblocks",
    "sw_modules": "sw_modules",
}

# Convert short notation to python attributes
module_short2python = [
    "original_name",
]


# We should prevent users from instantiating this class (they should instantiate iob_core instead)
@dataclass
class iob_module(ABC):
    """
    Class to describe a (Verilog) module.

    Attributes:
        original_name (str): Original name of the module. (The module name commonly used in the files of the setup dir.)
        name (str): Name of the generated module.
        description (str): Description of the module.
        reset_polarity (str): Global reset polarity of the module. Can be 'positive' or 'negative'. (Will override all subblocks' reset polarities).
        confs (list): List of module macros and Verilog (false-)parameters
        ports (list): List of module ports
        wires (list): List of wires
        snippets (list): List of Verilog code snippets
        comb (iob_comb): Combinational circuit
        fsm (iob_fsm): Finite state machine
        subblocks (list): List of instances of other cores inside this core.
        superblocks (list): List of wrappers for this core. Will only be setup if this core is a top module, or a wrapper of the top module.
        sw_modules (list): List of software modules required by this core.
    """

    original_name: str = None
    name: str = ""
    description: str = "Default description"
    reset_polarity: str = None
    confs: list[iob_conf_group] = _empty_list()
    ports: list[iob_port] = _empty_list()
    wires: list[iob_wire] = _empty_list()
    snippets: list[iob_snippet] = _empty_list()
    comb: iob_comb = None
    fsm: iob_fsm = None
    subblocks: list[iob_block_group] = _empty_list()
    superblocks: list[iob_block_group] = _empty_list()
    sw_modules: list[iob_block_group] = _empty_list()


# Convert dict keys to python attributes
instance_dict2python = {
    "instance_name": "instance_name",
    "instance_description": "instance_description",
    "parameters": "parameters",
    "if_defined": "if_defined",
    "if_not_defined": "if_not_defined",
    "instantiate": "instantiate",
    "connect": "connect",
}

# Convert short notation to python attributes
instance_short2python = [
    "instance_name",
    ["-p", "parameters", {"nargs": "+"}, "pairs"],
    ["--no_instance", "instantiate", {"action": "store_false"}],
    ["-c", "connect", {"nargs": "+"}, "pairs"],
]


# We should prevent users from instantiating this class (they should instantiate iob_core instead)
@dataclass
class iob_instance(ABC):
    """
    Class to describe a module's (Verilog) instance.

    Attributes:
        instance_name (str): Name of the instance. (Will be used as the instance's name in the Verilog module).
        instance_description (str): Description of the instance.
        parameters (dict): Verilog parameter values for this instance.
        if_defined (str): Only use this instance in Verilog if given Verilog macro is defined.
        if_not_defined (str): Only use this instance in Verilog if given Verilog macro is not defined.
        instantiate (bool): Select if should intantiate the module inside another Verilog module.
        connect (dict): Connections for ports of the instance.
    """

    instance_name: str = None
    instance_description: str = ""
    parameters: dict[str, int | str] = _empty_dict()
    if_defined: str = ""
    if_not_defined: str = ""
    instantiate: bool = ""
    connect: dict[str, str] = _empty_dict()


# Convert dict keys to python attributes
core_dict2python = {
    "version": "version",
    "previous_version": "previous_version",
    "setup_dir": "setup_dir",
    "build_dir": "build_dir",
    "use_netlist": "use_netlist",
    "is_system": "is_system",
    "board_list": "board_list",
    "dest_dir": "dest_dir",
    "ignore_snippets": "ignore_snippets",
    "generate_hw": "generate_hw",
    "parent": "parent",
    "is_top_module": "is_top_module",
    "is_superblock": "is_superblock",
    "is_tester": "is_tester",
    "python_parameters": "python_parameters",
    "license": "license",
    "doc_conf": "doc_conf",
    "title": "title",
}

# Convert short notation to python attributes
core_short2python = [
    ["--dest_dir", "dest_dir"],
    # Should short notation for CSRs be here?
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
                    ["-m", "mode"],
                    ["--rst_val", "rst_val"],
                    ["--addr", "addr", {"type": int}],
                    ["--log2n_items", "log2n_items"],
                ],
            },
        ]
    },
]


@dataclass
class iob_core(iob_module, iob_instance):
    """
    Generic class to describe how to generate a base IOb IP core.

    Attributes:
        version (str): Core version. By default is the same as Py2HWSW version.",
        previous_version (str): Core previous version.",
        setup_dir (str): Path to root setup folder of the core.",
        build_dir (str): Path to folder of build directory to be generated for this project.",
        # instance_name (str): Name of an instance of this class.",
        use_netlist (bool): Copy `<SETUP_DIR>/CORE.v` netlist instead of `<SETUP_DIR>/hardware/src/*`",
        is_system (bool): Sets `IS_FPGA=1` in config_build.mk",
        board_list (list): List of FPGAs supported by this core. A standard folder will be created for each board in this list.",
        dest_dir (str): Relative path inside build directory to copy sources of this core. Will only sources from `hardware/src/*`",
        ignore_snippets (list): List of `.vs` file includes in verilog to ignore.",
        generate_hw (bool): Select if should try to generate `<corename>.v` from py2hwsw dictionary. Otherwise, only generate `.vs` files.",
        parent (dict): Select parent of this core (if any). If parent is set, that core will be used as a base for the current one. Any attributes of the current core will override/add to those of the parent.",
        is_top_module (bool): Selects if core is top module. Auto-filled. DO NOT CHANGE.",
        is_superblock (bool): Selects if core is superblock of another. Auto-filled. DO NOT CHANGE.",
        is_tester (bool): Generates makefiles and depedencies to run this core as if it was the top module. Used for testers (superblocks of top moudle).",
        python_parameters (list): List of core Python Parameters. Used for documentation.",
        license (iob_license): License for the core.",
        doc_conf (str): CSR Configuration to use.",
        title (str): Title of this core. Used for documentation.",
    """

    version: str = None
    previous_version: str = None
    setup_dir: str = None
    build_dir: str = "build"
    # instance_name: str = None
    use_netlist: bool = False
    is_system: bool = False
    board_list: list[str] = _empty_list()
    # dest_dir: str = "" # Should not be visible to the user
    ignore_snippets: list[str] = _empty_list()
    generate_hw: bool = False
    parent: dict = _empty_dict()  # FIXME: not sure if this will be needed in pythase?
    is_top_module: bool = False
    is_superblock: bool = False
    is_tester: bool = False
    python_parameters: list[object] = _empty_list()
    license: iob_license = None
    doc_conf: str = ""
    title: str = ""

    @abstractmethod
    def __init__(self, core_dictionary: dict = {}):
        """
        Constructor for cores.

        Attributes:
            core_dictionary (dict): Optional dictionary to initialize core attributes.
        """
        pass

    @abstractmethod
    def generate_build_dir(self):
        """
        Standard method to generate build directory.
        May be overridden by user subclasses to generate custom files or run scripts during the build directory generation process.
        """
        pass
