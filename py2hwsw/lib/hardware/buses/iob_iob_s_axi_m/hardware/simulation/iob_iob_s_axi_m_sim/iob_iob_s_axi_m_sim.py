# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "board_list": [],
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "32",
                "max": "32",
                "descr": "CPU data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "P",
                "val": "20",  # Enough space for AXI access and CSRs
                "min": "NA",
                "max": "32",
                "descr": "Address bus width",
            },
            # AXI parameters
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "P",
                "val": "16",
                "min": "1",
                "max": "28",
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
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "descr": "Clock, clock enable and reset",
                "signals": {
                    "type": "iob_clk",
                },
            },
            {
                "name": "pbus_s",
                "descr": "Testbench peripherals CSRs interface",
                "signals": {
                    "type": "iob",
                    "ADDR_W": "ADDR_W",  # Includes 2 LSBs
                },
            },
        ],
        "wires": [
            {
                "name": "soft_reset",
                "descr": "Soft reset signal",
                "signals": [
                    {"name": "soft_reset"},
                ],
            },
            {
                "name": "uut_access",
                "descr": "UUT access signal",
                "signals": {
                    "type": "iob",
                    "prefix": "uut_access_",
                    "ADDR_W": "AXI_ADDR_W",
                },
            },
            {
                "name": "axi_access",
                "descr": "AXI access signal",
                "signals": {
                    "type": "axi",
                    "prefix": "axi_m_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "iob_s_axi_m_control_length",
                "descr": "Burst length signal",
                "signals": [
                    {
                        "name": "iob_s_axi_m_control_length",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "iob_s_axi_m_control_w_level",
                "descr": "Write level signal",
                "signals": [
                    {
                        "name": "iob_s_axi_m_control_w_level",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "iob_s_axi_m_control_r_level",
                "descr": "Read level signal",
                "signals": [
                    {
                        "name": "iob_s_axi_m_control_r_level",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "iob_s_axi_m_control",
                "descr": "Control signals",
                "signals": [
                    {
                        "name": "iob_s_axi_m_control_length",
                        "width": "(AXI_LEN_W+1)",
                    },
                    {
                        "name": "iob_s_axi_m_control_w_level",
                        "width": "(AXI_LEN_W+1)",
                    },
                    {
                        "name": "iob_s_axi_m_control_r_level",
                        "width": "(AXI_LEN_W+1)",
                    },
                ],
            },
            {
                "name": "split_reset",
                "descr": "Split reset signal",
                "signals": [
                    {"name": "arst_i"},
                ],
            },
            {
                "name": "split_control_csrs",
                "descr": "Control/Status Registers interface",
                "signals": {
                    "type": "iob",
                    "prefix": "split_control_",
                    "ADDR_W": 16,
                },
            },
            {
                "name": "control_csrs",
                "descr": "Control/Status Registers interface",
                "signals": {
                    "type": "iob",
                    "prefix": "control_",
                    "ADDR_W": 4,
                },
            },
            {
                "name": "clk",
                "descr": "Clock signal",
                "signals": [{"name": "clk_i"}],
            },
            {
                "name": "axi_ram_ext_mem",
                "descr": "AXI RAM external memory bus",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                },
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_split",
                "name": "tb_pbus_split",
                "instance_name": "iob_pbus_split",
                "instance_description": "Split between testbench peripherals",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "reset_i": "split_reset",
                    "input_s": ("pbus_s", ["iob_addr_i[16:0]"]),
                    "output_0_m": "uut_access",
                    "output_1_m": "split_control_csrs",
                },
                "num_outputs": 2,
                "addr_w": 17,
            },
            {
                "core_name": "iob_memwrapper",
                "instance_name": "uut_inst",
                "instance_description": "Unit Under Test (UUT)",
                "parameters": {
                    "ADDR_W": "AXI_ADDR_W",
                    "DATA_W": "DATA_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ID_W": "AXI_ID_W",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "rst_i: soft_reset",
                        ],
                    ),
                    "iob_s": "uut_access",
                    "axi_m": "axi_access",
                    "control_io": "iob_s_axi_m_control",
                },
            },
            {
                "core_name": "iob_s_axi_m_sim_controller",
                "instance_name": "iob_s_axi_m_sim_controller_inst",
                "instance_description": "Length and levels controller",
                "parameters": {
                    "AXI_LEN_W": "AXI_LEN_W",
                    "DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "iob_csrs_cbus_s": "control_csrs",
                    "soft_reset_o": "soft_reset",
                    "burst_length_o": "iob_s_axi_m_control_length",
                    "w_level_i": "iob_s_axi_m_control_w_level",
                    "r_level_i": "iob_s_axi_m_control_r_level",
                },
            },
            {
                "core_name": "iob_axi_ram",
                "instance_name": "iob_axi_ram_inst",
                "instance_description": "AXI RAM",
                "parameters": {
                    "DATA_WIDTH": "AXI_DATA_W",
                    "ADDR_WIDTH": "AXI_ADDR_W",
                    "ID_WIDTH": "AXI_ID_W",
                    "LEN_WIDTH": "AXI_LEN_W",
                },
                "connect": {
                    "clk_i": "clk",
                    "rst_i": "soft_reset",
                    "axi_s": "axi_access",
                    "external_mem_bus_m": "axi_ram_ext_mem",
                },
            },
            {
                "core_name": "iob_ram_t2p_be",
                "instance_name": "iob_ram_t2p_be_inst",
                "instance_description": "Memory for AXI RAM",
                "parameters": {
                    "HEXFILE": '"none"',
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "ram_t2p_be_s": "axi_ram_ext_mem",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": """
            assign control_iob_valid = split_control_iob_valid;
            assign control_iob_addr = split_control_iob_addr[3:0];
            assign control_iob_wdata = split_control_iob_wdata;
            assign control_iob_wstrb = split_control_iob_wstrb;
            assign split_control_iob_rvalid = control_iob_rvalid;
            assign split_control_iob_rdata = control_iob_rdata;
            assign split_control_iob_ready = control_iob_ready;
            """
            },
        ],
    }

    return attributes_dict
