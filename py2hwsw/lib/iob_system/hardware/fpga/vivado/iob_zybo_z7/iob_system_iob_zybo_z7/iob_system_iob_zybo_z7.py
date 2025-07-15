# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "name": params["name"] + "_iob_zybo_z7",
        "generate_hw": False,
        #
        # Configuration
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "D",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "D",
                "val": "8",
                "min": "1",
                "max": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "D",
                "val": "30" if params["use_extmem"] else "20",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "D",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "BAUD",
                "descr": "UART baud rate",
                "type": "D",
                "val": "115200",
            },
            {
                "name": "FREQ",
                "descr": "Clock frequency",
                "type": "D",
                "val": "50000000",
            },
            {
                "name": "XILINX",
                "descr": "xilinx flag",
                "type": "D",
                "val": "1",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = [
        # inout [14:0]DDR_addr;
        #  inout [2:0]DDR_ba;
        #  inout DDR_cas_n;
        #  inout DDR_ck_n;
        #  inout DDR_ck_p;
        #  inout DDR_cke;
        #  inout DDR_cs_n;
        #  inout [3:0]DDR_dm;
        #  inout [31:0]DDR_dq;
        #  inout [3:0]DDR_dqs_n;
        #  inout [3:0]DDR_dqs_p;
        #  inout DDR_odt;
        #  inout DDR_ras_n;
        #  inout DDR_reset_n;
        #  inout DDR_we_n;
        #  inout FIXED_IO_ddr_vrn;
        #  inout FIXED_IO_ddr_vrp;
        #  inout [53:0]FIXED_IO_mio;
        #  inout FIXED_IO_ps_clk;
        #  inout FIXED_IO_ps_porb;
        #  inout FIXED_IO_ps_srstb;
        {
            "name": "DDR_addr_io",
            "descr": "DDR address bus",
            "wires": [
                {"name": "DDR_addr_io", "width": "15"},
            ],
        },
        {
            "name": "DDR_ba_io",
            "descr": "DDR bank address bus",
            "wires": [
                {"name": "DDR_ba_io", "width": "3"},
            ],
        },
        {
            "name": "DDR_cas_n_io",
            "descr": "DDR CAS wire",
            "wires": [
                {"name": "DDR_cas_n_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_ck_n_io",
            "descr": "DDR clock negative wire",
            "wires": [
                {"name": "DDR_ck_n_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_ck_p_io",
            "descr": "DDR clock positive wire",
            "wires": [
                {"name": "DDR_ck_p_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_cke_io",
            "descr": "DDR clock enable wire",
            "wires": [
                {"name": "DDR_cke_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_cs_n_io",
            "descr": "DDR chip select wire",
            "wires": [
                {"name": "DDR_cs_n_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_dm_io",
            "descr": "DDR data mask bus",
            "wires": [
                {
                    "name": "DDR_dm_io",  # Data mask
                    # Width is 4 for DDR3, 8 for DDR4
                    # This should match the memory type used
                    # in the design.
                    # For Zybo Z7, it is typically 4.
                    # Adjust as necessary based on your design.
                    # Here we assume DDR3 with 4 data masks
                    "width": 4,
                },
            ],
        },
        {
            # DDR data bus
            # Width is typically 32 bits for DDR3/4
            # Adjust based on your design requirements.
            # For Zybo Z7, it is usually 32 bits.
            # If using DDR4, consider using a wider bus if needed.
            # Here we assume a standard 32-bit data bus.
            # If you need more bits, adjust accordingly.
            # For example, if using DDR4 with
            # 64-bit data bus, change width to 64.
            "name": "DDR_dq_io",
            "descr": "DDR data bus",
            "wires": [
                {"name": "DDR_dq_io", "width": "32"},
            ],
        },
        {
            "name": "DDR_dqs_n_io",
            "descr": "DDR data strobe negative wire",
            "wires": [
                {"name": "DDR_dqs_n_io", "width": "4"},
            ],
        },
        {
            "name": "DDR_dqs_p_io",
            "descr": "DDR data strobe positive wire",
            "wires": [
                {"name": "DDR_dqs_p_io", "width": "4"},
            ],
        },
        {
            "name": "DDR_odt_io",
            "descr": "DDR on-die termination wire",
            "wires": [
                {"name": "DDR_odt_io", "width": "1"},
            ],
        },
        {
            "name": "DDR_ras_n_io",
            "descr": "DDR RAS wire",
            "wires": [
                {"name": "DDR_ras_n_io", "width": "1"},
            ],
        },
        {
            # DDR reset wire
            # This is typically active low.
            # Ensure it matches your design requirements.
            # For Zybo Z7, it is usually active low.
            # If using DDR4, ensure the reset logic is compatible.
            # Here we assume a standard active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            # Here we assume an active low reset.
            #
            "name": "DDR_reset_n_io",
            "descr": "DDR reset wire",
            "wires": [
                {"name": "DDR_reset_n_io", "width": "1"},
            ],
        },
        {
            "name": "FIXED_IO_ddr_vrn_io",
            "descr": "DDR voltage reference negative",
            "wires": [
                {"name": "FIXED_IO_ddr_vrn_io", "width": "1"},
            ],
        },
        {
            "name": "FIXED_IO_ddr_vrp_io",
            "descr": "DDR voltage reference positive",
            "wires": [
                {"name": "FIXED_IO_ddr_vrp_io", "width": "1"},
            ],
        },
        {
            # MIO pins for various functions
            # Adjust the width based on your design requirements.
            # For Zybo Z7, it is typically 54 bits.
            # If using fewer MIO pins, adjust the width accordingly.
            # Here we assume a standard 54-bit MIO bus.
            # If you need more or fewer bits, adjust accordingly.
            # For example, if using 40 MIO pins, change width to 40.
            # Here we assume a standard 54-bit MIO bus.
            # If you need more or fewer bits, adjust accordingly.
            # For example, if using 40 MIO pins, change width to 40.
            # Here we assume a standard 54-bit MIO bus.
            # If you need more or fewer bits, adjust accordingly.
            # For example, if using 40 MIO pins, change width to 40.
            "name": "FIXED_IO_mio_io",
            "descr": "MIO pins for various functions",
            "wires": [
                {"name": "FIXED_IO_mio_io", "width": "54"},
            ],
        },
        {
            # PS clock input
            # This is typically used for system clock input.
            # Ensure it matches your design requirements.
            # For Zybo Z7, it is usually connected to a clock source.
            # If using a different clock frequency, adjust accordingly.
            # Here we assume a standard clock input wire.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high clock input, change to '1'.
            # Here we assume an active high clock input wire.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active low clock input, change to '0'.
            # Here we assume an active high clock input
            "name": "FIXED_IO_ps_clk_io",
            "descr": "PS clock input",
            "wires": [
                {"name": "FIXED_IO_ps_clk_io", "width": "1"},
            ],
        },
        {
            # PS PORB (Power-On Reset) wire
            # This is typically used for system reset.
            # Ensure it matches your design requirements.
            # For Zybo Z7, it is usually connected to a reset source.
            # If using a different reset logic, adjust accordingly.
            # Here we assume an active low reset wire.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            "name": "FIXED_IO_ps_porb_io",
            "descr": "PS PORB wire",
            "wires": [
                {"name": "FIXED_IO_ps_porb_io", "width": "1"},
            ],
        },
        {
            # PS SRSTB (System Reset) wire
            # This is typically used for system reset.
            # Ensure it matches your design requirements.
            # For Zybo Z7, it is usually connected to a reset source.
            # If using a different reset logic, adjust accordingly.
            # Here we assume an active low reset wire.
            # If you need a different logic level, adjust accordingly.
            # For example, if using active high reset, change to '1'.
            "name": "FIXED_IO_ps_srstb_io",
            "descr": "PS SRSTB wire",
            "wires": [
                {"name": "FIXED_IO_ps_srstb_io", "width": "1"},
            ],
        },
    ]

    #
    # Wires
    #
    attributes_dict["buses"] = [
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "wires": {
                "type": "iob_clk",
            },
        },
        {
            "name": "arst_n",
            "descr": "Negated reset",
            "wires": [
                {"name": "arst_n", "width": "1"},
            ],
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "wires": {
                "type": "rs232",
            },
        },
    ]

    #
    # Blocks
    #
    attributes_dict["subblocks"] = [
        {
            # Memory Wrapper
            "core_name": py_params_dict["issuer"]["original_name"],
            "instance_name": py_params_dict["issuer"]["original_name"],
            "instance_description": "IOb-SoC instance",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst",
                "rs232_m": "rs232_int",
            },
            "dest_dir": "hardware/common_src",
        },
    ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
            // General connections
            assign cke = 1'b1;
            assign arst = ~arst_n;

            assign txd_o = rs232_txd;
            assign rs232_rxd = rxd_i;

 processing_system7_0 processing_system7_0
       (
        .PS_CLK(FIXED_IO_ps_clk_io),
        .PS_PORB(FIXED_IO_ps_porb_io),
        .PS_SRSTB(FIXED_IO_ps_srstb_io,

        .FCLK_CLK0(clk),
        .FCLK_RESET0_N(arst_n),

        .DDR_Addr(DDR_addr),
        .DDR_BankAddr(DDR_ba),
        .DDR_CAS_n(DDR_cas_n),
        .DDR_CKE(DDR_cke),
        .DDR_CS_n(DDR_cs_n),
        .DDR_Clk(DDR_ck_p),
        .DDR_Clk_n(DDR_ck_n),
        .DDR_DM(DDR_dm),
        .DDR_DQ(DDR_dq),
        .DDR_DQS(DDR_dqs_p),
        .DDR_DQS_n(DDR_dqs_n),
        .DDR_DRSTB(DDR_reset_n),
        .DDR_ODT(DDR_odt),
        .DDR_RAS_n(DDR_ras_n),
        .DDR_VRN(FIXED_IO_ddr_vrn),
        .DDR_VRP(FIXED_IO_ddr_vrp),
        .DDR_WEB(DDR_we_n)
  );


            """,
        },
    ]

    return attributes_dict
