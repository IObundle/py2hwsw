# SPDX-FileCopyrightText: 2024 IObundle
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

    def __post_init__(self):
        """Wrap verilog code with the always block"""
        self.verilog_code = (
            f"""\talways @ (*)\n\t\tbegin\n"""
            + """\t\t\t"""
            + self.verilog_code
            + """\n\t\tend"""
        )

    def set_needed_reg(self, core):
        blocking_regex = re.compile(r"^\s*(\w+)\s*(?:\[[^\]]*\])?\s*=", re.MULTILINE)
        non_blocking_regex = re.compile(
            r"^\s*(\w+)\s*(?:\[[^\]]*\])?\s*<=", re.MULTILINE
        )

        outputs = set()

        for match in blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for match in non_blocking_regex.findall(self.verilog_code):
            outputs.add(match)

        for signal_name in outputs:
            if signal_name.endswith("_o"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name,
                    process_func=generate_direction_process_func("output"),
                )
            elif signal_name.endswith("_io"):
                signal = find_signal_in_wires(
                    core.ports,
                    signal_name,
                    process_func=generate_direction_process_func("inout"),
                )
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

            if signal is not None:
                signal.isvar = True
            else:
                fail_with_msg(f"Output '{signal_name}' not found in wires/ports lists!")

    def infer_registers(self, core):
        for wire in core.wires + core.ports:
            for signal_ref in wire.signals:
                signal = get_real_signal(signal_ref)
                if signal.isreg:
                    reg_type = "iob_reg"
                    connect = {
                        "clk_en_rst_s": "clk_en_rst_s",
                        "data_i": f"{signal.name}_nxt",
                        "data_o": f"{signal.name}",
                    }
                    if any(reg_signal == "_nxt" for reg_signal in signal.reg_signals):
                        if not any(
                            wire.name == f"{signal.name}_nxt" for wire in core.wires
                        ):
                            core.create_wire(
                                name=f"{signal.name}_nxt",
                                signals=[
                                    {
                                        "name": f"{signal.name}_nxt",
                                        "width": signal.width,
                                        "isvar": True,
                                    }
                                ],
                            )
                    _reg_signals = []
                    connect_key = None
                    if any(reg_signal == "_en" for reg_signal in signal.reg_signals):
                        _reg_signals.append(
                            {"name": f"{signal.name}_en", "width": 1, "isvar": True}
                        )
                        reg_type = "iob_reg_e"
                        connect_key = "en_i"
                    if any(reg_signal == "_rst" for reg_signal in signal.reg_signals):
                        _reg_signals.append(
                            {"name": f"{signal.name}_rst", "width": 1, "isvar": True}
                        )
                        if reg_type.endswith("_e"):
                            reg_type = "iob_reg_re"
                            connect_key = "en_rst"
                        else:
                            reg_type = "iob_reg_r"
                            connect_key = "rst"

                    if reg_type != "iob_reg":
                        if not any(
                            wire.name == f"{signal.name}_reg_signals"
                            for wire in core.wires
                        ):
                            core.create_wire(
                                name=f"{signal.name}_reg_signals", signals=_reg_signals
                            )
                            connect[connect_key] = f"{signal.name}_reg_signals"

                    if not any(port.name == "clk_en_rst_s" for port in core.ports):
                        core.create_port(
                            name="clk_en_rst_s",
                            signals={"type": "clk_en_rst"},
                            descr="Clock enable and reset signal",
                        )

                    if not any(
                        block.instance_name == f"{signal.name}_reg"
                        for group in core.blocks
                        for block in group.blocks
                    ):
                        core.create_block_group(
                            core_name=reg_type,
                            instance_name=f"{signal.name}_reg",
                            parameters={"DATA_W": signal.width, "RST_VAL": 0},
                            connect=connect,
                            instance_description=f"Infered register for {signal.name}",
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
    verilog_code = kwargs.get("verilog_code", None)
    assert_attributes(
        iob_comb,
        kwargs,
        error_msg=f"Invalid {kwargs.get('name', '')} comb attribute '[arg]'!",
    )
    comb = iob_comb(verilog_code=verilog_code)
    comb.set_needed_reg(core)
    comb.infer_registers(core)
    core.comb = comb
