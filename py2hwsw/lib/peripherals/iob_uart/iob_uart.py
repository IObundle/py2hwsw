# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    CSR_IF = py_params_dict["csr_if"] if "csr_if" in py_params_dict else "iob"
    NAME = py_params_dict["name"] if "name" in py_params_dict else "iob_uart"
    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "version": "0.1",
        "board_list": ["cyclonev_gt_dk", "aes_ku040_db_g"],
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width.",
            },
            {
                "name": "RST_POL",
                "type": "M",
                "val": "1",
                "min": "0",
                "max": "1",
                "descr": "Reset polarity.",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "rs232_m",
                "signals": {
                    "type": "rs232",
                },
                "descr": "RS232 interface",
            },
        ],
        "wires": [
            {
                "name": "softreset",
                "descr": "",
                "signals": [
                    {"name": "softreset_wr", "width": 1},
                ],
            },
            {
                "name": "div",
                "descr": "",
                "signals": [
                    {"name": "div_wr", "width": 16},
                ],
            },
            {
                "name": "txdata",
                "descr": "",
                "signals": [
                    {"name": "txdata_wdata_wr", "width": 8},
                    {"name": "txdata_wen_wr", "width": 1},
                    {"name": "txdata_wready_wr", "width": 1},
                ],
            },
            {
                "name": "txen",
                "descr": "",
                "signals": [
                    {"name": "txen_wr", "width": 1},
                ],
            },
            {
                "name": "rxen",
                "descr": "",
                "signals": [
                    {"name": "rxen_wr", "width": 1},
                ],
            },
            {
                "name": "txready",
                "descr": "",
                "signals": [
                    {"name": "txready_rd", "width": 1},
                ],
            },
            {
                "name": "rxready",
                "descr": "",
                "signals": [
                    {"name": "rxready_rd", "width": 1},
                ],
            },
            {
                "name": "rxdata",
                "descr": "",
                "signals": [
                    {"name": "rxdata_rdata_rd", "width": 8},
                    {"name": "rxdata_rvalid_rd", "width": 1},
                    {"name": "rxdata_ren_rd", "width": 1},
                    {"name": "rxdata_rready_rd", "width": 1},
                ],
            },
            # RXDATA reg
            {
                "name": "iob_reg_rvalid_data_i",
                "descr": "",
                "signals": [
                    {"name": "rxdata_rvalid_nxt", "width": 1},
                ],
            },
            {
                "name": "iob_reg_rvalid_data_o",
                "descr": "",
                "signals": [
                    {"name": "rxdata_rvalid_rd"},
                ],
            },
            # uart core
            {
                "name": "clk_rst",
                "descr": "Clock and reset",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "arst_i"},
                ],
            },
            {
                "name": "iob_uart_core_reg_interface",
                "descr": "",
                "signals": [
                    {"name": "softreset_wr"},
                    {"name": "txen_wr"},
                    {"name": "rxen_wr"},
                    {"name": "txready_rd"},
                    {"name": "rxready_rd"},
                    {"name": "txdata_wdata_wr"},
                    {"name": "rxdata_rdata_rd"},
                    {"name": "txdata_wen_wr"},
                    {"name": "rxdata_ren_rd"},
                    {"name": "div_wr"},
                ],
            },
        ],
        "subblocks": [
            # iob_csrs 'control_if_s' port is connected automatically by py2hwsw
            f"""iob_csrs iob_uart_csrs 
				-d 'Control/Status Registers' 
                --no_autoaddr 
                --rw_overlap 
                -c 
                    "clk_en_rst_s":"clk_en_rst_s"
                    "softreset_o":"softreset"
                    "div_o":"div"
                    "txdata_io":"txdata"
                    "txen_o":"txen"
                    "txready_i":"txready"
                    "rxen_o":"rxen"
                    "rxready_i":"rxready"
                    "rxdata_io":"rxdata"
                --csr_if {CSR_IF}
                --csr-group 
				    uart 
                    -d 'UART software accessible registers' 
                        -r softreset:1 -t W -d 'Soft reset'  --rst_val 0 --addr 0 --log2n_items 0
                        -r div:16 -t W -d 'Bit duration in system clock cycles.' --rst_val 0 --addr 2 --log2n_items 0
                        -r txdata:8 -t W -d 'TX data.' --rst_val 0 --addr 4 --log2n_items 0 --no_autoreg
                        -r txen:1 -t W -d 'TX enable.' --rst_val 0 --addr 5 --log2n_items 0
				        -r rxen:1 -t W -d 'RX enable.' --rst_val 0 --addr 6 --log2n_items 0
                        -r txready:1 -t R -d 'TX ready to receive data.' --rst_val 0 --addr 0 --log2n_items 0
                        -r rxready:1 -t R -d 'RX ready to be read.' --rst_val 0 --addr 1 --log2n_items 0
                        -r rxdata:8 -t R -d 'RX data.' --rst_val 0 --addr 4 --log2n_items 0 --no_autoreg
            """,
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_rvalid",
                "instance_description": "Register for rxdata rvalid",
                "parameters": {
                    "DATA_W": 1,
                    "RST_VAL": "1'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "iob_reg_rvalid_data_i",
                    "data_o": "iob_reg_rvalid_data_o",
                },
            },
            {
                "core_name": "iob_uart_core",
                "instance_name": "iob_uart_core_inst",
                "instance_description": "UART core driver",
                "connect": {
                    "clk_rst_s": "clk_rst",
                    "reg_interface_io": "iob_uart_core_reg_interface",
                    "rs232_m": "rs232_m",
                },
            },
        ],
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    // txdata Manual logic
    assign txdata_wready_wr = 1'b1;

    // rxdata Manual logic
    assign rxdata_rready_rd = 1'b1;

    // rxdata rvalid is iob_valid registered
    assign rxdata_rvalid_nxt = rxdata_ren_rd;
""",
            },
        ],
    }

    return attributes_dict
