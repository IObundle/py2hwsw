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
                "name": "ADDR_W",
                "type": "P",
                "val": "10",
                "min": "0",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "0",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "COL_W",
                "type": "D",
                "val": "DATA_W / 4",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "NUM_COL",
                "type": "D",
                "val": "DATA_W / COL_W",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "mem_init_file_int",
                "type": "D",
                "val": '{HEXFILE, ".hex"}',
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Clock",
                "wires": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "port_a_io",
                "descr": "Memory interface A",
                "wires": [
                    {"name": "enA_i", "width": 1},
                    {"name": "wstrbA_i", "width": "DATA_W/8"},
                    {"name": "addrA_i", "width": "ADDR_W"},
                    {"name": "dA_i", "width": "DATA_W"},
                    {"name": "dA_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "port_b_io",
                "descr": "Memory interface B",
                "wires": [
                    {"name": "enB_i", "width": 1},
                    {"name": "wstrbB_i", "width": "DATA_W/8"},
                    {"name": "addrB_i", "width": "ADDR_W"},
                    {"name": "dB_i", "width": "DATA_W"},
                    {"name": "dB_o", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none.hex") ? 1 : 0;
             // Core Memory
   reg [DATA_W-1:0] ram_block[(2**ADDR_W)-1:0];

   // Initialize the RAM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, ram_block, 0, 2 ** ADDR_W - 1);
       end
   endgenerate

   // Port-A Operation
   reg     [DATA_W-1:0] dA_o_int;
   integer              i;
   always @(posedge clk_i) begin
      if (enA_i) begin
         for (i = 0; i < NUM_COL; i = i + 1) begin
            if (wstrbA_i[i]) begin
               ram_block[addrA_i][i*COL_W+:COL_W] <= dA_i[i*COL_W+:COL_W];
            end
         end
         dA_o_int <= ram_block[addrA_i];  // Send Feedback
      end
   end

   assign dA_o = dA_o_int;

   // Port-B Operation
   reg     [DATA_W-1:0] dB_o_int;
   integer              j;
   always @(posedge clk_i) begin
      if (enB_i) begin
         for (j = 0; j < NUM_COL; j = j + 1) begin
            if (wstrbB_i[j]) begin
               ram_block[addrB_i][j*COL_W+:COL_W] <= dB_i[j*COL_W+:COL_W];
            end
         end
         dB_o_int <= ram_block[addrB_i];  // Send Feedback
      end
   end

   assign dB_o = dB_o_int;
            """,
            },
        ],
    }

    return attributes_dict
