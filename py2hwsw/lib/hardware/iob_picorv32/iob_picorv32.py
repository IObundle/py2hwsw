# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # Each generated cpu verilog module must have a unique name due to different python parameters (can't have two differnet verilog modules with same name).
    assert "name" in py_params_dict, print(
        "Error: Missing name for generated picorv32 module."
    )

    params = {
        "reset_addr": 0x00000000,
        "uncached_start_addr": 0x00000000,
        "uncached_size": 2**32,
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    attributes_dict = {
        "name": py_params_dict["name"],
        "version": "0.1",
        "generate_hw": True,
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 32,
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": 0,
                "min": 0,
                "max": 4,
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {"type": "clk_en_rst"},
            },
            {
                "name": "rst_i",
                "descr": "Synchronous reset",
                "signals": [
                    {
                        "name": "rst_i",
                        "descr": "CPU synchronous reset",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "i_bus_m",
                "descr": "iob-picorv32 instruction bus",
                "signals": {
                    "type": "axi",
                    "prefix": "ibus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "d_bus_m",
                "descr": "iob-picorv32 data bus",
                "signals": {
                    "type": "axi",
                    "prefix": "dbus_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
            {
                "name": "clint_cbus_s",
                "descr": "CLINT CSRs bus",
                "signals": {
                    "type": "iob",
                    "prefix": "clint_",
                    "ADDR_W": 16 - 2,
                },
            },
            {
                "name": "plic_cbus_s",
                "descr": "PLIC CSRs bus",
                "signals": {
                    "type": "iob",
                    "prefix": "plic_",
                    "ADDR_W": 22 - 2,
                },
            },
            {
                "name": "plic_interrupts_i",
                "descr": "PLIC interrupts",
                "signals": [
                    {
                        "name": "plic_interrupts_i",
                        "descr": "PLIC interrupts",
                        "width": "32",
                    },
                ],
            },
        ],
    }

    #
    # CPU wrapper body
    #
    attributes_dict |= {
        "wires": [
            {
                "name": "cpu_reset",
                "descr": "cpu reset signal",
                "signals": [
                    {"name": "cpu_reset", "width": "1"},
                ],
            },
            {
                "name": "i_bus",
                "signals": {
                    "type": "iob",
                    "file_prefix": "iob_picorv32_ibus_",
                    "prefix": "ibus_",
                    "prefix": "ibus_",
                    "DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                },
                "descr": "iob-picorv32 instruction bus",
            },
            {
                "name": "d_bus",
                "signals": {
                    "type": "iob",
                    "file_prefix": "iob_picorv32_dbus_",
                    "prefix": "dbus_",
                    "prefix": "dbus_",
                    "DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                },
                "descr": "iob-picorv32 data bus",
            },
        ],
        "subblocks": [
            # TODO: Add iob_cache and a way to bypass it for uncached memory region
            {
                "core_name": "iob_iob2axi",
                "instance_name": "ibus_iob2axi",
                "instance_description": "Convert IOb instruction bus to AXI",
                "parameters": {
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst": "clk_en_rst_s",
                    "control_io": "",
                    "iob_s": "i_bus",
                    "axi_m": "i_bus_m",
                },
            },
            {
                "core_name": "iob_iob2axi",
                "instance_name": "dbus_iob2axi",
                "instance_description": "Convert IOb data bus to AXI",
                "parameters": {
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst": "clk_en_rst_s",
                    "control_io": "",
                    "iob_s": "d_bus",
                    "axi_m": "d_bus_m",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
   //picorv32 native interface wires
   wire                cpu_instr;
   wire                cpu_valid;
   wire [  ADDR_W-1:0] cpu_addr;
   wire [DATA_W/8-1:0] cpu_wstrb;
   wire [  DATA_W-1:0] cpu_wdata;
   wire [  DATA_W-1:0] cpu_rdata;
   wire                cpu_ready;

   //split cpu bus into ibus and dbus
   wire                iob_i_valid;
   wire                iob_d_valid;

   //iob interface wires
   wire                iob_i_rvalid;
   wire                iob_d_rvalid;
   wire                iob_d_ready;

   //compute the instruction bus request
   assign ibus_iob_valid = iob_i_valid;
   assign ibus_iob_addr  = cpu_addr;
   assign ibus_iob_wdata = {DATA_W{1'b0}};
   assign ibus_iob_wstrb = {(DATA_W / 8) {1'b0}};

   //compute the data bus request
   assign dbus_iob_valid = iob_d_valid;
   assign dbus_iob_addr  = cpu_addr;
   assign dbus_iob_wdata = cpu_wdata;
   assign dbus_iob_wstrb = cpu_wstrb;

   //split cpu bus into instruction and data buses
   assign iob_i_valid      = cpu_instr & cpu_valid;

   assign iob_d_valid      = (~cpu_instr) & cpu_valid & (~iob_d_rvalid);

   //extract iob interface wires from concatenated buses
   assign iob_d_rvalid     = dbus_iob_rvalid;
   assign iob_i_rvalid     = ibus_iob_rvalid;
   assign iob_d_ready      = dbus_iob_ready;

   //cpu rdata and ready
   assign cpu_rdata        = cpu_instr ? ibus_iob_rdata : dbus_iob_rdata;
   assign cpu_ready        = cpu_instr ? iob_i_rvalid : |cpu_wstrb ? iob_d_ready : iob_d_rvalid;

   assign cpu_reset = rst_i | arst_i;

   //intantiate the PicoRV32 CPU
   picorv32 #(
      .COMPRESSED_ISA (USE_COMPRESSED),
      .ENABLE_FAST_MUL(USE_MUL_DIV),
      .ENABLE_DIV     (USE_MUL_DIV),
      .BARREL_SHIFTER (1)
   ) picorv32_core (
      .clk         (clk_i),
      .resetn      (~cpu_reset),
      .trap        (),
      .mem_instr   (cpu_instr),
      //memory interface
      .mem_valid   (cpu_valid),
      .mem_addr    (cpu_addr),
      .mem_wdata   (cpu_wdata),
      .mem_wstrb   (cpu_wstrb),
      .mem_rdata   (cpu_rdata),
      .mem_ready   (cpu_ready),
      //lookahead interface
      .mem_la_read (),
      .mem_la_write(),
      .mem_la_addr (),
      .mem_la_wdata(),
      .mem_la_wstrb(),
      //co-processor interface (PCPI)
      .pcpi_valid  (),
      .pcpi_insn   (),
      .pcpi_rs1    (),
      .pcpi_rs2    (),
      .pcpi_wr     (1'b0),
      .pcpi_rd     (32'd0),
      .pcpi_wait   (1'b0),
      .pcpi_ready  (1'b0),
      // IRQ
      .irq         (plic_interrupts_i),
      .eoi         (),
      .trace_valid (),
      .trace_data  ()
   );


// Connect unused CLINT interface to zero
assign clint_iob_rvalid_o = 1'b0;
assign clint_iob_rdata_o = 20'b0;
assign clint_iob_ready_o = 1'b0;
//clint_iob_valid_i,
//clint_iob_addr_i,
//clint_iob_wdata_i,
//clint_iob_wstrb_i

// Connect unused PLIC interface to zero
assign plic_iob_rvalid_o = 1'b0;
assign plic_iob_rdata_o = 14'b0;
assign plic_iob_ready_o = 1'b0;
//plic_iob_valid_i,
//plic_iob_addr_i,
//plic_iob_wdata_i,
//plic_iob_wstrb_i,
"""
            }
        ],
    }

    return attributes_dict
