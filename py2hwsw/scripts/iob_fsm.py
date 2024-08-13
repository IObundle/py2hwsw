from dataclasses import dataclass, field
from iob_snippet import iob_snippet
import re


@dataclass
class iob_fsm(iob_snippet):
    """Class to represent a Verilog finite state machine in an iob module"""

    def __post_init__(self):
        _states = self.verilog_code.split("\n\n")
        self.state_reg_width = (len(_states) - 1).bit_length()
        _state_names = {}
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
                    #remove for loop from state
                    state = re.sub(r"for\s*\([^)]+\)", "", state)
                _state_names[tag] = i
                _states[i] = state.replace(f"{tag}:", "")
        for state_name, i in _state_names.items():
            for j, state in enumerate(_states):
                _states[j] = state.replace(state_name, f"{self.state_reg_width}'b{i:0{self.state_reg_width}b}")
        for tag, loop in _for_loops.items():
            _states[_state_names[tag]] = f"{loop['init']};\n{_states[_state_names[tag]]}"
            _states[_state_names[tag+"_endfor"]] = f"{_states[_state_names[tag+'_endfor']]}\n{loop['update']};\nif ({loop['cond']}) begin\npc_nxt = {self.state_reg_width}'b{_state_names[tag]:0{self.state_reg_width}b};\nend"
        for i, state in enumerate(_states[:-1]):
            _states[i] = f"{i}: begin\n{state}\nend"
        _states[-1] = f"default: begin\n{_states[-1]}\nend"
        joined_states = "\n".join(_states)
        self.verilog_code = f"""
always @* begin
    pc_nxt = pc + 1;
    case (pc)
        {joined_states}
    endcase
end
"""
    
        
def create_fsm(core, *args, **kwargs):
    """Create a Verilog finite state machine to insert in a given core."""
    core.set_default_attribute("fsms", [])

    fsm_nr = len(core.fsms)

    verilog_code = kwargs.get("verilog_code", "")

    fsm = iob_fsm(verilog_code=verilog_code)

    fsm.verilog_code = fsm.verilog_code.replace("pc", f"pc{fsm_nr}")

    core.create_wire(name = f"pc{fsm_nr}",
                     signals = [
                         {
                             "name": f"pc{fsm_nr}",
                             "width": fsm.state_reg_width
                         }])

    fsm.set_needed_reg(core)

    fsm.infer_registers(core)

    core.fsms.append(fsm)
