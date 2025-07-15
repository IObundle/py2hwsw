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
                "val": "10",
                "min": "NA",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "COL_W",
                "type": "D",
                "val": "8",
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
                "name": "enA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "enA_i", "width": 1},
                ],
            },
            {
                "name": "wstrbA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "wstrbA_i", "width": "DATA_W/8"},
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
                "name": "dA_i",
                "descr": "Input port",
                "wires": [
                    {"name": "dA_i", "width": "DATA_W"},
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
                "name": "enB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "enB_i", "width": 1},
                ],
            },
            {
                "name": "wstrbB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "wstrbB_i", "width": "DATA_W/8"},
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
                "name": "dB_i",
                "descr": "Input port",
                "wires": [
                    {"name": "dB_i", "width": "DATA_W"},
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
        "subblocks": [
            {
                "core_name": "iob_ram_atdp",
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

            iob_ram_atdp #(
               .HEXFILE(mem_init_file_int),
               .ADDR_W (ADDR_W),
               .DATA_W (COL_W)
            ) ram (
               .clkA_i (clkA_i),
               .enA_i  (enA_i),
               .addrA_i(addrA_i),
               .dA_i   (dA_i[i*COL_W+:COL_W]),
               .wstrbA_i  (wstrbA_i[i]),
               .dA_o   (dA_o[i*COL_W+:COL_W]),

               .clkB_i (clkB_i),
               .enB_i  (enB_i),
               .addrB_i(addrB_i),
               .dB_i   (dB_i[i*COL_W+:COL_W]),
               .wstrbB_i  (wstrbB_i[i]),
               .dB_o   (dB_o[i*COL_W+:COL_W])
            );
         end
      end else begin : not_MEM_NO_READ_ON_WRITE
         // this allow ISE 14.7 to work; do not remove
         localparam INIT_RAM = (mem_init_file_int != "none.hex") ? 1 : 0;
         localparam mem_init_file_int = {HEXFILE, ".hex"};

         // Core Memory
         reg [DATA_W-1:0] ram_block[(2**ADDR_W)-1:0];

         // Initialize the RAM
         if (INIT_RAM) begin : mem_init
            initial
               if (mem_init_file_int != "none.hex")
                  $readmemh(mem_init_file_int, ram_block, 0, 2 ** ADDR_W - 1);
         end

         // Port-A Operation
         reg     [DATA_W-1:0] dA_o_int;
         integer              i;
         always @(posedge clkA_i) begin
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
         always @(posedge clkB_i) begin
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
      end
   endgenerate
""",
            },
        ],
    }

    return attributes_dict
