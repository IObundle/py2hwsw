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
                "max": "8",
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
                "val": "1",
                "min": "1",
                "max": "32",
            },
            {
                "name": "WSTRB_W",
                "descr": "AXI write strobe width",
                "type": "D",
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
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "start_addr_i",
                "descr": "Burst start address",
                "signals": [{"name": "start_addr_i", "width": "AXI_ADDR_W"}],
            },
            {
                "name": "length_i",
                "descr": "Burst length",
                "signals": [{"name": "length_i", "width": "(AXI_LEN_W+1)"}],
            },
            {
                "name": "write_data_i",
                "descr": "Write data",
                "signals": [{"name": "write_data_i", "width": "AXI_DATA_W"}],
            },
            {
                "name": "write_strobe_i",
                "descr": "Write strobe",
                "signals": [{"name": "write_strobe_i", "width": "WSTRB_W"}],
            },
            {
                "name": "busy_o",
                "descr": "Signal indicating if the module is busy transferring data",
                "signals": [{"name": "busy_o", "isvar": True}],
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
                "name": "write_fifo_external_mem_bus_m",
                "descr": "Port for connection to external iob_ram_t2p memory",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "write_fifo_ext_mem_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "wires": [
            {
                "name": "fifo_wen",
                "descr": "Write enable for the FIFO",
                "signals": [{"name": "fifo_wen", "isvar": True}],
            },
            {
                "name": "fifo_w_full",
                "descr": "FIFO write full signal",
                "signals": [{"name": "fifo_w_full"}],
            },
            {
                "name": "fifo_ren",
                "descr": "Read enable for the FIFO",
                "signals": [{"name": "fifo_ren"}],
            },
            {
                "name": "fifo_rdata",
                "descr": "FIFO read data",
                "signals": [{"name": "fifo_rdata", "width": "AXI_DATA_W"}],
            },
            {
                "name": "fifo_r_empty",
                "descr": "FIFO read empty signal",
                "signals": [{"name": "fifo_r_empty"}],
            },
            {
                "name": "en_fifo2axis",
                "descr": "Enable signal for FIFO to AXI-Stream converter",
                "signals": [{"name": "en_fifo2axis", "isvar": True}],
            },
            {
                "name": "internal_axis_signals",
                "descr": "Internal signals for the AXI-Stream interface",
                "signals": {
                    "type": "axis",
                    "prefix": "int_",
                    "DATA_W": "AXI_DATA_W",
                },
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
            {
                "name": "axis_s_axi_m_config_write_if",
                "descr": "AXI-Stream to AXI write burst converter configuration interface",
                "signals": [
                    {"name": "start_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "length_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "wstrb_int", "width": "WSTRB_W", "isvar": True},
                    {"name": "start_transfer"},
                    {"name": "write_busy"},
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
                    "w_en_i": "fifo_wen",
                    "w_data_i": "write_data_i",
                    "w_full_o": "fifo_w_full",
                    "r_en_i": "fifo_ren",
                    "r_data_o": "fifo_rdata",
                    "r_empty_o": "fifo_r_empty",
                    "level_o": "level_o",
                    "extmem_io": "write_fifo_external_mem_bus_m",
                },
            },
            {
                "core_name": "iob_fifo2axis",
                "instance_name": "write_data_fifo_axis",
                "instance_description": "FIFO to AXI-Stream converter",
                "parameters": {
                    "DATA_W": "AXI_DATA_W",
                },
                "use_en": True,
                "connect": {
                    "clk_en_rst_s": "fifo2axis_clk_if",
                    "en_i": "en_fifo2axis",
                    "fifo_read_o": "fifo_ren",
                    "fifo_rdata_i": "fifo_rdata",
                    "fifo_empty_i": "fifo_r_empty",
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
                    "clk_en_rst_s": "fifo2axis_clk_if",
                    "config_write_io": "axis_s_axi_m_config_write_if",
                    "axis_in_io": "internal_axis_signals",
                    "axi_write_m": "axi_write_m",
                },
            },
        ],
        "fsm": {
            "type": "fsm",
            "default_assignments": """
        fifo_wen = |write_strobe_i;
        // Default assignments
        start_transfer = 1'b0;
        busy_o = 1'b0;
        en_fifo2axis = 1'b0;
        wstrb_int = {WSTRB_W{1'b0}};
        """,
            "state_descriptions": """
        WAIT_DATA: // Start transfer when enough data is available in the FIFO
            if (level_o == length_i) begin
                start_transfer = 1'b1;
                en_fifo2axis = 1'b1;
                busy_o = 1'b1;
                state_nxt = TRANSF_DATA;
            end

        TRANSF_DATA: // Transfer data
            busy_o = 1'b1;
            en_fifo2axis = 1'b1;
            wstrb_int = {WSTRB_W{1'b1}};
            if (!write_busy) begin // Wait for the AXI write burst converter to finish
                state_nxt = WAIT_DATA;
            end
        """,
        },
    }

    return attributes_dict
