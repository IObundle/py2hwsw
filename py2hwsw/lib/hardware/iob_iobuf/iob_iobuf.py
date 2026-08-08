# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "FPGA_TOOL",
                "descr": "Use IPs from fpga tool. Avaliable options: 'XILINX', 'other'.",
                "type": "P",
                "val": '"other"',
                "min": "NA",
                "max": "NA",
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
            .IO(io_io)
         );
      end else begin : tool_other

         assign io_io = t_i ? 1'bz : i_i;

         // Buffer gate primitive to add inertial delay. Models physical pad propagation
         // time and prevents infinite zero-delay combinational feedback loops in
         // event-driven simulators. Ignored by synthesis tools.
         buf #1 u_pad_delay (o_int, io_io);
      end
   endgenerate

   assign o_o = (n_i ^ o_int);
""",
            },
        ],
    }

    return attributes_dict
