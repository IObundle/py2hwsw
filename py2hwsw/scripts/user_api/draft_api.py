# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

"""
DRAFT API for Py2HWSW. These are NOT production ready!
When these API components are stable, we will move them to the production-ready api.py file.
"""


import os
import sys
from datetime import date
from dataclasses import field

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
)
from api_base import api_for, empty_list, empty_dict
import iob_port as py2hwsw_port
import iob_interface as py2hwsw_interface
import iob_conf as py2hwsw_conf
import iob_wire as py2hwsw_wire
import iob_bus as py2hwsw_bus
import iob_snippet as py2hwsw_snippet
import iob_comb as py2hwsw_comb
import iob_fsm as py2hwsw_fsm
import iob_license as py2hwsw_license
import iob_portmap as py2hwsw_portmap
import iob_parameter as py2hwsw_parameter
import iob_instance as py2hwsw_instance
import iob_core as py2hwsw_core

# Import some modules that are already in the production-ready API
from user_api.api import iob_conf, iob_port, iob_wire, iob_snippet, iob_core


#
# Confs
#


@api_for(py2hwsw_conf.conf_from_text)
def create_conf_from_text(conf_text):
    """
    Function to create iob_conf object from short notation text.

    Attributes:
        conf_text (str): Short notation text. Object attributes are specified using the following format:
            name [-t kind] [-v value] [-m min_value] [-M max_value] [-doc]
            [-d descr]
            Example:
                DATA_W -t P -v 32 -m NA -M NA
                -d 'Data bus width'

    Returns:
        iob_conf: iob_conf object
    """
    pass


#
# Wires
#


@api_for(py2hwsw_wire.wire_from_text)
def create_wire_from_text(wire_text):
    """
    Function to create iob_wire object from short notation text.

    Attributes:
        wire_text (str): Short notation text. Object attributes are specified using the following format:
            name [-w width] [-d descr] [-v (enables isvar)]
            Example:
                en -w 1 -d 'Enable wire' -v

    Returns:
        iob_wire: iob_wire object
    """
    pass


#
# Buses
#


@api_for(py2hwsw_bus.iob_bus)
class iob_bus:
    """
    Class to represent a bus in an iob module.

    Attributes:
        name (str): Identifier name for the bus.
        descr (str): Description of the bus.
        wires (list): List of wires belonging to this bus
                        (each wire represents a hardware Verilog bus).
    """

    name: str = ""
    descr: str = "Default description"
    wires: list[iob_wire] = empty_list()

    def get_wire(self, wire_name: str) -> iob_wire:
        """
        Find a wire by name and return it.

        Args:
            wire_name (str): Name of the wire to find

        Returns:
            iob_wire: The found wire.
        """
        pass


@api_for(py2hwsw_bus.bus_from_dict)
def create_bus_from_dict(bus_dict):
    """
    Function to create iob_bus object from dictionary attributes.

    Attributes:
        bus_dict (dict): dictionary with values to initialize attributes of iob_bus object.
            This dictionary supports the following keys corresponding to the iob_bus attributes:
            - name           -> iob_bus.name
            - descr          -> iob_bus.descr
            - wires        -> iob_bus.wires

    Returns:
        iob_bus: iob_bus object
    """
    pass


@api_for(py2hwsw_bus.bus_from_text)
def create_bus_from_text(bus_text):
    """
    Function to create iob_bus object from short notation text.

    Attributes:
        bus_text (str): Short notation text. Object attributes are specified using the following format:
            name [-d descr] [-s wire_name1:width1] [-s wire_name2:width2]+
            Examples:
                dbus -d 'data bus' -s wdata:32 -s wstrb:4

    Returns:
        iob_bus: iob_bus object
    """
    pass


#
# Ports
#


@api_for(py2hwsw_port.port_text2dict)
def port_text2dict(port_text):
    """Convert port short notation text to dictionary.
    Atributes:
        port_text (str): Short notation text. See `create_port_from_text` for format.

    Returns:
        dict: Dictionary with port attributes.
    """
    pass


@api_for(py2hwsw_port.port_from_text)
def create_port_from_text(port_text):
    """
    Function to create iob_port object from short notation text.

    Attributes:
        port_text (str): Short notation text. Object attributes are specified using the following format:
            name [-i interface] [-d descr] [-s wire_name:width]+ [-doc] [-doc_clearpage]
            Example:
                control -d 'control bus' -s start_i:1 -s done_o:1 -s cmd_i:CMD_W -doc

    Returns:
        iob_port: iob_port object
    """
    pass


#
# Interfaces
#


@api_for(py2hwsw_interface.iob_interface)
class iob_interface:
    """
    Class to represent an interface for generation.

    Attributes:
        if_direction (str): Interface direction. Examples: '' (unspecified), 'manager', 'subordinate', ...
        prefix (str): Prefix for wires of the interface.
        mult (str or int): Width multiplier. Used when concatenating multiple instances of the interface.
        file_prefix (str): Prefix for generated "Verilog Snippets" of this interface.
        portmap_port_prefix (str): Prefix for "Verilog snippets" of portmaps of this interface:
    """

    if_direction: str = ""
    prefix: str = ""
    mult: str | int = 1
    file_prefix: str = ""
    portmap_port_prefix: str = ""


@api_for(py2hwsw_interface.interface_from_dict)
def create_interface_from_dict(interface_dict):
    """
    Function to create interface object from dictionary attributes.

    Attributes:
        interface_dict (dict): dictionary with values to initialize attributes of interface object.
            This dictionary supports the following keys corresponding to the interface attributes:
            - if_direction        -> interface.if_direction
            - prefix              -> interface.prefix
            - mult                -> interface.mult
            - file_prefix         -> interface.file_prefix
            - portmap_port_prefix -> interface.portmap_port_prefix

    Returns:
        interface: interface object
    """
    pass


@api_for(py2hwsw_interface.interface_text2dict)
def interface_text2dict(interface_text):
    """Convert interface short notation text to dictionary.
    Atributes:
        interface_text (str): Short notation text. See `create_interface_from_text` for format.

    Returns:
        dict: Dictionary with interface attributes.
    """
    pass


@api_for(py2hwsw_interface.interface_from_text)
def create_interface_from_text(interface_text):
    """
    Function to create interface object from short notation text.

    Attributes:
        interface_text (str): Short notation text. Object attributes are specified using the following format:
            genre [-d direction] [-p prefix] [-m mult] [-f file_prefix] [-pm portmap_port_prefix] [-w WIDTH_W:val]+ -[-P PARAM:val]+
            Examples:
                axi -d manager -p cpu_ -m 1 -f ctrl_cpu_ -pm controller_

                rom_sp -d subordinate -p boot_ -w ADDR_W:8 -w DATA_W:32

                axis -p output_ -P 'has_tlast'

    Returns:
        interface: interface object
    """
    pass


#
# Snippets
#


@api_for(py2hwsw_snippet.snippet_text2dict)
def snippet_text2dict(snippet_text):
    """Convert snippet short notation text to dictionary.
    Atributes:
        snippet_text (str): Short notation text. See `create_snippet_from_text` for format.

    Returns:
        dict: Dictionary with snippet attributes.
    """
    pass


@api_for(py2hwsw_snippet.snippet_from_text)
def create_snippet_from_text(snippet_text):
    """
    Function to create iob_snippet object from short notation text.

    Attributes:
        snippet_text (str): Short notation text. Object attributes are specified using the following format:
            [snippet_text]

    Returns:
        iob_snippet: iob_snippet object
    """
    pass


#
# Combinatorial
#


@api_for(py2hwsw_comb.iob_comb)
class iob_comb(iob_snippet):
    """
    Class to represent a Verilog combinatory circuit in an iob module.

    Attributes:
        code (str): Verilog body code of the @always block.
                    This string will be parsed to automatically identify and infer registers.
                    The `iob_reg` Py2HWSW lib module will be automatically instantiated in the core for each wire '<name>' if the following conditions are met:
                    - The bus '<name>' with single wire '<name>' exists in the core;
                    - The wire '<name>_nxt' is used in the iob_comb's code. The bus '<name>_nxt' will be automatically created if it does not exist;

                    The infered register will have the instance name '<name>_reg'. It will automatically connect it's input to the '<name>_nxt' wire, and it's output to the '<name>' wire.

                    If the following wires are found in the iob_comb's code, their buses are automatically created and the corresponding register will be updated:
                    - The '<name>_rst' wire will cause the register to have a reset port, and be connected to this bus;
                    - The '<name>_en' wire will cause the register to have an enable port, and be connected to this bus;

                    For example, if we define the 'reg_wire' bus in the core, and the iob_comb has the following code:
                    '''
                    reg_wire_nxt = reg_wire + 1;
                    '''
                    then the 'reg_wire_nxt' bus will be automatically created, and the 'reg_wire_reg' register will be instantiated.
        clk_if (str): Clock interface
        clk_prefix (str): Clock interface prefix
    """

    code: str = ""
    clk_if: str = "c_a"
    clk_prefix: str = ""


@api_for(py2hwsw_comb.comb_from_dict)
def create_comb_from_dict(comb_dict):
    """
    Function to create iob_comb object from dictionary attributes.

    Attributes:
        comb_dict (dict): dictionary with values to initialize attributes of iob_comb object.
            This dictionary supports the following keys corresponding to the iob_comb attributes:
            - code -> iob_comb.code
            - clk_if -> iob_comb.clk_if

    Returns:
        iob_comb: iob_comb object
    """
    pass


@api_for(py2hwsw_comb.comb_text2dict)
def comb_text2dict(comb_text):
    """Convert comb short notation text to dictionary.
    Atributes:
        comb_text (str): Short notation text. See `create_comb_from_text` for format.

    Returns:
        dict: Dictionary with comb attributes.
    """
    pass


@api_for(py2hwsw_comb.comb_from_text)
def create_comb_from_text(comb_text):
    """
    Function to create iob_comb object from short notation text.

    Attributes:
        comb_text (str): Short notation text. Object attributes are specified using the following format:
            [-c code] [-clk_if clk_if] [-clk_p clk_prefix]
            Example:
                -c
                {{
                    // Register data
                    data_nxt = data;
                }}
                -clk_if c_a_r
                -clk_p data_

    Returns:
        iob_comb: iob_comb object
    """
    pass


#
# Finite State Machine
#


@api_for(py2hwsw_fsm.iob_fsm)
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


@api_for(py2hwsw_fsm.fsm_from_dict)
def create_fsm_from_dict(fsm_dict):
    """
    Function to create iob_fsm object from dictionary attributes.

    Attributes:
        fsm_dict (dict): dictionary with values to initialize attributes of iob_fsm object.
            This dictionary supports the following keys corresponding to the iob_fsm attributes:
            - type -> iob_fsm.kind
            - default_assignments -> iob_fsm.default_assignments
            - state_descriptions -> iob_fsm.state_descriptions

    Returns:
        iob_fsm: iob_fsm object
    """
    pass


@api_for(py2hwsw_fsm.fsm_text2dict)
def fsm_text2dict(fsm_text):
    """Convert fsm short notation text to dictionary.
    Atributes:
        fsm_text (str): Short notation text. See `create_fsm_from_text` for format.

    Returns:
        dict: Dictionary with fsm attributes.
    """
    pass


@api_for(py2hwsw_fsm.fsm_from_text)
def create_fsm_from_text(fsm_text):
    """
    Function to create iob_fsm object from short notation text.

    Attributes:
        fsm_text (str): Short notation text. Object attributes are specified using the following format:
            [-t kind] [-d default_assignments] [-s state_descriptions]
            Example:
                -t fsm
                -d 'a_o = 10;'
                -s
                {{
                    A: a_o = 0;
                    B: a_o = 1;
                    a_o = 2;
                    if(a_o == 0)
                    begin
                        pcnt_nxt = A;
                    end
                    else
                    begin
                        pcnt_nxt = B;
                    end
                }}

    Returns:
        iob_fsm: iob_fsm object
    """
    pass


#
# License
#


@api_for(py2hwsw_license.license_text2dict)
def license_text2dict(license_text):
    """Convert license short notation text to dictionary.
    Atributes:
        license_text (str): Short notation text. See `create_license_from_text` for format.

    Returns:
        dict: Dictionary with license attributes.
    """
    pass


@api_for(py2hwsw_license.iob_license)
class iob_license:
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


@api_for(py2hwsw_license.license_from_dict)
def create_license_from_dict(license_dict):
    """
    Function to create iob_license object from dictionary attributes.

    Attributes:
        license_dict (dict): dictionary with values to initialize attributes of iob_license object.
            This dictionary supports the following keys corresponding to the iob_license attributes:
            - name -> iob_license.name
            - year -> iob_license.year
            - author -> iob_license.author

    Returns:
        iob_license: iob_license object
    """
    pass


@api_for(py2hwsw_license.license_from_text)
def create_license_from_text(license_text):
    """
    Function to create iob_license object from short notation text.

    Attributes:
        license_text (str): Short notation text. Object attributes are specified using the following format:
            [name] [-y year] [-a author]
            Example:
                MIT -y 2025 -a 'IObundle, Lda'

    Returns:
        iob_license: iob_license object
    """
    pass


#
# Port map
#


@api_for(py2hwsw_portmap.iob_portmap)
class iob_portmap:
    """
    Class that represents a portmap attribute.

    Attributes:
        e_connect (iob_bus): Identifier name of external bus that connects this port
        e_connect_bit_slices (list): List of bit slices for external connections.
        port (str): IDentifier name of port associated with portmap
    """

    e_connect: iob_bus | None = None
    e_connect_bit_slices: list[str] = empty_list()
    port: str = None


@api_for(py2hwsw_portmap.portmap_from_dict)
def create_portmap_from_dict(portmap_dict):
    """
    Function to create iob_portmap object from dictionary attributes.

    Attributes:
        portmap_dict (dict): dictionary with values to initialize attributes of iob_portmap object.
            Dictionary format:
            {
                "port1_name": "external_connection1_name",
                "port2_name": "external_connection2_name",
                "port3_name": ("external_connection3_name", ["bit_slice_1", "bit_slice_2", ...]),
            }
            Dictionary element to attribute mapping:
            port1_name -> iob_portmap.port
            external_connection1_name -> iob_portmap.e_connect
            ["bit_slice_1", "bit_slice_2", ...] -> iob_portmap.e_connect_bit_slices

            Bit slices may perform multiple functions:
            - Slice bits from a wire that is being connected.
              For example, if we have a wire (iob_addr_wire) with 32 bits, from a bus (iob_bus_bus), and we want to connect it to a port (iob_bus_port) that only accepts an address of 8 bits, we could use:
              "iob_bus_port": ("iob_bus_bus", ["iob_addr_wire[7:0]"]),
            - Connect extra wires that do not exist in the bus.
              For example, if we have a wire (independent_iob_data_wire) that is not included in the bus (iob_bus_bus), but exists in the port (iob_bus_port), we could use:
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: independent_iob_data_wire"]),
              If we didn't have the independent_iob_data_wire, we could instead connect that port's wire to a constant value or high impedance, like so:
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: 'b1"]),
              "iob_bus_port": ("iob_bus_bus", ["iob_data_wire_i: 'bz"]),

              # FIXME: For some reason, connecting extra wires with bit slices only works for connections between ports and buses that have standard interfaces! Not sure why its implemented this way: https://github.com/IObundle/py2hwsw/blob/0679fc64576380c19be96567efb5093667eeb9fd/py2hwsw/scripts/block_gen.py#L121
              # Also, I'm not sure we can connect them to constants/high impedance.
              # It seems to be possible to connect ports to constants like so: https://github.com/IObundle/py2hwsw/pull/236



    Returns:
        list[iob_portmap]: List of iob_portmap objects
    """
    pass


@api_for(py2hwsw_portmap.portmap_from_text)
def create_portmap_from_text(portmap_text):
    """
    Function to create iob_portmap object from short notation text.

    Attributes:
        portmap_text (str): Short notation text. Object attributes are specified using the following format:
            TODO

    Returns:
        iob_portmap: iob_portmap object
    """
    pass


#
# IOb Parameter
#


@api_for(py2hwsw_parameter.iob_parameter)
class iob_parameter:
    """
    Class that represents a IOb parameter attribute.

    Attributes:
        name (str): Identifier name for the IOb Parameter option.
        val (Any): Value of the IOb Parameter option.
        descr (str): Description of the IOb Parameter option.
    """

    name: str = ""
    val: object = ""
    descr: str = "Default description"


@api_for(py2hwsw_parameter.iob_parameter_from_dict)
def create_iob_parameter_from_dict(iob_parameter_dict):
    """
    Function to create iob_iob_parameter object from dictionary attributes.

    Attributes:
        iob_parameter_dict (dict): dictionary with values to initialize attributes of iob_iob_parameter object.
            This dictionary supports the following keys corresponding to the iob_parameter attributes:
            - name -> iob_parameter.name
            - val -> iob_parameter.val
            - descr -> iob_parameter.descr

    Returns:
        iob_parameter: iob_parameter object
    """
    pass


@api_for(py2hwsw_parameter.iob_parameter_text2dict)
def iob_parameter_text2dict(iob_parameter_text):
    """Convert iob_parameter short notation text to dictionary.
    Atributes:
        iob_parameter_text (str): Short notation text. See `create_iob_parameter_from_text` for format.

    Returns:
        dict: Dictionary with iob_parameter attributes.
    """
    pass


@api_for(py2hwsw_parameter.iob_parameter_from_text)
def create_iob_parameter_from_text(iob_parameter_text):
    """
    Function to create iob_parameter object from short notation text.

    Attributes:
        iob_parameter_text (str): Short notation text. Object attributes are specified using the following format:
            [name] [-v value] [-d descr]
            Example:
                my_param -v 42 -d 'My parameter description'

    Returns:
        iob_parameter: iob_parameter object
    """
    pass


@api_for(py2hwsw_parameter.iob_parameter_group)
class iob_parameter_group:
    """
    Class that represents a group of IOb Parameters.

    Attributes:
        name (str): Identifier name for the group of IOb Parameters.
        descr (str): Description of the IOb Parameter group.
        iob_parameters (list): List of IOb Parameter objects.
        doc_clearpage (bool): If enabled, the documentation table for this group will be terminated by a TeX '\clearpage' command.
    """

    name: str = ""
    descr: str = "Default description"
    iob_parameters: list = empty_list()
    doc_clearpage: bool = False


@api_for(py2hwsw_parameter.iob_parameter_group_from_dict)
def create_iob_parameter_group_from_dict(iob_parameter_group_dict):
    """
    Function to create iob_parameter_group object from dictionary attributes.

    Attributes:
        iob_parameter_group_dict (dict): dictionary with values to initialize attributes of iob_parameter_group object.
            This dictionary supports the following keys corresponding to the iob_parameter_group attributes:
            - name -> iob_parameter_group.name
            - descr -> iob_parameter_group.descr
            - iob_parameters -> iob_parameter_group.iob_parameters
            - doc_clearpage -> iob_parameter_group.doc_clearpage

    Returns:
        iob_parameter_group: iob_parameter_group object
    """
    pass


@api_for(py2hwsw_parameter.iob_parameter_group_from_text)
def create_iob_parameter_group_from_text(iob_parameter_group_text):
    """
    Function to create iob_parameter_group object from short notation text.

    Attributes:
        iob_parameter_group_text (str): Short notation text. Object attributes are specified using the following format:
            TODO

    Returns:
        iob_parameter_group: iob_parameter_group object
    """
    pass


#
# Instance
#


class iob_core:
    """Forward reference of iob_core class. Full declaration of iob_core class is available in below."""

    pass


@api_for(py2hwsw_instance.iob_instance)
class iob_instance:
    """
    Generic class to describe a module's instance.

    Attributes:
        core (str): Name of the core to instantiate.
        instance_name (str): Name of the instance. (Will be used as the instance's name in the Verilog module).
        instance_description (str): Description of the instance.
        portmap_connections (list): Instance portmap connections.
        parameters (dict): Verilog parameter values for this instance.
        instantiate (bool): Select if should intantiate the module inside another Verilog module.
    """

    # TODO: Make a new iob_instance class, independent from the iob_core class. Subblocks will instantiate iob_instance objects. Each iob_instance will store a reference to an iob_core.
    core: iob_core = None
    name: str = None
    description: str = "Default instance description"
    portmap_connections: list[str] = empty_list()
    parameters: dict[str, int | str] = empty_dict()
    instantiate: bool = True


@api_for(py2hwsw_instance.instance_from_dict)
def create_instance_from_dict(instance_dict):
    """
    Function to create iob_instance object from dictionary attributes.

    Attributes:
        instance_dict (dict): dictionary with values to initialize attributes of iob_instance object.
            This dictionary supports the following keys corresponding to the iob_instance attributes:
            - core -> iob_instance.core
            - name -> iob_instance.name
            - description -> iob_instance.description
            - portmap_connections -> iob_instance.portmap_connections = create_portmap_from_dict(portmap_connections)
            - parameters -> iob_instance.parameters
            - instantiate -> iob_instance.instantiate
            # Non-attribute instance keys
            - core (str): Optional. The name of the core to instantiate. Will search for <core>.py or <core>.json files.
                          If this key is set, all other keys will be ignored! (Except 'iob_parameters' key).
                          If <core>.py is found, it must contain a class called <core> that extends iob_core. This class will be used to instantiate the core.
                          If <core>.json is found, its contents will be read and parsed by the create_core_from_dict(<json_contents>) function.
            - iob_parameters (dict): Optional. Dictionary of iob parameters to pass to the instantiated core.
                                        This key should be used in conjunction with the 'core' key.
                                        Elements from this dictionary will be passed as **kwargs to the instantiated core's constructor.
                                        Only applicable if instantiated core has a constructor that accepts IOb parameters (excludes cores defined in JSON or purely by dictionary).


    Returns:
        iob_instance: iob_instance object
    """
    pass


@api_for(py2hwsw_instance.iob_instance)
def create_instance_from_text(instance_text):
    """
    Function to create iob_instance object from short notation text.

    Attributes:
        instance_text (str): Short notation text. Object attributes are specified using the following format:
            name [-p parameter_name:parameter_value]+ [-c port_name:wire_name]+ [--no_instance]


    Returns:
        iob_instance: iob_instance object
    """
    pass


#
# Core
#


@api_for(py2hwsw_core.core_text2dict)
def core_text2dict(core_text):
    """Convert core short notation text to dictionary.
    Atributes:
        core_text (str): Short notation text. See `create_core_from_text` for format.

    Returns:
        dict: Dictionary with core attributes.
    """
    pass


@api_for(py2hwsw_core.core_from_text)
def create_core_from_text(core_text):
    """
    Function to create iob_core object from short notation text.

    Attributes:
        core_text (str): Short notation text. Object attributes are specified using the following format:
            # Notation specific to modules
            original_name

            # Notation specific to cores
            # TODO

            # Below are parameters specific to the 'iob_csrs' module. They should probably not belong in the Py2HWSW API.
            [--no_autoaddr]
            [--rw_overlap]
            [--csr_if csr_if]
                [--csr-group csr_group_name]
                    [-r reg_name:n_bits]
                        [-t type] [-m mode] [--rst_val rst_val] [--addr addr] [--log2n_items log2n_items]

    Returns:
        iob_core: iob_core object
    """
    pass
