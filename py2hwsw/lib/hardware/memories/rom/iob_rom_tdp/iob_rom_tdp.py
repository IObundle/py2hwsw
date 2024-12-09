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
                "name": "rom_tdp_s",
                "descr": "ROM TDP",
                "signals": {"type": "rom_tdp"},
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
            // Declare the ROM
   reg [DATA_W-1:0] rom[(2**ADDR_W)-1:0];

   // Initialize the ROM
   initial begin
       if (MEM_INIT_FILE_INT != "none") begin
           $readmemh(MEM_INIT_FILE_INT, rom, 0, (2 ** ADDR_W) - 1);
       end
   end

   always @(posedge clk_i) begin  // Port A
      if (r_en_a_i) begin
         r_data_a_o <= rom[r_addr_a_i];
      end
   end

   always @(posedge clk_i) begin  // Port B
      if (r_en_b_i) begin
         r_data_b_o <= rom[r_addr_b_i];
      end
   end
            """,
            },
        ],
    }

    return attributes_dict
