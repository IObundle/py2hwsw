# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                "verilog_code": f"""
        `ifdef XILINX
   IOBUF IOBUF_inst (
      .I (i_i),
      .T (t_i),
      .O (o_int),
      .IO(io)
   );
`else
   reg o_var;
   assign io = t_i ? 1'bz : i_i;
   always @* o_var = #1 io;
   assign o_int = o_var;
`endif

   assign o_o = (n_i ^ o_int);
            """,
            },
        ],
    }

    return attributes_dict
