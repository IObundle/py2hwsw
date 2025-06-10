# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import re

from dataclasses import dataclass
from iob_comb import iob_comb
from iob_base import assert_attributes


@dataclass
class iob_fsm(iob_comb):
    """Class to represent a Verilog finite state machine in an iob module"""

    fsm_type: str = "prog"
    default_assignments: str = ""
    state_descriptions: str = ""

    def __post_init__(self):
        if self.fsm_type not in ["prog", "fsm"]:
            raise ValueError("type must be either 'prog' or 'fsm'")
        if self.fsm_type == "fsm":
            self.state_reg_name = "state"
            update_statement = "state_nxt = state;"
        else:
            self.state_reg_name = "pcnt"
            update_statement = "pcnt_nxt = pcnt + 1;"
        update_statement += f"{self.default_assignments}\n"
        _states = self.state_descriptions.split("\n\n")
        self.state_names = {}
        _for_loops = {}
        self.state_reg_width = (len(_states) - 1).bit_length()
        for i, state in enumerate(_states):
            tag = re.search(r"^\s*(\w+):", state)
            tag = tag.group(1) if tag else None
            if tag:
                for_loop = re.search(r"for\s*\(([^)]+)\)", state)
                for_loop = for_loop.group(1) if for_loop else None
                if for_loop:
                    if self.fsm_type == "fsm":
                        raise ValueError("for loops are not suported in FSMs")
                    init, cond, update = for_loop.split(";")
                    _for_loops[tag] = {"init": init, "cond": cond, "update": update}
                    state = re.sub(r"for\s*\([^)]+\)", "", state)
                self.state_names[tag] = i
                _states[i] = state.replace(f"{tag}:", "")
        for tag, loop in _for_loops.items():
            if loop["init"] != "":
                _states[self.state_names[tag]] = (
                    f"\n{loop['init']};\n{_states[self.state_names[tag]]}"
                )
            if loop["update"] != "":
                _states[self.state_names[tag + "_endfor"]] = (
                    f"{_states[self.state_names[tag+'_endfor']]}\n{loop['update']};\nif ({loop['cond']}) begin\npcnt_nxt = {tag} + 1;\nend"
                )
            else:
                _states[self.state_names[tag + "_endfor"]] = (
                    f"{_states[self.state_names[tag+'_endfor']]}\nif ({loop['cond']}) begin\npcnt_nxt = {tag} + 1;\nend"
                )
        for i, state in enumerate(_states[:-1]):
            _states[i] = f"{i}: begin\n{state}\nend"
            _states[i] = re.sub(r"\n\s*\n", "\n", _states[i])
        _states[-1] = f"default: begin\n{_states[-1]}\nend"
        _states[-1] = re.sub(r"\n\s*\n", "\n", _states[-1])
        localparams = ""
        for state_name, i in self.state_names.items():
            _states[i] = _states[i].replace(f"{i}:", f"{state_name}:", 1)
            if not state_name.endswith("_endfor"):
                localparams += (
                    f"localparam {state_name} = {self.state_reg_width}'d{i};\n"
                )
        joined_states = "\n".join(_states)
        self.verilog_code = f"""
{localparams}
always @* begin
    {update_statement}
    case ({self.state_reg_name})
        {joined_states}
    endcase
end
"""


def create_fsm(core, *args, **kwargs):
    """Create a Verilog finite state machine to insert in a given core."""
    if core.comb is not None:
        raise ValueError(
            "Combinational logic is mutually exclusive with FSMs. Create separate submodules for each."
        )

    core.set_default_attribute("fsm", None)

    default_assignments = kwargs.get("default_assignments", "")
    fsm_type = kwargs.get("type", "prog")
    state_descriptions = kwargs.get("state_descriptions", "")

    assert_attributes(
        iob_fsm,
        kwargs,
        error_msg=f"Invalid {kwargs.get('name', '')} fsm attribute '[arg]'!",
    )
    fsm = iob_fsm(
        fsm_type=fsm_type,
        default_assignments=default_assignments,
        state_descriptions=state_descriptions,
    )

    # Check if the FSM wire is already created, if not create it
    if not any(wire.name == fsm.state_reg_name for wire in core.wires):
        core.create_wire(
            name=fsm.state_reg_name,
            descr="FSM state",
            signals=[{"name": fsm.state_reg_name, "width": fsm.state_reg_width}],
        )

    fsm.set_needed_reg(core)

    fsm.infer_registers(core)

    core.fsm = fsm
