# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """Setup function for the iob_ram_at2p module.
    :param py_params_dict: Dictionary with parameters for the module.
    :return: Dictionary with attributes for the module.
    """
    # Validate the input parameters
    if not isinstance(py_params_dict, dict):
        raise TypeError("py_params_dict must be a dictionary")
    init_mem = py_params_dict.get("init_mem", False)

    # change parameter to boolean
    if isinstance(init_mem, str):
        init_mem = init_mem.lower() == "true"

    # Create the configuration list based on the init_mem parameter
    if init_mem:
        confs = [
            {
                "name": "HEXFILE",
                "type": "P",
                "val": '"none"',
                "min": "NA",
                "max": "NA",
                "descr": "Name of file to load into RAM",
            },
        ]
    else:
        confs = []

    confs += [
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
            "val": "1",
            "min": "1",
            "max": "NA",
            "descr": "Address bus width",
        },
    ]

    code_snippet = """
    // Declare the RAM
   reg [DATA_W-1:0] ram[(2**ADDR_W)-1:0];
   reg [DATA_W-1:0] r_data_int;
   assign r_data_o = r_data_int;
        """

    # Add initialization code if init_mem is True
    if init_mem:
        code_snippet +="""
   // Initialize the RAM
   initial $readmemh(HEXFILE, ram, 0, (2 ** ADDR_W) - 1);
            """

    code_snippet += """
   //write
   always @(posedge w_clk_i) begin
       if (w_en_i) begin
           ram[w_addr_i] <= w_data_i;
       end
   end

   //read
   always @(posedge r_clk_i) begin
       if (r_en_i) begin
           r_data_int <= ram[r_addr_i];
       end
   end
            """
    
    if init_mem:
        name = "iob_ram_at2p_w_init"
    else:
        name = "iob_ram_at2p"

    attributes_dict = {
        "generate_hw": True,
        "name": name,
        "confs": confs,
        "ports": [
            {
                "name": "ram_at2p_s",
                "descr": "RAM interface",
                "signals": {
                    "type": "ram_at2p",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": code_snippet,
            },
        ],
    }

    return attributes_dict
