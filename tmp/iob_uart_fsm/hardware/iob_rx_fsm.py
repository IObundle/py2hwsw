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

            rxen_i -s rx_en_i:1
            -d 'Transmit enable'

            rxdata_o -s rx_data_o:8
            -d 'Transmit data'

            rxready_o -s rx_ready_o:1
            -d 'Transmit ready'

            rs232_rxd_i -s rs232_rxd_i:1
            -d 'RS232 receive data'

            rs232_rts_o -s rs232_rts_o:1
            -d 'RS232 request to send'

            data_read_en_i -s data_read_en_i:1
            -d 'Data read enable'

            bit_duration_i -s bit_duration_i:16
            -d 'Bit duration'
            """
        ],
        "wires": [
            """
            rx_cyclecnt -s rx_cyclecnt:16
            -d 'clk cycle counter'

            rx_bitcnt -s rx_bitcnt:4
            -d 'bit cycle counter'

            rx_pattern -s rx_pattern:10
            -d 'pattern shift register'
            """
        ],
        "fsm": {
            "verilog_code": """
rs232_rts_nxt = 1;
rx_ready_o = 0;
rx_bitcnt_nxt = 0;
rx_cyclecnt_nxt = 1;
if (!rs232_rxd_i)  //line is low, wait until it is high
    pcnt_nxt = pcnt;                    

rx_cyclecnt_nxt = rx_cyclecnt + 1;
if (rx_cyclecnt != bit_duration_i) 
   pcnt_nxt = pcnt;
if (rs232_rxd_i)
   pcnt_nxt = pcnt;

rx_cyclecnt_nxt = 1;
if (rs232_rxd_i)  //start bit (low) has not arrived, wait
   pcnt_nxt = pcnt;

rx_cyclecnt_nxt = rx_cyclecnt + 1;
if (rx_cyclecnt != bit_duration_i / 2)  // wait half bit period
   pcnt_nxt = pcnt;
else if (rs232_rxd_i)  //error: line returned to high unexpectedly 
   pcnt_nxt = 0;  //go back and resync
else 
   rx_cyclecnt_nxt = 1;

"""
        },
    }

    return attributes_dict
