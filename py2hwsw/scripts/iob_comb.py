# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import re

from dataclasses import dataclass
from iob_snippet import iob_snippet
from iob_base import fail_with_msg, assert_attributes
from iob_wire import find_signal_in_wires
from iob_signal import get_real_signal


@dataclass
class iob_comb(iob_snippet):
    """Class to represent a Verilog combinatory circuit in an iob module"""

    code: str = ""
    clk_if: str = "c_a"
    clk_prefix: str = ""

    def __post_init__(self):
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

        for signal_name in outputs | nxt_vars:
            if signal_name.endswith("_o"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name,
                    process_func=generate_direction_process_func("output"),
                )
                signal.isvar = True
            elif signal_name.endswith("_io"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name,
                    process_func=generate_direction_process_func("inout"),
                )
                signal.isvar = True
            elif signal_name.endswith("_nxt"):
                signal = find_signal_in_wires(core.wires + core.ports, signal_name[:-4])
                if not signal:
                    fail_with_msg(
                        f"Could not find signal '{signal_name[:-4]}' in wires of '{core.name}' for register implied by '{signal_name}'."
                    )
                signal.isreg = True
                signal.reg_signals.append("_nxt")
            elif signal_name.endswith("_rst"):
                signal = find_signal_in_wires(core.wires + core.ports, signal_name[:-4])
                if not signal:
                    fail_with_msg(
                        f"Could not find signal '{signal_name[:-4]}' in wires of '{core.name}' for register implied by '{signal_name}'."
                    )
                signal.reg_signals.append("_rst")
            elif signal_name.endswith("_en"):
                signal = find_signal_in_wires(core.wires + core.ports, signal_name[:-3])
                if not signal:
                    fail_with_msg(
                        f"Could not find signal '{signal_name[:-3]}' in wires of '{core.name}' for register implied by '{signal_name}'."
                    )
                signal.reg_signals.append("_en")
            else:
                signal = find_signal_in_wires(core.wires + core.ports, signal_name)
                signal.isvar = True

            if signal is None:
                fail_with_msg(f"Output '{signal_name}' not found in wires/ports lists!")

        for signal_name in nxt_vars - outputs:
            insert_point = self.verilog_code.find("\t\t\t")
            if insert_point != -1:
                self.verilog_code = (
                    self.verilog_code[:insert_point]
                    + f"\t\t\t{signal_name} = {signal_name[:-4]};\n"
                    + self.verilog_code[insert_point:]
                ) 

    def infer_registers(self, core):
        """Infer registers from the combinatory code and create the necessary subblocks"""

        for wire in core.wires + core.ports:
            for signal_ref in wire.signals:
                signal = get_real_signal(signal_ref)
                if signal.isreg:
                    clk_if_name = "clk_en_rst_s"
                    # Find the clock interface if it exists
                    # and overwrite the default one
                    for port in core.ports:
                        if port.interface:
                            if port.interface.type == "iob_clk" and port.interface.prefix == self.clk_prefix:
                                clk_if_name = port.name
                                if port.interface.params:
                                    port_params = port.interface.params
                                else:
                                    port_params = "c_a"

                    # Connect the register
                    connect = {
                        "clk_en_rst_s": clk_if_name,
                        "data_i": f"{signal.name}_nxt",
                        "data_o": f"{signal.name}",
                    }

                    # Find the register signals (if any)
                    if any(reg_signal == "_nxt" for reg_signal in signal.reg_signals):
                        # If the _nxt wire does not already exists, create it
                        if not any(
                            wire.name == f"{signal.name}_nxt" for wire in core.wires
                        ):
                            core.create_wire(
                                name=f"{signal.name}_nxt",
                                signals=[
                                    {
                                        "name": f"{signal.name}_nxt",
                                        "descr": f"{signal.name} next value",
                                        "width": signal.width,
                                        "isvar": True,
                                    }
                                ],
                            )
                        # Create the register wire
                        core.create_wire(
                            name=signal.name,
                            signals=[{"name": signal.name}],
                        )

                    _reg_signals = []
                    bit_slices = []

                    if self.clk_if:
                        port_params = self.clk_if

                    # Find, create and connect the enable and reset signals (if they exist)
                    if any(reg_signal == "_en" for reg_signal in signal.reg_signals):
                        _reg_signals.append(
                            {
                                "name": f"{signal.name}_en",
                                "descr": f"{signal.name} enable",
                                "width": 1,
                                "isvar": True,
                            }
                        )
                        bit_slices.append(f"en_i:{signal.name}_en")
                        port_params = port_params + "_e"

                    if any(reg_signal == "_rst" for reg_signal in signal.reg_signals):
                        _reg_signals.append(
                            {
                                "name": f"{signal.name}_rst",
                                "descr": f"{signal.name} reset",
                                "width": 1,
                                "isvar": True,
                            }
                        )
                        bit_slices.append(f"rst_i:{signal.name}_rst")
                        port_params = port_params + "_r"

                    if any(x in port_params for x in ["_r", "_e"]):
                        if not any(
                            wire.name == f"{signal.name}_reg_signals"
                            for wire in core.wires
                        ):
                            core.create_wire(
                                name=f"{signal.name}_reg_signals", signals=_reg_signals
                            )

                    # Create the clock interface in the core, if it does not exist
                    if not any(port.name == "clk_en_rst_s" for port in core.ports):
                        core.create_port_from_dict(
                            name="clk_en_rst_s",
                            signals={"type": "iob_clk", "params": self.clk_if},
                            descr="Clock interface signals",
                        )

                    # if bit_slices is not empty, add it to the connect dictionary
                    if bit_slices:
                        connect["clk_en_rst_s"] = (clk_if_name, bit_slices)

                    # Create the subblock for the register
                    # if it does not already exist
                    if not any(
                        block.instance_name == f"{signal.name}_reg"
                        for block in core.subblocks
                    ):
                        core.create_subblock(
                            core_name="iob_reg",
                            instance_name=f"{signal.name}_reg",
                            parameters={"DATA_W": signal.width, "RST_VAL": 0},
                            connect=connect,
                            port_params={"clk_en_rst_s": port_params},
                            instance_description=f"{signal.name} register",
                        )


def generate_direction_process_func(direction):
    """Generates a process function that returns a signal if it matches the direction"""

    def filter_signal(signal):
        signal = get_real_signal(signal)
        if signal.direction == direction:
            return signal
        # Return empty object if not correct signal direction
        return None

    return filter_signal


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
