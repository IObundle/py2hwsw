def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_fsm3",
        "name": "iob_fsm3",
        "version": "0.1",
        "ports": [
            {
                "name": "a_o",
                "descr": "Output port",
                "signals": [
                    {"name": "a_o", "width": "8"},
                ],
            },
        ],
        "fsm": {
            "verilog_code": """
A: a_o = 0;

B: a_o = 1;

a_o = 2;

if(a_o == 0)
begin
    pc_nxt = A;
end
else
begin
    pc_nxt = B;
end
"""
            }
    }

    return attributes_dict
