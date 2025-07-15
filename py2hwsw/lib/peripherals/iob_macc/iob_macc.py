# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    CSR_IF = py_params_dict["csr_if"] if "csr_if" in py_params_dict else "iob"
    NAME = py_params_dict["name"] if "name" in py_params_dict else "iob_macc"
    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "board_list": ["iob_cyclonev_gt_dk", "iob_aes_ku040_db_g"],
        "description": "The IObundle MACC is a RISC-V-based Peripheral written in Verilog, which users can download for free, modify, simulate and implement in FPGA or ASIC. It is written in Verilog and includes a C software driver. The IObundle MACC is a very compact IP that works at high clock rates if needed. It supports full-duplex operation and a configurable baud rate. The IObundle MACC has a fixed configuration for the Start and Stop bits. More flexible licensable commercial versions are available upon request.",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width.",
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
        ],
        "buses": [
            {
                "name": "en",
                "descr": "Enable",
                "signals": [
                    {"name": "en", "width": 1},
                ],
            },
            {
                "name": "enp",
                "descr": "Enable",
                "signals": [
                    {"name": "enp", "width": 1},
                ],
            },
            {
                "name": "en_int",
                "descr": "Enable internal",
                "signals": [
                    {"name": "en_int", "width": 1},
                ],
            },
            {
                "name": "load",
                "descr": "Load",
                "signals": [
                    {"name": "load", "width": 1},
                ],
            },
            {
                "name": "a",
                "descr": "operand a",
                "signals": [
                    {"name": "a", "width": 8},
                ],
            },
            {
                "name": "b",
                "descr": "operand b",
                "signals": [
                    {"name": "b", "width": 8},
                ],
            },
            {
                "name": "mul1",
                "descr": "Multiplier reg 1",
                "signals": [
                    {"name": "mul1", "width": 16},
                ],
            },
            {
                "name": "mul2",
                "descr": "Multiplier reg 2",
                "signals": [
                    {"name": "mul2", "width": 16},
                ],
            },
            {
                "name": "acc",
                "descr": "Accumulator",
                "signals": [
                    {"name": "acc", "width": 16},
                ],
            },
            {
                "name": "done",
                "descr": "Done",
                "signals": [
                    {"name": "done", "width": 3},
                ],
            },
            {
                "name": "done_int",
                "descr": "Done internal",
                "signals": [
                    {"name": "done_int", "width": 1},
                ],
            },
        ],
        "subblocks": [
            # iob_csrs 'control_if_s' port is connected automatically by py2hwsw
            f"""iob_csrs iob_csrs
                -d 'Control/Status Registers' 
                -c 
                    "clk_en_rst_s":"clk_en_rst_s"
                    "en_o":"en"
                    "done_i":"done_int"
                    "load_o":"load"
                    "a_o":"a"
                    "b_o":"b"
                    "c_i":"acc"
                --csr_if {CSR_IF}
                --csr-group macc 
                    -d 'MACC software accessible registers' 
                        -r en:1   -m W -d 'Enable.'
                        -r done:1 -m R -d 'Done.'
                        -r load:1 -m W -d 'Load.'
                        -r a:8    -m W -d 'Operand A.'
                        -r b:8    -m W -d 'Operand B.'
                        -r c:16   -m R -d 'Operand C.'
            """,
        ],
        "superblocks": [
            # Tester
            {
                "core_name": "iob_macc_tester",
                "dest_dir": "tester",
            },
            # Simulation wrapper
            {
                "core_name": "iob_macc_sim",
                "dest_dir": "hardware/simulation/src",
                "csr_if": CSR_IF,
            },
        ],
        "comb": {
            "code": """
            mul1_nxt = a*b;
            mul2_nxt = mul1;
            en_int_nxt = en;
            enp = en & ~en_int;
            acc_nxt = done[2]? (load? mul2: mul2+acc): acc;
            done_nxt = {done[1], done[0], enp};
            done_int_nxt = enp? 1'b0: (done[2] | done_int);
            """,
        },
    }

    return attributes_dict
