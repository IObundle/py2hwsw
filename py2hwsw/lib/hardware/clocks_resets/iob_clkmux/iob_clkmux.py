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
                "descr": "Use IPs from fpga tool. Avaliable options: 'XILINX', 'INTEL', 'other'.",
            },
        ],
        "ports": [
            {
                "name": "clk0_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "clk0_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "clk1_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "clk1_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "clk_sel_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "clk_sel_i",
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
        "snippets": [
            {
                "verilog_code": """
   generate
      if (FPGA_TOOL == "XILINX") begin : tool_XILINX
         BUFGMUX #(
            .CLK_SEL_TYPE("ASYNC")
         ) BUFGMUX_inst (
            .I0(clk0_i),
            .I1(clk1_i),
            .S (clk_sel_i),
            .O (clk_o)
         );
      end else if (FPGA_TOOL == "INTEL") begin : tool_INTEL
         altclkctrl altclkctrl_inst (
            .inclk     ({clk0_i, clk1_i}),
            .clkselect (clk_sel_i),
            .outclk    (clk_o)
         );
      end else begin : tool_other
         reg    clk_v;
         always @* clk_v = #1 clk_sel_i ? clk1_i : clk0_i;
         assign clk_o = clk_v;
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
