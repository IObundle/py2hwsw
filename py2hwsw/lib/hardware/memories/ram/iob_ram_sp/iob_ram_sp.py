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
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "DATA width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "14",
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
                "descr": "Address bus width",
            },
        ],
        "ports": [
            {
                "name": "clk_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clk_i", "width": 1},
                ],
            },
            {
                "name": "en_i",
                "descr": "Input port",
                "signals": [
                    {"name": "en_i", "width": 1},
                ],
            },
            {
                "name": "we_i",
                "descr": "Input port",
                "signals": [
                    {"name": "we_i", "width": 1},
                ],
            },
            {
                "name": "addr_i",
                "descr": "Input port",
                "signals": [
                    {"name": "addr_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "d_o",
                "descr": "Output port",
                "signals": [
                    {"name": "d_o", "width": "DATA_W"},
                ],
            },
            {
                "name": "d_i",
                "descr": "Input port",
                "signals": [
                    {"name": "d_i", "width": "DATA_W"},
                ],
            },
        ],
        "blocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "instantiate": False,
                "dest_dir": "hardware/simulation/src",
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            // Declare the RAM
   reg [DATA_W-1:0] ram[2**ADDR_W-1:0];
   reg [DATA_W-1:0] d_o_reg;
   assign d_o=d_o_reg;

   // Initialize the RAM
   initial if (MEM_INIT_FILE_INT != "none") $readmemh(MEM_INIT_FILE_INT, ram, 0, 2 ** ADDR_W - 1);

   // Operate the RAM
   always @(posedge clk_i)
      if (en_i)
         if (we_i) ram[addr_i] <= d_i;
         else d_o_reg<= ram[addr_i];
            """,
            },
        ],
    }

    return attributes_dict
