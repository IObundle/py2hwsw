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
                "type": "F",
                "val": "HEXFILE",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
        ],
        "ports": [
            {
                "name": "rom_atdp_s",
                "descr": "ROM ATDP",
                "signals": {"type": "rom_atdp"},
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   localparam INIT_RAM = (MEM_INIT_FILE_INT != "none") ? 1 : 0;
            // Declare the ROM
   reg [DATA_W-1:0] rom[2**ADDR_W-1:0];

   // Initialize the ROM
   generate
       if (INIT_RAM) begin : mem_init
           initial $readmemh( MEM_INIT_FILE_INT, rom, 0, 2 ** ADDR_W - 1);
       end
   endgenerate

   always @(posedge clk_a_i)  // Port A
      if (en_a_i)
         r_data_a_o <= rom[addr_a_i];

   always @(posedge clk_b_i)  // Port B
      if (en_b_i)
         r_data_b_o <= rom[addr_b_i];
            """,
            },
        ],
    }

    return attributes_dict
