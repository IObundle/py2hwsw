from dataclasses import dataclass, field
from iob_snippet import iob_snippet
import re


@dataclass
class iob_fsm(iob_snippet):
    """Class to represent a Verilog finite state machine in an iob module"""

    def __post_init__(self):
        self.states = self.verilog_code.split("\n\n")
        self.state_reg_width = (len(self.states) - 1).bit_length()
        self.state_names = {}
        for i, state in enumerate(self.states):
            tag = re.search(r"^\s*(\w+):", state)
            tag = tag.group(1) if tag else None
            if tag:
                self.state_names[tag] = i
                self.states[i] = state.replace(f"{tag}:", "")
        for state_name, i in self.state_names.items():
            for j, state in enumerate(self.states):
                self.states[j] = state.replace(state_name, f"{self.state_reg_width}'b{i:0{self.state_reg_width}b}")
        for i, state in enumerate(self.states[:-1]):
            self.states[i] = f"{i}: begin\n{state}\nend"
        self.states[-1] = f"default: begin\n{self.states[-1]}\nend"
        joined_states = "\n".join(self.states)
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
