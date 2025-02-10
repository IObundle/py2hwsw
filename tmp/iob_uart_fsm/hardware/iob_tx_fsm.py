# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "version": "0.1",
        "generate_hw": True,
        "ports": [
            """
            rst_i -s rst_i:1
            -d 'Sync reset'

            txen_i -s tx_en_i:1
            -d 'Transmit enable'

            txdata_i -s tx_data_i:8
            -d 'Transmit data'

            txready_o -s tx_ready_o:1
            -d 'Transmit ready'

            rs232_txd_o -s rs232_txd_o:1
            -d 'RS232 transmit data'

            bit_duration_i -s bit_duration_i:16
            -d 'Bit duration'
            """
        ],
        "wires": [
            """
            tx_cyclecnt -s tx_cyclecnt:16
            -d 'clk cycle counter'

            tx_bitcnt -s tx_bitcnt:4
            -d 'bit cycle counter'

            tx_pattern -s tx_pattern:10
            -d 'pattern shift register'
            """
        ],
        "fsm": {
            "verilog_code": """
default_assignments:
rs232_txd_o = tx_pattern[0];

tx_ready_o = 0;
tx_bitcnt_nxt = 0;
tx_cyclecnt_nxt = 1;
tx_pattern_nxt = 0;
if (!data_write_en_i) 
    pc_nxt = pc;                    
else
    tx_ready_o = 1'b0;

tx_pattern_nxt = {1'b1, tx_data_int[7:0], 1'b0};

pc_nxt = pc;
tx_cyclecnt_nxt = tx_cyclecnt + 1;
if (tx_cyclecnt == bit_duration_i)
    if (tx_bitcnt == 4'd9) begin
        pc_nxt = 0;
    end else begin
        tx_pattern_nxt = tx_pattern >> 1;
        tx_bitcnt = tx_bitcnt + 4'd1;
        tx_cyclecnt = 1;
    end
"""
        },
        "superblocks": [
            # Simulation wrapper
            {
                "core_name": "iob_sim",
                "instance_name": "iob_sim",
                "dest_dir": "hardware/simulation/src",
            },
        ],
    }

    return attributes_dict
