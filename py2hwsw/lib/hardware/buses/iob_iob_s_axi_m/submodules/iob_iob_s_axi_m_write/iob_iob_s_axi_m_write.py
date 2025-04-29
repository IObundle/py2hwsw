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
                    },
                ],
            },
            {
                "name": "length_i",
                "descr": "Burst length",
                "signals": [
                    {
                        "name": "length_i",
                        "width": "(AXI_LEN_W+1)",
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
                    },
                ],
            },
            {
                "name": "busy_o",
                "descr": "Signal indicating if the module is busy transferring data",
                "signals": [
                    {
                        "name": "busy_o",
                    },
                ],
            },
            {
                "name": "level_o",
                "descr": "FIFO level",
                "signals": [
                    {
                        "name": "level_o",
                        "width": "(AXI_LEN_W+1)",
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
                    {"name": "fifo_wen", "isvar": True},
                    {"name": "fifo_w_data", "width": "AXI_DATA_W"},
                    {"name": "fifo_w_full"},
                ],
            },
            {
                "name": "fifo_r_if",
                "descr": "FIFO read interface",
                "signals": [
                    {"name": "fifo_ren"},
                    {"name": "fifo_r_data", "width": "AXI_DATA_W"},
                    {"name": "fifo_r_empty"},
                ],
            },
            {
                "name": "en_fifo2axis",
                "descr": "Enable signal for FIFO to AXI-Stream converter",
                "signals": [
                    {
                        "name": "en_fifo2axis",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "internal_axis_signals",
                "descr": "Internal signals for the AXI-Stream interface",
                "signals": {
                    "type": "axis",
                    "prefix": "int_",
                    "DATA_W": "DATA_W",
                },
            },
            {
                "name": "en_write",
                "descr": "Enable signal for write operation",
                "signals": [
                    {
                        "name": "en_write",
                        "isvar": True,
                    },
                ],
            },
            {
                "name": "fifo2axis_clk_if",
                "descr": "FIFO to AXI-Stream clock interface",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "cke_i"},
                    {"name": "arst_i"},
                    {"name": "rst_i"},
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
                    "fifo_o": "level_o",
                },
            },
            {
                "core_name": "iob_fifo2axis",
                "instance_name": "write_data_fifo_axis",
                "instance_description": "FIFO to AXI-Stream converter",
                "parameters": {
                    "DATA_W": "AXI_DATA_W",
                    "AXIS_LEN_W": "AXI_LEN_W+1",
                },
                "use_en": True,
                "connect": {
                    "clk_en_rst_s": "fifo2axis_clk_if",
                    "en_i": "en_fifo2axis",
                    "fifo_r_io": "fifo_r_if",
                    "axis_m": "internal_axis_signals",
                },
            },
            {
                "core_name": "iob_axis_s_axi_m_write_int",
                "instance_name": "axis_s_axi_m_write_inst",
                "instance_description": "AXI-Stream to AXI write burst converter",
                "parameters": {
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ID_W": "AXI_ID_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                },
            },
        ],
        "fsm": {
            "type": "fsm",
            "default_assignments": """
        en_write = |write_strobe_i;
        // Default assignments
        m_axi_awaddr_o_nxt = m_axi_awaddr_o;
        m_axi_awvalid_o_nxt = 1'b0;
        m_axi_awlen_o_nxt = m_axi_awlen_o;
        m_axi_wdata_o_nxt = write_data_i;
        m_axi_wstrb_o_nxt = {WSTRB_W{1'b0}};
        m_axi_wvalid_o_nxt = 1'b0;
        m_axi_bready_o_nxt = 1'b0;
        m_axi_wlast_o_nxt = 1'b0;
        fifo_wen = 1'b0;
        en_fifo2axis = 1'b0;
        """,
            "state_descriptions": """
        WAIT_DATA: // Start transfer in the next state
            if (en_write) begin
                fifo_wen = 1'b1;
                // If it has enough data, it will start the burst
                if((length_i == {AXI_LEN_W{1'b0}}) || {1'b0,length_i} == level_o) begin
                    m_axi_awaddr_o_nxt = start_addr_i;
                    m_axi_awvalid_o_nxt = 1'b1;
                    // If the burst's last address is in the next 4k boundary,
                    // the burst length is the remaining space in the current 4k boundary
                    if ((length_i != {AXI_LEN_W{1'b0}}) && (start_addr_i[12] != last_addr[12])) begin
                        m_axi_awlen_o_nxt = ((13'd4096 - (start_addr_i[0+:13])) >> 2) - 1;
                    end else begin
                        m_axi_awlen_o_nxt = length_i;
                    end
                    state_nxt = START_BURST;
                end
            end

        START_BURST: // Send burst address and length and wait for ready signal
            if (m_axi_awready_i) begin
                state_nxt = TRANSF_DATA;
            end else begin
                m_axi_awvalid_o_nxt = 1'b1;
            end

        TRANSF_DATA: // Transfer data
            en_fifo2axis = 1'b1;

        """,
        },
        "snippets": [
            {
                "verilog_code": """

    """
            },
        ],
    }

    return attributes_dict
