# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "HEXFILE",
                "type": "P",
                "val": '"none"',
                "min": "NA",
                "max": "NA",
                "descr": "Name of file to load into RAM",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "14",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "MEM_INIT_FILE_INT",
                "type": "D",
                "val": "HEXFILE",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "wires": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "en_i",
                "descr": "Input port",
                "wires": [
                    {"name": "en_i", "width": 1},
                ],
            },
            {
                "name": "we_i",
                "descr": "Input port",
                "wires": [
                    {"name": "we_i", "width": 1},
                ],
            },
            {
                "name": "addr_i",
                "descr": "Input port",
                "wires": [
                    {"name": "addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "d_o",
                "descr": "Output port",
                "wires": [
                    {"name": "d_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "d_i",
                "descr": "Input port",
                "wires": [
                    {"name": "d_i", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none") ? 1 : 0;
            // Declare the RAM
   reg [DATA_W-1:0] ram[2**ADDR_W-1:0];
   reg [DATA_W-1:0] d_o_reg;
   assign d_o=d_o_reg;

   // Initialize the RAM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, ram, 0, 2 ** ADDR_W - 1);
       end
   endgenerate

   // Operate the RAM
   always @(posedge clk_i)
      if (en_i)
         if (we_i) ram[addr_i] <= d_i;
         else d_o_reg<= ram[addr_i];
            """,
            },
        ],
    }

    return attributes_dict
