# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "WIDTH",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "width",
            },
            {
                "name": "DEPTH",
                "type": "P",
                "val": 2,
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
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
                "name": "rst_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "d_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "d_i",
                        "width": "WIDTH",
                    },
                ],
            },
            {
                "name": "q_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "q_o",
                        "width": "WIDTH",
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
        integer            i;
   integer            j;
   reg [WIDTH-1:0]    delay_line [DEPTH-1:0];
   always @(posedge clk_i,posedge rst_i) begin
      if(rst_i) begin
         for (i=0; i < DEPTH; i=i+1) begin
            delay_line[i] <= 0;
         end
      end else begin
         delay_line[0] <= d_i;
         for (j=1; j < DEPTH; j=j+1) begin
            delay_line[j] <= delay_line[j-1];
         end
      end
   end

   assign q_o = delay_line[DEPTH-1];
            """,
            },
        ],
    }

    return attributes_dict
