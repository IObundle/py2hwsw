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
                        "width": "$clog2(W)",
                        "isvar": True,
                    },
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
         integer pos;
   generate
      if (MODE == "LOW") begin : gen_low_prio
         always @* begin
            encoded_o = {$clog2(W) {1'd0}};  //In case input is 0
            for (pos = W - 1; pos != -1; pos = pos - 1) begin
               if (unencoded_i[pos]) begin
                  encoded_o = pos[$clog2(W)-1:0];
               end
            end
         end
      end else begin : gen_highest_prio  //MODE == "HIGH"
         always @* begin
            encoded_o = {$clog2(W){1'd0}};  //In case input is 0
            for (pos = 0; pos < W; pos = pos + 1) begin
               if (unencoded_i[pos]) begin
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
