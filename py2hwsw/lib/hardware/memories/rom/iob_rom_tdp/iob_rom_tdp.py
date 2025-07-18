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
                "val": "32",
                "min": "1",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "11",
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
        ],
        "ports": [
            {
                "name": "rom_tdp_s",
                "descr": "ROM TDP",
                "wires": {
                    "type": "rom_tdp",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none") ? 1 : 0;
            // Declare the ROM
   reg [DATA_W-1:0] rom[(2**ADDR_W)-1:0];
   reg [DATA_W-1:0] r_data_a_int;
   reg [DATA_W-1:0] r_data_b_int;

   // Initialize the ROM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, rom, 0, (2 ** ADDR_W) - 1);
       end
   endgenerate

   always @(posedge clk_i) begin  // Port A
      if (r_en_a_i) begin
         r_data_a_int <= rom[r_addr_a_i];
      end
   end

   always @(posedge clk_i) begin  // Port B
      if (r_en_b_i) begin
         r_data_b_int <= rom[r_addr_b_i];
      end
   end

   assign r_data_a_o = r_data_a_int;
   assign r_data_b_o = r_data_b_int;
            """,
            },
        ],
    }

    return attributes_dict
