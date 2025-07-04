# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    # Confs List
    confs = [
        {
            "name": "ADDR_W",
            "descr": "",
            "type": "P",
            "val": "1",
            "min": "1",
            "max": "32",
        },
        {
            "name": "DATA_W",
            "descr": "",
            "type": "P",
            "val": "32",
            "min": "1",
            "max": "32",
        },
        # AXI parameters
        {
            "name": "AXI_ADDR_W",
            "descr": "AXI address bus width",
            "type": "D",
            "val": "ADDR_W",
            "min": "1",
            "max": "32",
        },
        {
            "name": "AXI_LEN_W",
            "descr": "AXI burst length width",
            "type": "P",
            "val": "6",
            "min": "1",
            "max": "8",
        },
        {
            "name": "AXI_DATA_W",
            "descr": "AXI data bus width",
            "type": "D",
            "val": "DATA_W",
            "min": "1",
            "max": "32",
        },
        {
            "name": "AXI_ID_W",
            "descr": "AXI ID bus width",
            "type": "P",
            "val": "1",
            "min": "1",
            "max": "32",
        },
    ]

    # Ports List
    ports = [
        {
            "name": "clk_en_rst_s",
            "signals": {
                "type": "iob_clk",
            },
            "descr": "Clock, clock enable and reset",
        },
        {
            "name": "rst_i",
            "descr": "Reset signal",
            "signals": [{"name": "rst_i", "descr": "Reset signal"}],
        },
        {
            "name": "iob_s",
            "descr": "Subordinate IOb interface",
            "signals": {
                "type": "iob",
                "ADDR_W": "ADDR_W",
                "DATA_W": "DATA_W",
            },
        },
        {
            "name": "axi_m",
            "descr": "Manager AXI interface",
            "signals": {
                "type": "axi",
                "prefix": "m_",
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        {
            "name": "control_io",
            "descr": "Control interface",
            "signals": [
                {
                    "name": "length_i",
                    "width": "(AXI_LEN_W+1)",
                    "descr": "Burst length",
                },
                {
                    "name": "w_level_o",
                    "width": "(AXI_LEN_W+1)",
                    "descr": "Write FIFO level",
                },
                {
                    "name": "r_level_o",
                    "width": "(AXI_LEN_W+1)",
                    "descr": "Read FIFO level",
                },
            ],
        },
    ]

    # Wires List
    wires = [
        {
            "name": "start_addr",
            "descr": "Start address for read/write",
            "signals": [
                {
                    "name": "start_addr",
                    "width": "ADDR_W",
                }
            ],
        },
        {
            "name": "start_addr_reg",
            "descr": "Start address register",
            "signals": [
                {
                    "name": "start_addr_reg",
                    "width": "ADDR_W",
                }
            ],
        },
        {
            "name": "write_data",
            "descr": "Write data for AXI",
            "signals": [
                {
                    "name": "iob_wdata_i",
                    "width": "DATA_W",
                },
            ],
        },
        {
            "name": "write_strobe",
            "descr": "Write strobe for AXI",
            "signals": [
                {
                    "name": "write_strobe",
                    "width": "DATA_W/8",
                },
            ],
        },
        {
            "name": "write_busy",
            "descr": "Write busy signal",
            "signals": [{"name": "write_busy"}],
        },
        {
            "name": "axi_write",
            "descr": "AXI write interface",
            "signals": [
                {"name": "m_axi_awaddr_o", "width": "AXI_ADDR_W"},
                {"name": "m_axi_awvalid_o"},
                {"name": "m_axi_awready_i"},
                {"name": "m_axi_wdata_o", "width": "AXI_DATA_W"},
                {"name": "m_axi_wstrb_o", "width": "AXI_DATA_W/8"},
                {"name": "m_axi_wvalid_o"},
                {"name": "m_axi_wready_i"},
                {"name": "m_axi_bresp_i", "width": 2},
                {"name": "m_axi_bvalid_i"},
                {"name": "m_axi_bready_o"},
                {"name": "m_axi_awid_o", "width": "AXI_ID_W"},
                {"name": "m_axi_awlen_o", "width": "AXI_LEN_W"},
                {"name": "m_axi_awsize_o", "width": 3},
                {"name": "m_axi_awburst_o", "width": 2},
                {"name": "m_axi_awlock_o", "width": 2},
                {"name": "m_axi_awcache_o", "width": 4},
                {"name": "m_axi_awqos_o", "width": 4},
                {"name": "m_axi_wlast_o"},
                {"name": "m_axi_bid_i", "width": "AXI_ID_W"},
            ],
        },
        {
            "name": "start_read_transfer",
            "descr": "Start read transfer signal",
            "signals": [{"name": "start_read_transfer", "isvar": True}],
        },
        {
            "name": "read_data_ready_rst",
            "descr": "Read data ready reset",
            "signals": [
                {"name": "read_data_ready_rst"},
            ],
        },
        {
            "name": "read_data_ready_en",
            "descr": "Read data ready enable",
            "signals": [
                {"name": "read_data_ready_en"},
            ],
        },
        {
            "name": "read_data_ready",
            "descr": "Read data ready signal",
            "signals": [
                {"name": "read_data_ready"},
            ],
        },
        {
            "name": "read_data_axis",
            "descr": "Read data AXI-Stream signals",
            "signals": [
                {"name": "iob_rdata_o", "width": "DATA_W"},
                {"name": "iob_rvalid_o"},
                {"name": "read_data_ready"},
            ],
        },
        {
            "name": "read_busy",
            "descr": "Read busy signal",
            "signals": [{"name": "read_busy"}],
        },
        {
            "name": "axi_read",
            "descr": "AXI read interface",
            "signals": [
                {"name": "m_axi_araddr_o", "width": "AXI_ADDR_W"},
                {"name": "m_axi_arvalid_o"},
                {"name": "m_axi_arready_i"},
                {"name": "m_axi_rdata_i", "width": "AXI_DATA_W"},
                {"name": "m_axi_rresp_i", "width": 2},
                {"name": "m_axi_rvalid_i"},
                {"name": "m_axi_rready_o"},
                {"name": "m_axi_arid_o", "width": "AXI_ID_W"},
                {"name": "m_axi_arlen_o", "width": "AXI_LEN_W"},
                {"name": "m_axi_arsize_o", "width": 3},
                {"name": "m_axi_arburst_o", "width": 2},
                {"name": "m_axi_arlock_o", "width": 2},
                {"name": "m_axi_arcache_o", "width": 4},
                {"name": "m_axi_arqos_o", "width": 4},
                {"name": "m_axi_rid_i", "width": "AXI_ID_W"},
                {"name": "m_axi_rlast_i"},
            ],
        },
        {
            "name": "length",
            "descr": "Length of the burst",
            "signals": [{"name": "length_i", "width": "(AXI_LEN_W+1)"}],
        },
        {
            "name": "w_level",
            "descr": "Write FIFO level",
            "signals": [{"name": "w_level_o", "width": "(AXI_LEN_W+1)"}],
        },
        {
            "name": "r_level",
            "descr": "Read FIFO level",
            "signals": [{"name": "r_level_o", "width": "(AXI_LEN_W+1)"}],
        },
        {
            "name": "ready",
            "descr": "Ready signal",
            "signals": [
                {
                    "name": "ready",
                    "isvar": True,
                    "descr": "Ready signal for the IOb interface",
                }
            ],
        },
        {
            "name": "en_write",
            "descr": "Write enable signal",
            "signals": [
                {
                    "name": "en_write",
                    "isvar": True,
                    "descr": "Write enable signal for the IOb interface",
                }
            ],
        },
    ]

    # Subblocks List
    subblocks = [
        {
            "core_name": "iob_iob_s_axi_m_write",
            "instance_name": "iob_s_axi_m_write_inst",
            "instance_description": "IOB to AXI write",
            "parameters": {
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_ID_W": "AXI_ID_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst_i",
                "start_addr_i": "start_addr",
                "length_i": "length",
                "write_data_i": "write_data",
                "write_strobe_i": "write_strobe",
                "busy_o": "write_busy",
                "level_o": "w_level",
                "axi_write_m": "axi_write",
            },
        },
        {
            "core_name": "iob_iob_s_axi_m_read",
            "instance_name": "iob_s_axi_m_read_inst",
            "instance_description": "IOB to AXI read",
            "parameters": {
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_DATA_W": "AXI_DATA_W",
                "AXI_ID_W": "AXI_ID_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst_i",
                "start_addr_i": "start_addr",
                "length_i": "length",
                "start_transfer_i": "start_read_transfer",
                "read_data_axis_io": "read_data_axis",
                "busy_o": "read_busy",
                "level_o": "r_level",
                "axi_read_m": "axi_read",
            },
        },
        {
            "core_name": "iob_reg",
            "instance_name": "read_data_ready_reg",
            "instance_description": "Register for read data ready logic",
            "parameters": {
                "DATA_W": 1,
                "RST_VAL": "1'b0",
            },
            "port_params": {
                "clk_en_rst_s": "c_a_r_e",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_rst_s",
                    [
                        "en_i:read_data_ready_en",
                        "rst_i:read_data_ready_rst",
                    ],
                ),
                "data_i": "read_data_ready_en",
                "data_o": "read_data_ready",
            },
        },
    ]

    # FSM List
    fsm = {
        "type": "fsm",
        "default_assignments": """
        en_write = |iob_wstrb_i;
        // Default assignments
        write_strobe = 0;
        start_addr_reg_nxt = start_addr_reg;
        start_addr = start_addr_reg;
        ready_nxt = 1'b1;
        start_read_transfer = 1'b0;
        """,
        "state_descriptions": """
        WAIT_OPERATION: // Wait for first operation that defines the start address
            if (iob_valid_i) begin
                start_addr = iob_addr_i;
                start_addr_reg_nxt = start_addr;
                if (en_write) begin
                    write_strobe = 4'b1111;
                    state_nxt = WRITE_OPERATION;
                end else begin
                    state_nxt = READ_OPERATION;
                    start_read_transfer = 1'b1;
                    ready_nxt = 1'b0;
                end
            end

        WRITE_OPERATION: // Write data to the fifo
            if (write_busy) begin
                ready_nxt = 1'b0;
                state_nxt = WAIT_WRITE_FINISH;
            end else begin
                if (en_write && iob_valid_i) begin
                    write_strobe = 4'b1111;
                end
            end

        WAIT_WRITE_FINISH: // Wait for the write operation to finish
            if (!write_busy) begin
                state_nxt = WAIT_OPERATION;
            end else begin
                ready_nxt = 1'b0;
            end

        READ_OPERATION: // Wait for the fifo to be filled
            if (!read_busy) begin
                state_nxt = WAIT_READ_FINISH;
            end else begin
                ready_nxt = 1'b0;
            end

        WAIT_READ_FINISH: // Wait for the read operation to finish
            if ((r_level_o == 0) && (!iob_rvalid_o)) begin
                state_nxt = WAIT_OPERATION;
            end
        """,
    }

    # Snippets List
    snippets = [
        {
            "verilog_code": """
        assign iob_ready_o = ready;
        assign read_data_ready_en = iob_valid_i & (!en_write) & iob_ready_o;
        assign read_data_ready_rst = iob_rvalid_o & read_data_ready;
        """
        },
    ]

    # Simulation wrapper
    superblocks = [
        {
            "core_name": "iob_iob_s_axi_m_sim",
            "dest_dir": "hardware/simulation/src",
        },
    ]

    attributes_dict = {
        "generate_hw": True,
        "confs": confs,
        "ports": ports,
        "wires": wires,
        "subblocks": subblocks,
        "fsm": fsm,
        "snippets": snippets,
        "superblocks": superblocks,
    }

    return attributes_dict
