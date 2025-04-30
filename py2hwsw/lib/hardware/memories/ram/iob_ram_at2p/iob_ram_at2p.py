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
        ],
        "ports": [
            {
                "name": "w_clk_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_clk_i", "width": 1},
                ],
            },
            {
                "name": "w_en_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_en_i", "width": 1},
                ],
            },
            {
                "name": "w_addr_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "w_data_i",
                "descr": "Input port",
                "signals": [
                    {"name": "w_data_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "r_clk_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_clk_i", "width": 1},
                ],
            },
            {
                "name": "r_en_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_en_i", "width": 1},
                ],
            },
            {
                "name": "r_addr_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "r_data_o",
                "descr": "Output port",
                "signals": [
                    {"name": "r_data_o", "width": "DATA_W"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (HEXFILE != "none") ? 1 : 0;
            // Declare the RAM
   reg [DATA_W-1:0] ram[(2**ADDR_W)-1:0];
   reg [DATA_W-1:0] r_data_o_reg;
   assign r_data_o=r_data_o_reg;

   // Initialize the RAM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh(MEM_INIT_FILE_INT, ram, 0, (2 ** ADDR_W) - 1);
       end
   endgenerate

   //write
   always @(posedge w_clk_i) begin
       if (w_en_i) begin
           ram[w_addr_i] <= w_data_i;
       end
   end

   //read
   always @(posedge r_clk_i) begin
       if (r_en_i) begin
           r_data_o_reg <= ram[r_addr_i];
       end
   end
            """,
            },
        ],
    }

    return attributes_dict
