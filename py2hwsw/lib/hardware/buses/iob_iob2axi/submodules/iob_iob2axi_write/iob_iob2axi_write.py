# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            # AXI parameters
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": "8",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "P",
                "val": "4",
                "min": "1",
                "max": "4",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "P",
                "val": "32",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "P",
                "val": "0",
                "min": "0",
                "max": "32",
            },
            {
                "name": "WSTRB_W",
                "descr": "AXI write strobe width",
                "type": "F",
                "val": "AXI_DATA_W/8",
                "min": "1",
                "max": "32",
            },
        ],
        "ports": [
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
                "signals": [
                    {
                        "name": "rst_i",
                        "width": 1,
                        "descr": "Reset signal",
                    },
                ],
            },
            {
                "name": "start_addr_i",
                "descr": "Burst start address",
                "signals": [
                    {
                        "name": "start_addr_i",
                        "width": "AXI_ADDR_W",
                        "descr": "Burst start address",
                    },
                ],
            },
            {
                "name": "length_i",
                "descr": "Burst length minus 1",
                "signals": [
                    {
                        "name": "length_i",
                        "width": "AXI_LEN_W",
                        "descr": "Burst length minus 1",
                    },
                ],
            },
            {
                "name": "write_data_i",
                "descr": "Write data",
                "signals": [
                    {
                        "name": "write_data_i",
                        "width": "AXI_DATA_W",
                        "descr": "Write data",
                    },
                ],
            },
            {
                "name": "write_strobe_i",
                "descr": "Write strobe",
                "signals": [
                    {
                        "name": "write_strobe_i",
                        "width": "WSTRB_W",
                        "descr": "Write strobe",
                    },
                ],
            },
            {
                "name": "write_ready_o",
                "descr": "Write ready",
                "signals": [
                    {
                        "name": "write_ready_o",
                        "width": 1,
                        "descr": "Write ready",
                    },
                ],
            },
            {
                "name": "level_o",
                "descr": "FIFO level",
                "signals": [
                    {
                        "name": "level_o",
                        "width": "AXI_LEN_W+1",
                        "descr": "FIFO level",
                    },
                ],
            },
            {
                "name": "axi_write_m",
                "descr": "AXI write interface",
                "signals": {
                    "type": "axi_write",
                    "prefix": "m_",
                    "file_prefix": "iob_iob2axi_write_m_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external iob_ram_t2p memory",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "write_fifo_ext_mem_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "wires": [
            {
                "name": "fifo_w_if",
                "descr": "FIFO write interface",
                "signals": [
                    {"name": "fifo_w_en", "width": 1},
                    {"name": "fifo_w_data", "width": "AXI_DATA_W"},
                    {"name": "fifo_w_full", "width": 1},
                ],
            },
            {
                "name": "fifo_r_if",
                "descr": "FIFO read interface",
                "signals": [
                    {"name": "fifo_r_en", "width": 1},
                    {"name": "fifo_r_data", "width": "AXI_DATA_W"},
                    {"name": "fifo_r_empty", "width": 1},
                ],
            },
            {
                "name": "fifo_level",
                "descr": "FIFO level",
                "signals": [
                    {"name": "fifo_level", "width": "AXI_LEN_W+1"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fifo_sync",
                "instance_name": "write_data_fifo",
                "instance_description": "Write data FIFO",
                "parameters": {
                    "W_DATA_W": "AXI_DATA_W",
                    "R_DATA_W": "AXI_DATA_W",
                    "ADDR_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst_i",
                    "write_io": "fifo_w_if",
                    "read_io": "fifo_r_if",
                    "extmem_io": "external_mem_bus_m",
                    "fifo_o": "fifo_level",
                },
            },
        ],
        "fsm": {
            "type": "fsm",
            "default_assignments": """
        m_axi_awaddr_o_nxt = start_addr_i;
        m_axi_awvalid_o_nxt = 1'b0;
        m_axi_wdata_o_nxt = write_data_i;
        m_axi_wstrb_o_nxt = write_strobe_i;
        m_axi_wvalid_o_nxt = 1'b0;
        m_axi_bready_o_nxt = 1'b0;
        m_axi_wlast_o_nxt = 1'b0;
        """,
            "state_descriptions": """
        WAIT_DATA:
        m_axi_awaddr_o_nxt = start_addr_i;
        m_axi_awvalid_o_nxt = 1'b0;
        m_axi_wdata_o_nxt = write_data_i;
        m_axi_wstrb_o_nxt = write_strobe_i;
        m_axi_wvalid_o_nxt = 1'b0;
        m_axi_bready_o_nxt = 1'b0;
        m_axi_wlast_o_nxt = 1'b0;
        if (start_addr_i != 0) begin
            state_nxt = START_BURST;
        end else begin
            state_nxt = WAIT_DATA;
        end

        START_BURST:
        m_axi_awaddr_o_nxt = start_addr_i;
        m_axi_awvalid_o_nxt = 1'b1;
        m_axi_wdata_o_nxt = write_data_i;
        m_axi_wstrb_o_nxt = write_strobe_i;
        m_axi_wvalid_o_nxt = 1'b1;
        m_axi_bready_o_nxt = 1'b0;
        m_axi_wlast_o_nxt = 1'b0;
        if (m_axi_awready_i) begin
            state_nxt = WRITE_DATA;
        end else begin
            state_nxt = START_BURST;
        end
        """,
        },
    }

    return attributes_dict
