# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
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
                "val": "0",
                "min": "NA",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "0",
                "min": "NA",
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
                "name": "clkA_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clkA_i", "width": 1},
                ],
            },
            {
                "name": "dA_i",
                "descr": "Input port",
                "signals": [
                    {"name": "dA_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "addrA_i",
                "descr": "Input port",
                "signals": [
                    {"name": "addrA_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "enA_i",
                "descr": "Input port",
                "signals": [
                    {"name": "enA_i", "width": 1},
                ],
            },
            {
                "name": "weA_i",
                "descr": "Input port",
                "signals": [
                    {"name": "weA_i", "width": 1},
                ],
            },
            {
                "name": "dA_o",
                "descr": "Output port",
                "signals": [
                    {"name": "dA_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "clkB_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clkB_i", "width": 1},
                ],
            },
            {
                "name": "dB_i",
                "descr": "Input port",
                "signals": [
                    {"name": "dB_i", "width": "DATA_W"},
                ],
            },
            {
                "name": "addrB_i",
                "descr": "Input port",
                "signals": [
                    {"name": "addrB_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "enB_i",
                "descr": "Input port",
                "signals": [
                    {"name": "enB_i", "width": 1},
                ],
            },
            {
                "name": "weB_i",
                "descr": "Input port",
                "signals": [
                    {"name": "weB_i", "width": 1},
                ],
            },
            {
                "name": "dB_o",
                "descr": "Output port",
                "signals": [
                    {"name": "dB_o", "width": "DATA_W"},
                ],
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
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

   //read port
   always @(posedge clkA_i) begin  // Port A
      if (enA_i)
`ifdef IOB_MEM_NO_READ_ON_WRITE
         if (weA_i) ram[addrA_i] <= dA_i;
         else dA_o_reg <= ram[addrA_i];
`else
         if (weA_i) ram[addrA_i] <= dA_i;
         dA_o_reg <= ram[addrA_i];
`endif
   end

   //write port
   always @(posedge clkB_i) begin  // Port B
      if (enB_i)
`ifdef IOB_MEM_NO_READ_ON_WRITE
         if (weB_i) ram[addrB_i] <= dB_i;
         else dB_o_reg <= ram[addrB_i];
`else
         if (weB_i) ram[addrB_i] <= dB_i;
         dB_o_reg <= ram[addrB_i];
`endif
   end
            """,
            },
        ],
    }

    return attributes_dict
