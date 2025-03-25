# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    params = {
        # Type of interface for CSR bus
        "csr_if": "iob",
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data bus width",
                "type": "P",
                "val": "32",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_en_rst_s",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "iob_clk",
            },
        },
        {
            "name": "uart_s",
            "descr": "Testbench uart csrs interface",
            "signals": {
                "type": "iob",
                "ADDR_W": 3,
            },
        },
    ]
    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "rs232_loopback",
            "descr": "Uart loopback wires",
            "signals": {
                "type": "rs232",
            },
        },
        {
            "name": "uart_cbus",
            "descr": "Testbench uart csrs bus",
            "signals": {
                "type": params["csr_if"],
                "prefix": "internal_",
                "ADDR_W": 3 - 2,
            },
        },
    ]
    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            "core_name": "iob_uart",
            "instance_name": "uart_inst",
            "instance_description": "UUT UART instance",
            "csr_if": params["csr_if"],
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "iob_csrs_cbus_s": "uart_cbus",
                "rs232_m": "rs232_loopback",
            },
        },
    ]
    if params["csr_if"] == "wb":
        # "Wishbone" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2wishbone",
                "instance_name": "iob_iob2wishbone_coverter",
                "instance_description": "Convert IOb port into Wishbone interface for uart CSRs bus",
                "parameters": {
                    "APB_ADDR_W": "ADDR_W",
                    "APB_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "apb_m": "uart_cbus",
                    "iob_s": (
                        "uart_s",
                        [
                            "iob_addr_i[3-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "apb":
        # "APB" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2apb",
                "instance_name": "iob_iob2apb_coverter",
                "instance_description": "Convert IOb port into APB interface for uart CSRs bus",
                "parameters": {
                    "APB_ADDR_W": "ADDR_W",
                    "APB_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "apb_m": "uart_cbus",
                    "iob_s": (
                        "uart_s",
                        [
                            "iob_addr_i[3-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "axil":
        # "AXI_Lite" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axil",
                "instance_name": "iob_iob2axil_coverter",
                "instance_description": "Convert IOb port into AXI_Lite interface for uart CSRs bus",
                "parameters": {
                    "AXIL_ADDR_W": "ADDR_W",
                    "AXIL_DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axilms": "uart_cbus",
                    "iob_s": (
                        "uart_s",
                        [
                            "iob_addr_i[3-1:2]",
                        ],
                    ),
                },
            }
        )
    elif params["csr_if"] == "axi":
        # "AXI" CSR_IF
        attributes_dict["subblocks"].append(
            {
                "core_name": "iob_iob2axi",
                "instance_name": "iob_iob2axi_coverter",
                "instance_description": "Convert IOb port into AXI interface for uart CSRs bus",
                "parameters": {
                    "ADDR_WIDTH": "ADDR_W",
                    "DATA_WIDTH": "DATA_W",
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "axi_m": (
                        "uart_cbus",
                        [
                            "axi_awlock_i[0]",
                            "axi_arlock_i[0]",
                        ],
                    ),
                    "iob_s": (
                        "uart_s",
                        [
                            "iob_addr_i[3-1:2]",
                        ],
                    ),
                },
            }
        )
    #
    # Snippets
    #
    attributes_dict["snippets"] = []
    snippet_code = """
   assign rs232_rxd = rs232_txd;
   assign rs232_cts = rs232_rts;
"""
    if params["csr_if"] == "iob":
        snippet_code += """
   // Directly connect cbus IOb port to internal IOb wires
   assign internal_iob_valid = iob_valid_i;
   assign internal_iob_addr = iob_addr_i[3-1:2]; // Ignore 2 LSBs
   assign internal_iob_wdata = iob_wdata_i;
   assign internal_iob_wstrb = iob_wstrb_i;
   assign internal_iob_rready = iob_rready_i;
   assign iob_rvalid_o = internal_iob_rvalid;
   assign iob_rdata_o = internal_iob_rdata;
   assign iob_ready_o = internal_iob_ready;
"""
    attributes_dict["snippets"] += [
        {"verilog_code": snippet_code},
    ]

    return attributes_dict
