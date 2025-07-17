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
                "signals": [{"name": "rst_i"}],
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
                "name": "start_transfer_i",
                "descr": "Start transfer signal",
                "signals": [{"name": "start_transfer_i"}],
            },
            {
                "name": "read_data_axis_io",
                "descr": "Read data AXI-Stream signals",
                "signals": [
                    {"name": "read_data_o", "width": "AXI_DATA_W"},
                    {"name": "read_data_valid_o"},
                    {"name": "read_data_ready_i"},
                ],
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
                "name": "axi_read_m",
                "descr": "AXI Read interface",
                "signals": {
                    "type": "axi_read",
                    "prefix": "m_",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "read_fifo_external_mem_bus_m",
                "descr": "Port for connection to external iob_ram_t2p memory",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "read_fifo_ext_mem_",
                    "ADDR_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "wires": [
            {
                "name": "clk_w_rst_ref",
                "descr": "FIFO to AXI-Stream clock interface",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "cke_i"},
                    {"name": "arst_i"},
                    {"name": "rst_i"},
                ],
            },
            {
                "name": "fifo_wen",
                "descr": "FIFO write enable signal",
                "signals": [{"name": "fifo_wen"}],
            },
            {
                "name": "fifo_wdata",
                "descr": "FIFO write data signal",
                "signals": [{"name": "fifo_wdata", "width": "AXI_DATA_W"}],
            },
            {
                "name": "fifo_full",
                "descr": "FIFO full signal",
                "signals": [{"name": "fifo_full"}],
            },
            {
                "name": "fifo_ren",
                "descr": "FIFO read enable signal",
                "signals": [{"name": "fifo_ren"}],
            },
            {
                "name": "fifo_rdata",
                "descr": "FIFO read data signal",
                "signals": [{"name": "fifo_rdata", "width": "AXI_DATA_W"}],
            },
            {
                "name": "fifo_empty",
                "descr": "FIFO empty signal",
                "signals": [{"name": "fifo_empty"}],
            },
            {
                "name": "axi2axis_signals",
                "descr": "Internal signals for the AXI converter AXI-Stream interface",
                "signals": {
                    "type": "axis",
                    "prefix": "axi2axis_",
                    "DATA_W": "AXI_DATA_W",
                },
            },
            {
                "name": "en_fifo2axis",
                "descr": "Enable signal for FIFO to AXI-Stream converter",
                "signals": [{"name": "en_fifo2axis", "isvar": True}],
            },
            {
                "name": "axis_s_axi_m_config_read_if",
                "descr": "AXI read burst converter to AXI-Stream configuration interface",
                "signals": [
                    {"name": "start_addr_i", "width": "AXI_ADDR_W"},
                    {"name": "length_i", "width": "(AXI_LEN_W+1)"},
                    {"name": "start_transfer_i"},
                    {"name": "read_busy"},
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fifo2axis",
                "instance_name": "fifo2axis_inst",
                "instance_description": "FIFO to AXI-Stream converter",
                "parameters": {"DATA_W": "AXI_DATA_W"},
                "use_en": True,
                "connect": {
                    "clk_en_rst_s": "clk_w_rst_ref",
                    "fifo_read_o": "fifo_ren",
                    "fifo_rdata_i": "fifo_rdata",
                    "fifo_empty_i": "fifo_empty",
                    "en_i": "en_fifo2axis",
                    "axis_m": "read_data_axis_io",
                },
            },
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
                    "w_en_i": "fifo_wen",
                    "w_data_i": "fifo_wdata",
                    "w_full_o": "fifo_full",
                    "r_en_i": "fifo_ren",
                    "r_data_o": "fifo_rdata",
                    "r_empty_o": "fifo_empty",
                    "level_o": "level_o",
                    "extmem_io": "read_fifo_external_mem_bus_m",
                },
            },
            {
                "core_name": "iob_axis2fifo",
                "instance_name": "axis2fifo_inst",
                "instance_description": "AXI-Stream to FIFO converter",
                "parameters": {
                    "DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_w_rst_ref",
                    "fifo_write_o": "fifo_wen",
                    "fifo_wdata_o": "fifo_wdata",
                    "fifo_full_i": "fifo_full",
                    "axis_s": "axi2axis_signals",
                },
            },
            {
                "core_name": "iob_axis_s_axi_m_read_int",
                "instance_name": "axis_s_axi_m_read_inst",
                "instance_description": "AXI read burst to AXI-Stream converter",
                "parameters": {
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ID_W": "AXI_ID_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_w_rst_ref",
                    "config_read_io": "axis_s_axi_m_config_read_if",
                    "axis_out_io": "axi2axis_signals",
                    "axi_read_m": "axi_read_m",
                },
            },
        ],
        "fsm": {
            "type": "fsm",
            "default_assignments": """
        // Default assignments
        busy_o = 1'b0;
        en_fifo2axis = 1'b0;
        """,
            "state_descriptions": """
        WAIT_START: // Wait to start transfer
            if (start_transfer_i) begin
                state_nxt = WAIT_DATA;
            end

        WAIT_DATA: // Wait for data to be available in the FIFO
            if ((!read_busy) && (level_o == length_i)) begin // Wait for the data to be available
                en_fifo2axis = 1'b1;
                state_nxt = TRANSF_DATA;
            end else begin
                busy_o = 1'b1;
            end

        TRANSF_DATA: // Transfer data from FIFO to AXI-Stream
            en_fifo2axis = 1'b1;
            if (fifo_empty) begin // Wait for the FIFO to be empty
                state_nxt = WAIT_START;
            end
        """,
        },
    }

    return attributes_dict
