# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "W",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "MODE",
                "type": "P",
                "val": '"LOW"',
                "min": "NA",
                "max": "NA",
                "descr": "'LOW' = Prioritize smaller index",
            },
        ],
        "ports": [
            {
                "name": "unencoded_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "unencoded_i",
                        "width": "W",
                    },
                ],
            },
            {
                "name": "encoded_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "encoded_o",
                        "width": "$clog2(W+1)",
                        "isvar": True,
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "unencoded_int",
                "descr": "",
                "signals": [
                    {"name": "unencoded_int", "width": "W+1"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   // MSB = 1 if unencoded_i = 0
   assign unencoded_int = {(~(|unencoded_i)), unencoded_i};

   integer pos;
   generate
      if (MODE == "LOW") begin : gen_low_prio
         always @* begin
            encoded_o = 1'b0;  //placeholder default value
            for (pos = W; pos != -1; pos = pos - 1) begin
               if (unencoded_int[pos]) begin
                  encoded_o = pos[$clog2(W)-1:0];
               end
            end
         end
      end else begin : gen_highest_prio  //MODE == "HIGH"
         always @* begin
            encoded_o = 1'b0;  //placeholder default value
            for (pos = {W{1'd0}}; pos < (W+1); pos = pos + 1) begin
               if (unencoded_int[pos]) begin
                  encoded_o = pos[$clog2(W)-1:0];
               end
            end
         end
      end
   endgenerate    
         """,
            },
        ],
    }

    return attributes_dict
