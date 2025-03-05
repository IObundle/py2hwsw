# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "FPGA_TOOL",
                "type": "P",
                "val": '"XILINX"',
                "min": "NA",
                "max": "NA",
                "descr": "Use IPs from fpga tool. Avaliable options: 'XILINX', 'other'.",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "clk_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "n_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "n_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "clk_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "clk_o",
                        "width": 1,
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "clk_int",
                "descr": "clk_int wire",
                "signals": [
                    {"name": "clk_int", "width": 1},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   assign clk_int = n_i ? ~clk_i : clk_i;
   generate
      if (FPGA_TOOL == "XILINX") begin : tool_XILINX
         BUFG BUFG_inst (
            .I(clk_int),
            .O(clk_o)
         );
      end else begin : tool_other
         assign clk_o = clk_int;
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
