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
                "val": "6",
                "min": "0",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "8",
                "min": "0",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "MEM_NO_READ_ON_WRITE",
                "type": "P",
                "val": "1",
                "min": "0",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "MEM_INIT_FILE_INT",
                "type": "D",
                "val": "HEXFILE",
                "min": "0",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "clock",
                "wires": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "port_a_io",
                "descr": "Port A",
                "wires": [
                    {"name": "enA_i", "width": 1},
                    {"name": "weA_i", "width": 1},
                    {"name": "addrA_i", "width": "ADDR_W"},
                    {"name": "dA_i", "width": "DATA_W"},
                    {"name": "dA_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "port_b_io",
                "descr": "Port B",
                "wires": [
                    {"name": "enB_i", "width": 1},
                    {"name": "weB_i", "width": 1},
                    {"name": "addrB_i", "width": "ADDR_W"},
                    {"name": "dB_i", "width": "DATA_W"},
                    {"name": "dB_o", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    localparam INIT_RAM = (MEM_INIT_FILE_INT != "none") ? 1 : 0;
    reg [DATA_W-1:0] dA_o_reg;
    reg [DATA_W-1:0] dB_o_reg;
    assign dA_o=dA_o_reg;
    assign dB_o=dB_o_reg;
            // Declare the RAM
   reg [DATA_W-1:0] ram[2**ADDR_W-1:0];

   // Initialize the RAM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, ram, 0, 2 ** ADDR_W - 1);
       end
   endgenerate

   generate
      if (MEM_NO_READ_ON_WRITE) begin : with_MEM_NO_READ_ON_WRITE
         always @(posedge clk_i) begin  // Port A
            if (enA_i)
               if (weA_i) ram[addrA_i] <= dA_i;
               else dA_o_reg <= ram[addrA_i];
         end
         always @(posedge clk_i) begin  // Port B
            if (enB_i)
               if (weB_i) ram[addrB_i] <= dB_i;
               else dB_o_reg <= ram[addrB_i];
         end
      end else begin : not_MEM_NO_READ_ON_WRITE
         always @(posedge clk_i) begin  // Port A
            if (enA_i) if (weA_i) ram[addrA_i] <= dA_i;
            dA_o_reg <= ram[addrA_i];
         end
         always @(posedge clk_i) begin  // Port B
            if (enB_i) if (weB_i) ram[addrB_i] <= dB_i;
            dB_o_reg <= ram[addrB_i];
         end
      end
   endgenerate    
            """,
            },
        ],
    }

    return attributes_dict
