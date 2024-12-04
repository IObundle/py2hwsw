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
                "name": "clk_a_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clk_a_i", "width": 1},
                ],
            },
            {
                "name": "addr_a_i",
                "descr": "Input port",
                "signals": [
                    {"name": "addr_a_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "r_en_a_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_en_a_i", "width": 1},
                ],
            },
            {
                "name": "clk_b_i",
                "descr": "Input port",
                "signals": [
                    {"name": "clk_b_i", "width": 1},
                ],
            },
            {
                "name": "addr_b_i",
                "descr": "Input port",
                "signals": [
                    {"name": "addr_b_i", "width": "ADDR_W"},
                ],
            },
            {
                "name": "r_en_b_i",
                "descr": "Input port",
                "signals": [
                    {"name": "r_en_b_i", "width": 1},
                ],
            },
            {
                "name": "r_data_a_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "r_data_a_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "r_data_b_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "r_data_b_o",
                        "width": "DATA_W",
                        "isvar": True,
                    },
                ],
            },
        ],
        "subblocks": [
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
            // Declare the ROM
   reg [DATA_W-1:0] rom[2**ADDR_W-1:0];

   // Initialize the ROM
   initial if ( MEM_INIT_FILE_INT != "none") $readmemh( MEM_INIT_FILE_INT, rom, 0, 2 ** ADDR_W - 1);

   always @(posedge clk_a_i)  // Port A
      if (r_en_a_i)
         r_data_a_o <= rom[addr_a_i];

   always @(posedge clk_b_i)  // Port B
      if (r_en_b_i)
         r_data_b_o <= rom[addr_b_i];
            """,
            },
        ],
    }

    return attributes_dict
