# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                "name": "i_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "i_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "t_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "t_i",
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
                "name": "o_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "o_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "io_io",
                "descr": "In/Output port",
                "signals": [
                    {
                        "name": "io_io",
                        "width": 1,
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "o_int",
                "descr": "o_int wire",
                "signals": [
                    {"name": "o_int", "width": 1},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   generate
      if (FPGA_TOOL == "XILINX") begin : tool_XILINX
         IOBUF IOBUF_inst (
            .I (i_i),
            .T (t_i),
            .O (o_int),
            .IO(io)
         );
      end else begin : tool_other
         reg o_var;
         assign io = t_i ? 1'bz : i_i;
         always @* o_var = #1 io;
         assign o_int = o_var;
      end
   endgenerate

   assign o_o = (n_i ^ o_int);
""",
            },
        ],
    }

    return attributes_dict
