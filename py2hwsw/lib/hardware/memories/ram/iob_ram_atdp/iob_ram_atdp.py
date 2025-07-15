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
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "MEM_INIT_FILE_INT",
                "type": "D",
                "val": "HEXFILE",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "1",
                "descr": "No simultaneous read/write",
            },
        ],
        "ports": [
            {
                "name": "clkA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "clkA_i", "width": 1},
                ],
            },
            {
                "name": "dA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "dA_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "addrA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "addrA_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "enA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "enA_i", "width": 1},
                ],
            },
            {
                "name": "weA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "weA_i", "width": 1},
                ],
            },
            {
                "name": "dA_o",
                "descr": "Output port",
                "wires": [
                    {"name": "dA_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "clkB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "clkB_i", "width": 1},
                ],
            },
            {
                "name": "dB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "dB_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "addrB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "addrB_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "enB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "enB_i", "width": 1},
                ],
            },
            {
                "name": "weB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "weB_i", "width": 1},
                ],
            },
            {
                "name": "dB_o",
                "descr": "Output port",
                "wires": [
                    {"name": "dB_o", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none") ? 1 : 0;
   // Declare the RAM
   reg [DATA_W-1:0] ram[2**ADDR_W-1:0];
   reg [DATA_W-1:0] dA_o_reg;
   reg [DATA_W-1:0] dB_o_reg;
   assign dA_o=dA_o_reg;
   assign dB_o=dB_o_reg;

   // Initialize the RAM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, ram, 0, 2 ** ADDR_W - 1);
       end
   endgenerate

   generate
      if (MEM_NO_READ_ON_WRITE) begin : with_MEM_NO_READ_ON_WRITE
         //read port
         always @(posedge clkA_i) begin  // Port A
            if (enA_i)
               if (weA_i) ram[addrA_i] <= dA_i;
               else dA_o_reg <= ram[addrA_i];
         end
         //write port
         always @(posedge clkB_i) begin  // Port B
            if (enB_i)
               if (weB_i) ram[addrB_i] <= dB_i;
               else dB_o_reg <= ram[addrB_i];
         end
      end else begin : not_MEM_NO_READ_ON_WRITE
         //read port
         always @(posedge clkA_i) begin  // Port A
            if (enA_i)
               if (weA_i) ram[addrA_i] <= dA_i;
               dA_o_reg <= ram[addrA_i];
         end
         //write port
         always @(posedge clkB_i) begin  // Port B
            if (enB_i)
               if (weB_i) ram[addrB_i] <= dB_i;
               dB_o_reg <= ram[addrB_i];
         end
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
