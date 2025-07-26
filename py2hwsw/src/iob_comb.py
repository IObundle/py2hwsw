# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import re

from dataclasses import dataclass
from iob_snippet import iob_snippet
from iob_wire import iob_wire
from iob_bus import iob_bus, iobClkInterface
from iob_base import fail_with_msg, assert_attributes, parse_short_notation_text

find_wire_in_buses = iob_bus.find_wire_in_buses
get_real_wire = iob_wire.get_real_wire


@dataclass
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

    def validate_attributes(self):
        pass

    # FIXME: When should this be called? Maybe at the same as 'validate_attributes'? (wrap_verilog_code is the old post_init)
    def warp_verilog_code(self):
        """Wrap verilog code with the always block"""
        self.verilog_code = (
            f"""\talways @ (*)\n\t\tbegin\n"""
            + """\t\t\t"""
            + self.code
            + """\n\t\tend"""
        )
        if "clk_i:" in self.clk_if:
            self.clk_prefix, self.clk_if = self.clk_if.split("clk_i:")

    def set_needed_reg(self, core):
        blocking_regex = re.compile(r"^\s*(\w+)\s*(?:\[[^\]]*\])?\s*=", re.MULTILINE)
        non_blocking_regex = re.compile(
            r"^\s*(\w+)\s*(?:\[[^\]]*\])?\s*<=", re.MULTILINE
        )
        nxt_regex = re.compile(r"[a-zA-Z0-9_$]+_nxt", re.MULTILINE)

        outputs = set()
        nxt_vars = set()

        for match in blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in non_blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in nxt_regex.findall(self.verilog_code):
            nxt_vars.add(match)

        for wire_name in outputs | nxt_vars:
            if wire_name.endswith("_o"):
                wire = find_wire_in_buses(
                    core.ports,
                    wire_name,
                    process_func=__class__.generate_direction_process_func("output"),
                )
                wire.isvar = True
            elif wire_name.endswith("_io"):
                wire = find_wire_in_buses(
                    core.ports,
                    wire_name,
                    process_func=__class__.generate_direction_process_func("inout"),
                )
                wire.isvar = True
            elif wire_name.endswith("_nxt"):
                wire = find_wire_in_buses(core.buses + core.ports, wire_name[:-4])
                if not wire:
                    fail_with_msg(
                        f"Could not find wire '{wire_name[:-4]}' in buses of '{core.name}' for register implied by '{wire_name}'."
                    )
                wire.isreg = True
                wire.reg_wires.append("_nxt")
            elif wire_name.endswith("_rst"):
                wire = find_wire_in_buses(core.buses + core.ports, wire_name[:-4])
                if not wire:
                    fail_with_msg(
                        f"Could not find wire '{wire_name[:-4]}' in buses of '{core.name}' for register implied by '{wire_name}'."
                    )
                wire.reg_wires.append("_rst")
            elif wire_name.endswith("_en"):
                wire = find_wire_in_buses(core.buses + core.ports, wire_name[:-3])
                if not wire:
                    fail_with_msg(
                        f"Could not find wire '{wire_name[:-3]}' in buses of '{core.name}' for register implied by '{wire_name}'."
                    )
                wire.reg_wires.append("_en")
            else:
                wire = find_wire_in_buses(core.buses + core.ports, wire_name)
                wire.isvar = True

            if wire is None:
                fail_with_msg(f"Output '{wire_name}' not found in buses/ports lists!")

        for wire_name in nxt_vars - outputs:
            insert_point = self.verilog_code.find("\t\t\t")
            if insert_point != -1:
                self.verilog_code = (
                    self.verilog_code[:insert_point]
                    + f"\t\t\t{wire_name} = {wire_name[:-4]};\n"
                    + self.verilog_code[insert_point:]
                )

    def infer_registers(self, core):
        """Infer registers from the combinatory code and create the necessary subblocks"""

        for bus in core.buses + core.ports:
            for wire_ref in bus.wires:
                wire = get_real_wire(wire_ref)
                if wire.isreg:
                    clk_if_name = "clk_en_rst_s"
                    # Find the clock interface if it exists
                    # and overwrite the default one
                    for port in core.ports:
                        if port.interface:
                            if (
                                isinstance(port.interface, iobClkInterface)
                                and port.interface.prefix == self.clk_prefix
                            ):
                                clk_if_name = port.name
                                # If it does not cke or arst, set them
                                port.interface.has_cke = True
                                port.interface.has_arst = True

                                port_params = "c_a"
                                # Add the remaining parameters
                                if port.interface.has_rst:
                                    port_params += "_r"
                                if port.interface.has_en:
                                    port_params += "_e"

                    # Connect the register
                    connect = {
                        "clk_en_rst_s": clk_if_name,
                        "data_i": f"{wire.name}_nxt",
                        "data_o": f"{wire.name}",
                    }

                    # Find the register wires (if any)
                    if any(reg_wire == "_nxt" for reg_wire in wire.reg_wires):
                        # If the _nxt bus does not already exists, create it
                        if not any(
                            bus.name == f"{wire.name}_nxt" for bus in core.buses
                        ):
                            core.create_bus(
                                name=f"{wire.name}_nxt",
                                wires=[
                                    {
                                        "name": f"{wire.name}_nxt",
                                        "descr": f"{wire.name} next value",
                                        "width": wire.width,
                                        "isvar": True,
                                    }
                                ],
                            )
                        # Create the register bus
                        core.create_bus(
                            name=wire.name,
                            wires=[{"name": wire.name}],
                        )

                    _reg_wires = []
                    bit_slices = []

                    if self.clk_if:
                        port_params = self.clk_if

                    # Find, create and connect the enable and reset wires (if they exist)
                    if any(reg_wire == "_en" for reg_wire in wire.reg_wires):
                        _reg_wires.append(
                            {
                                "name": f"{wire.name}_en",
                                "descr": f"{wire.name} enable",
                                "width": 1,
                                "isvar": True,
                            }
                        )
                        bit_slices.append(f"en_i:{wire.name}_en")
                        port_params = port_params + "_e"

                    if any(reg_wire == "_rst" for reg_wire in wire.reg_wires):
                        _reg_wires.append(
                            {
                                "name": f"{wire.name}_rst",
                                "descr": f"{wire.name} reset",
                                "width": 1,
                                "isvar": True,
                            }
                        )
                        bit_slices.append(f"rst_i:{wire.name}_rst")
                        port_params = port_params + "_r"

                    if any(x in port_params for x in ["_r", "_e"]):
                        if not any(
                            bus.name == f"{wire.name}_reg_wires" for bus in core.buses
                        ):
                            core.create_bus(
                                name=f"{wire.name}_reg_wires", wires=_reg_wires
                            )

                    # Create the clock interface in the core, if it does not exist
                    if not any(port.name == "clk_en_rst_s" for port in core.ports):
                        core.create_port_from_dict(
                            name="clk_en_rst_s",
                            wires={"type": "iob_clk", "params": self.clk_if},
                            descr="Clock interface wires",
                        )

                    # if bit_slices is not empty, add it to the connect dictionary
                    if bit_slices:
                        connect["clk_en_rst_s"] = (clk_if_name, bit_slices)

                    # Create the subblock for the register
                    # if it does not already exist
                    if not any(
                        block.instance_name == f"{wire.name}_reg"
                        for block in core.subblocks
                    ):
                        core.create_subblock(
                            core_name="iob_reg",
                            instance_name=f"{wire.name}_reg",
                            parameters={"DATA_W": wire.width, "RST_VAL": 0},
                            connect=connect,
                            port_params={"clk_en_rst_s": port_params},
                            instance_description=f"{wire.name} register",
                        )

    @staticmethod
    def generate_direction_process_func(direction):
        """Generates a process function that returns a wire if it matches the direction"""

        def filter_wire(wire):
            wire = get_real_wire(wire)
            if wire.direction == direction:
                return wire
            # Return empty object if not correct wire direction
            return None

        return filter_wire

    @staticmethod
    def create_comb(core, *args, **kwargs):
        """Create a Verilog combinatory circuit to insert in a given core."""
        if core.fsm is not None:
            raise ValueError(
                "Comb circuits and FSMs are mutually exclusive. Use separate submodules."
            )
        core.set_default_attribute("comb", None)
        assert_attributes(
            iob_comb,
            kwargs,
            error_msg=f"Invalid {kwargs.get('name', '')} comb attribute '[arg]'!",
        )
        # Get attributes from kwargs or use default from iob_comb
        code = kwargs.get("code", "")
        clk_if = kwargs.get("clk_if", "c_a")
        comb = iob_comb(code=code, clk_if=clk_if)
        comb.set_needed_reg(core)
        comb.infer_registers(core)
        core.comb = comb

    #
    # Other Py2HWSW interface methods
    #

    @staticmethod
    def create_from_dict(comb_dict):
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
        return iob_comb(**comb_dict)

    @staticmethod
    def comb_text2dict(comb_text):
        """Convert comb short notation text to dictionary.
        Atributes:
            comb_text (str): Short notation text. See `create_from_text` for format.

        Returns:
            dict: Dictionary with comb attributes.
        """
        comb_flags = [
            ["-c", {"dest": "code"}],
            ["-clk_if", {"dest": "clk_if"}],
            ["-clk_p", {"dest": "clk_prefix"}],
        ]
        # Parse comb text into a dictionary
        return parse_short_notation_text(comb_text, comb_flags)

    @staticmethod
    def create_from_text(comb_text):
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
        return __class__.create_from_dict(__class__.comb_text2dict(comb_text))
