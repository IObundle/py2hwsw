from dataclasses import dataclass, field
from iob_snippet import iob_snippet
import re


@dataclass
class iob_fsm(iob_snippet):
    """Class to represent a Verilog finite state machine in an iob module"""
    type: str = "prog"

    def __post_init__(self):
        if self.type not in ["prog", "fsm"]:
            raise ValueError("type must be either 'prog' or 'fsm'")
        if self.type == "fsm":
            self.state_reg_name = "state"
            update_statement = "state_nxt <= state;"
        else:
            self.state_reg_name = "pc"
            update_statement = "pc_nxt = pc + 1;"
        _states = self.verilog_code.split("\n\n")
        self.state_reg_width = (len(_states) - 1).bit_length()
        self.state_names = {}
        _for_loops = {}
        for i, state in enumerate(_states):
            tag = re.search(r"^\s*(\w+):", state)
            tag = tag.group(1) if tag else None
            if tag:
                for_loop = re.search(r"for\s*\(([^)]+)\)", state)
                for_loop = for_loop.group(1) if for_loop else None
                if for_loop:
                    init, cond, update = for_loop.split(";")
                    _for_loops[tag] = {
                        "init": init,
                        "cond": cond,
                        "update": update
                    }
                    state = re.sub(r"for\s*\([^)]+\)", "", state)
                self.state_names[tag] = i
                _states[i] = state.replace(f"{tag}:", "")
        for tag, loop in _for_loops.items():
            if loop['init'] != "":
                _states[self.state_names[tag]] = f"\n{loop['init']};\n{_states[self.state_names[tag]]}"
            if loop['update'] != "":
                _states[self.state_names[tag+"_endfor"]] = f"{_states[self.state_names[tag+'_endfor']]}\n{loop['update']};\nif ({loop['cond']}) begin\npc_nxt = {tag} + 1;\nend"
            else:
                _states[self.state_names[tag+"_endfor"]] = f"{_states[self.state_names[tag+'_endfor']]}\nif ({loop['cond']}) begin\npc_nxt = {tag} + 1;\nend"
        for i, state in enumerate(_states[:-1]):
            _states[i] = f"{i}: begin\n{state}\nend"
            _states[i] = re.sub(r"\n\s*\n", "\n", _states[i])
        _states[-1] = f"default: begin\n{_states[-1]}\nend"
        _states[-1] = re.sub(r"\n\s*\n", "\n", _states[-1])
        localparams = ""
        for state_name, i in self.state_names.items():
            _states[i] = re.sub(r"^{i}:", f"{state_name}:", _states[i])
            if not state_name.endswith("_endfor"):
                localparams += f"localparam {state_name} = {i};\n"
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
    if core.combs != None:
        raise ValueError("Combinational logic is mutually exclusive with FSMs. Create separate submodules for each.")
    if core.fsms != None:
        raise ValueError("Multiple FSMs are not supported. Create separate submodules for each.")

    verilog_code = kwargs.get("verilog_code", "")

    fsm = iob_fsm(verilog_code=verilog_code)

    core.set_default_attribute("fsms", fsm)

    core.create_wire(
        name = fsm.state_reg_name,
        signals = [{"name": fsm.state_reg_name, "width": fsm.state_reg_width}]
    )

    fsm.set_needed_reg(core)

    fsm.infer_registers(core)

    core.fsms.append(fsm)
