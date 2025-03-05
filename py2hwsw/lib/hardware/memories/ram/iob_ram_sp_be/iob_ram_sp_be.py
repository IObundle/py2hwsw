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
                "type": "F",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "",
            },
            {
                "name": "NUM_COL",
                "type": "F",
                "val": "DATA_W / COL_W",
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
                "name": "clk_i",
                "descr": "Clock",
                "signals": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "mem_if_io",
                "descr": "Memory interface",
                "signals": [
                    {"name": "en_i", "width": 1},
                    {"name": "we_i", "width": "DATA_W/8"},
                    {"name": "addr_i", "width": "ADDR_W"},
                    {"name": "d_i", "width": "DATA_W"},
                    {"name": "d_o", "width": "DATA_W"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_ram_sp",
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   genvar i;
   generate
      if (MEM_NO_READ_ON_WRITE) begin : with_MEM_NO_READ_ON_WRITE
         localparam file_suffix = {"7", "6", "5", "4", "3", "2", "1", "0"};
         for (i = 0; i < NUM_COL; i = i + 1) begin : ram_col
            localparam mem_init_file_int = (HEXFILE != "none") ?
                {HEXFILE, "_", file_suffix[8*(i+1)-1-:8], ".hex"} : "none";

            iob_ram_sp #(
               .HEXFILE(mem_init_file_int),
               .ADDR_W (ADDR_W),
               .DATA_W (COL_W)
            ) ram (
               .clk_i(clk_i),

               .en_i  (en_i),
               .addr_i(addr_i),
               .d_i   (d_i[i*COL_W+:COL_W]),
               .we_i  (we_i[i]),
               .d_o   (d_o[i*COL_W+:COL_W])
            );
         end
      end else begin : not_MEM_NO_READ_ON_WRITE
         // this allows ISE 14.7 to work; do not remove
         localparam INIT_RAM = (HEXFILE != "none") ? 1 : 0;
         localparam mem_init_file_int = {HEXFILE, ".hex"};

         // Core Memory
         reg [DATA_W-1:0] ram_block[(2**ADDR_W)-1:0];

         // Initialize the RAM
         if (INIT_RAM) begin : mem_init
             initial
                $readmemh(mem_init_file_int, ram_block, 0, 2 ** ADDR_W - 1);
         end

         reg     [DATA_W-1:0] d_o_int;
         integer              i;
         always @(posedge clk_i) begin
            if (en_i) begin
               for (i = 0; i < NUM_COL; i = i + 1) begin
                  if (we_i[i]) begin
                     ram_block[addr_i][i*COL_W+:COL_W] <= d_i[i*COL_W+:COL_W];
                  end
               end
               d_o_int <= ram_block[addr_i];  // Send Feedback
            end
         end

         assign d_o = d_o_int;
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
