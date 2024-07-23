from dataclasses import dataclass, field
from iob_base import find_obj_in_list, convert_dict2obj_list, fail_with_msg
from iob_signal import iob_signal, iob_signal_reference
from iob_snippet import iob_snippet
from iob_wire import *

@dataclass
class iob_comb(iob_snippet):
    """Class to represent a Verilog combinatory circuit in an iob module"""

    def __post_init__(self):
        """Wrap verilog code with the always block"""
        super().__post_init__()
        self.verilog_code = f'''\talways @ (*)\n\t\tbegin\n''' + '''\t\t\t''' +  self.verilog_code + '''\n\t\tend'''

def create_comb(core, *args, **kwargs):
    """Create a Verilog combinatory circuit to insert in a given core."""
    # Ensure 'combs' list exists
    core.set_default_attribute("combs", [])
    verilog_code = kwargs.get('verilog_code',None)
    outputs = kwargs.get('outputs',None)
    for signal_name in outputs:
        signal = find_signal_in_wires(core.wires + core.ports, signal_name)
        if signal != None:
            signal.isreg = True
        else:
            fail_with_msg(
                f"output '{signal_name}' not found in wires/ports lists!"
            )
    comb = iob_comb(outputs=outputs,verilog_code=verilog_code)
    core.combs.append(comb)
                                                
if __name__ == '__main__':
    circ = iob_comb(outputs=[],verilog_code='a = b & c;')
    print(circ.outputs)
    print(circ.verilog_code)
