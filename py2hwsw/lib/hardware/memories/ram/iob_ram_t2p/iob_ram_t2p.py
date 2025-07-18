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
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "1",
                "min": "1",
                "max": "NA",
                "descr": "Data bus width",
            },
        ],
        "ports": [
            {
                "name": "ram_t2p_s",
                "descr": "RAM interface",
                "wires": {
                    "type": "ram_t2p",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """

   // Declare the RAM
   reg [DATA_W-1:0] mem    [(2**ADDR_W)-1:0];

   reg [DATA_W-1:0] r_data;
   // Initialize the RAM
   generate
       if (HEXFILE != "none") begin : mem_init
           initial $readmemh(HEXFILE, mem, 0, (2 ** ADDR_W) - 1);
       end
   endgenerate

   //read port
   always @(posedge clk_i) begin
       if (r_en_i) begin
           r_data <= mem[r_addr_i];
       end
   end

   //write port
   always @(posedge clk_i) begin
       if (w_en_i) begin
           mem[w_addr_i] <= w_data_i;
       end
   end

   assign r_data_o = r_data;
            """,
            },
        ],
    }

    return attributes_dict
