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
                "val": "0",
                "min": "0",
                "max": "NA",
                "descr": "Address bus width",
            },
            {
                "name": "DATA_W",
                "type": "P",
                "val": "0",
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
        ],
        "ports": [
            {
                "name": "ram_t2p_be_s",
                "descr": "RAM interface",
                "signals": {
                    "type": "ram_t2p_be",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_ram_t2p",
                "instantiate": False,
            },
        ],
        "snippets": [
            {
                "verilog_code": """

    genvar i;
    generate
        localparam file_suffix = {"7", "6", "5", "4", "3", "2", "1", "0"};
        for (i = 0; i < NUM_COL; i = i + 1) begin : ram_col
            localparam mem_init_file_int = (HEXFILE != "none") ?
                {HEXFILE, "_", file_suffix[8*(i+1)-1-:8], ".hex"} : "none";

            iob_ram_t2p #(
                .HEXFILE(mem_init_file_int),
                .ADDR_W (ADDR_W),
                .DATA_W (COL_W)
            ) ram (
                .clk_i(clk_i),
                .w_en_i  (w_strb_i[i]),
                .w_addr_i(w_addr_i),
                .w_data_i(w_data_i[i*COL_W+:COL_W]),
                .r_en_i  (r_en_i),
                .r_addr_i(r_addr_i),
                .r_data_o(r_data_o[i*COL_W+:COL_W])
            );
        end
    endgenerate
""",
            },
        ],
    }

    return attributes_dict
