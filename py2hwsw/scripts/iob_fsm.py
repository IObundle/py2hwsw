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
        
        print(self.verilog_code)
def create_fsm(core, *args, **kwargs):
    """Create a Verilog finite state machine to insert in a given core."""
    # Ensure 'fsms' list exists
    core.set_default_attribute("fsms", [])
    #TODO: go through arguments and build verilog code and add clk rst en if necessary

    fsm = iob_fsm(verilog_code=verilog_code)
    fsm.set_needed_reg(core)
    core.fsms.append(fsm)

if __name__ == "__main__":
    iob = iob_fsm(verilog_code="""
    state1:
        if (input) begin
            state <= 1;
        end

        if (input) begin
            state <= 2;
        end

        if (input) begin
            state <= 3;
        end

        if (input) begin
            pc_nxt <= state1;
        end
""")
