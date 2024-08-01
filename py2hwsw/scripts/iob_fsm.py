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
            tag = re.search(r"\b(\w+):", state)
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
        self.verilog_code = f"""
always @* begin
    pc_nxt = pc + 1;
    case (state)
        {'\n'.join(self.states)}
    endcase
end
"""
        
def create_fsm(core, *args, **kwargs):
    """Create a Verilog finite state machine to insert in a given core."""
    core.set_default_attribute("fsms", [])

    fsm_nr = len(core.fsms)

    verilog_code = verilog_code.replace("pc", f"pc{fsm_nr}")

    fsm = iob_fsm(verilog_code=verilog_code)

    reg_name = f"fms{fsm_nr}_state_reg"

    core.create_wire(name=f"pc{fsm_nr}",
                     signals={
                         "name": f"pc{fsm_nr}",
                         "width": fsm.state_reg_width,
                         "isreg": True})

    core.create_wire(name=f"pc{fsm_nr}_nxt",
                     signals={
                         "name": f"pc{fsm_nr}_nxt",
                         "width": fsm.state_reg_width,
                         "isreg": True})

    if not any(port["name"] == "clk_en_rst" for port in core.ports):
        core.create_port(name="clk_en_rst", 
                         interface={
                             "type": "clk_en_rst",
                             "subtype": "slave"},
                         descr="clock enable and reset")

    core.create_instance(core_name="iob_reg",
                         instance_name=reg_name,
                         parameters={
                            "DATA_W": fsm.state_reg_width,
                            "RST_VAL": 1},
                         connect={
                            "clk_en_rst": "clk_en_rst",
                            "data_i": f"pc{fsm_nr}_nxt",
                            "data_o": f"pc{fsm_nr}"})
                        
    fsm.set_needed_reg(core)

    core.fsms.append(fsm)
