# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "reg_interface_io",
                "descr": "",
                "signals": [
                    {"name": "rst_soft_i", "width": "1"},
                    {"name": "tx_en_i", "width": "1"},
                    {"name": "rx_en_i", "width": "1"},
                    {"name": "tx_ready_o", "width": "1"},
                    {"name": "rx_ready_o", "width": "1"},
                    {"name": "tx_data_i", "width": "8"},
                    {"name": "rx_data_o", "width": "8"},
                    {"name": "data_write_en_i", "width": "1"},
                    {"name": "data_read_en_i", "width": "1"},
                    {
                        "name": "bit_duration_i",
                        "width": "16",
                    },
                ],
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
                "name": "sync_clk_rst_s",
                "descr": "Synchronized Clock and reset",
                "signals": [
                    {
                        "name": "clk_i",
                    },
                    {
                        "name": "arst_i",
                    },
                ],
            },
            {
                "name": "cts_int",
                "descr": "CTS internal wire",
                "signals": [
                    {
                        "name": "cts_int",
                        "width": "1",
                        "descr": "CTS Internal Wire",
                    },
                ],
            },
            {
                "name": "cts_int",
                "descr": "CTS internal wire",
                "signals": [
                    {
                        "name": "cts_int",
                        "width": "1",
                        "descr": "CTS Internal Wire",
                    },
                ],
            },
            {
                "name": "txen",
                "descr": "TX Enable internal wire",
                "signals": [
                    {
                        "name": "txen",
                        "width": "1",
                        "descr": "TX Enable Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_data_int",
                "descr": "TX Data internal wire",
                "signals": [
                    {
                        "name": "tx_data_int",
                        "width": "8",
                        "descr": "TX Data Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_pc",
                "descr": "TX Parity Check internal wire",
                "signals": [
                    {
                        "name": "tx_pc",
                        "width": "2",
                        "descr": " TX Parity Check Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_pattern",
                "descr": "TX Pattern internal wire",
                "signals": [
                    {
                        "name": "tx_pattern",
                        "width": "10",
                        "descr": " TX Pattern Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_bitcnt",
                "descr": "TX Bit Count internal wire",
                "signals": [
                    {
                        "name": "tx_bitcnt",
                        "width": "4",
                        "descr": " TX Bit Count Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_cyclecnt",
                "descr": "TX Cycle Count internal wire",
                "signals": [
                    {
                        "name": "tx_cyclecnt",
                        "width": "16",
                        "descr": " TX Cycle Count Internal Wire",
                    },
                ],
            },
            {
                "name": "rx_pc",
                "descr": "RX Parity Check internal wire",
                "signals": [
                    {
                        "name": "rx_pc",
                        "width": "3",
                        "descr": " RX Parity Check Internal Wire",
                    },
                ],
            },
            {
                "name": "rx_cyclecnt",
                "descr": "RX Cycle Count internal wire",
                "signals": [
                    {
                        "name": "rx_cyclecnt",
                        "width": "16",
                        "descr": " RX Parity Check Internal Wire",
                    },
                ],
            },
            {
                "name": "rx_bitcnt",
                "descr": "RX Bit Count internal wire",
                "signals": [
                    {
                        "name": "rx_bitcnt",
                        "width": "4",
                        "descr": "RX Bit Count Internal Wire",
                    },
                ],
            },
            {
                "name": "rx_pattern",
                "descr": "RX Bit Count internal wire",
                "signals": [
                    {
                        "name": "rx_pattern",
                        "width": "8",
                        "descr": "RX Bit Count Internal Wire",
                    },
                ],
            },
            {
                "name": "tx_data",
                "descr": "TX Data internal wire",
                "signals": [
                    {
                        "name": "tx_data_i",
                    },
                ],
            },
            {
                "name": "rs232_int",
                "descr": "RS232 internal wire",
                "signals": [
                    {
                        "name": "rs232_cts_i",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_sync",
                "instance_name": "cts_sync",
                "parameters": {
                    "DATA_W": "1",
                },
                "connect": {
                    "clk_rst_s": "sync_clk_rst_s",
                    "signal_i": "rs232_int",
                    "signal_o": "cts_int",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "txdata_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_e",
                },
                "parameters": {
                    "DATA_W": "8",
                    "RST_VAL": "8'b0",
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "en_i: data_write_en_i",
                        ],
                    ),
                    "data_i": "tx_data",
                    "data_o": "tx_data_int",
                },
            },
        ],
        "comb": {
            "code": """
            rs232_txd_o = tx_pattern[0];
            txen = tx_en_i & cts_int;
     //TX
      tx_pc_nxt = tx_pc + 2'd1;  //increment pc by default
      tx_pc_rst = rst_soft_i;
      tx_pc_en = txen;

      tx_pattern_nxt = tx_pattern;
      tx_pattern_rst = rst_soft_i;
      tx_pattern_en = txen;

      tx_bitcnt_nxt = tx_bitcnt;
      tx_bitcnt_rst = rst_soft_i;
      tx_bitcnt_en = txen;

      tx_cyclecnt_nxt = tx_cyclecnt;
      tx_cyclecnt_rst = rst_soft_i;
      tx_cyclecnt_en = txen;

      tx_ready_o_nxt = tx_ready_o;
      tx_ready_o_rst = rst_soft_i;
      tx_ready_o_en = txen;


      


      case (tx_pc)

         0: begin  //wait for data to send
            tx_ready_o_nxt    = 1'b1;
            tx_bitcnt_nxt   = 4'd0;
            tx_cyclecnt_nxt = 16'd1;
            tx_pattern_nxt  = ~10'b0;
            if (!data_write_en_i) tx_pc_nxt = tx_pc;
            else tx_ready_o_nxt = 1'b0;
         end

         1: begin  //load tx pattern to send
            tx_pattern_nxt = {1'b1, tx_data_int[7:0], 1'b0};  //{stop, data, start}>>
         end

         default: begin  //send pattern
            tx_pc_nxt       = tx_pc;  //stay here util pattern sent
            tx_cyclecnt_nxt = tx_cyclecnt + 16'd1;  //increment cycle counter
            if (tx_cyclecnt == bit_duration_i)
               if (tx_bitcnt == 4'd9) begin  //stop bit sent sent
                  tx_pc_nxt = 2'd0;  //restart program 
               end else begin  //data bit sent
                  tx_pattern_nxt  = tx_pattern >> 1;
                  tx_bitcnt_nxt   = tx_bitcnt + 4'd1;  //send next bit
                  tx_cyclecnt_nxt = 16'd1;
               end
         end  // case: default
      endcase

//RX

     rx_ready_o_rst = rst_soft_i | data_read_en_i;

      rx_pc_nxt = rx_pc + 3'd1;  //increment pc by default
      rx_pc_rst = rst_soft_i;
      rx_pc_en = rx_en_i;

      rx_cyclecnt_nxt = rx_cyclecnt;
      rx_cyclecnt_rst = rst_soft_i;
      rx_cyclecnt_en = rx_en_i;

      rx_bitcnt_nxt = rx_bitcnt;
      rx_bitcnt_rst = rst_soft_i;
      rx_bitcnt_en = rx_en_i;

      rx_pattern_nxt = rx_pattern;
      rx_pattern_rst = rst_soft_i;
      rx_pattern_en = rx_en_i;
      
      rx_ready_o_nxt = rx_ready_o;
      rx_ready_o_rst = rst_soft_i;
      rx_ready_o_en = rx_en_i;

      rs232_rts_o_nxt = rs232_rts_o;
      rs232_rts_o_rst = rst_soft_i;
      rs232_rts_o_en = rx_en_i;

      rx_data_o_nxt = rx_data_o;
      rx_data_o_rst = rst_soft_i;
      rx_data_o_en = rx_en_i;


      case (rx_pc)

         0: begin  //sync up
            rs232_rts_o_nxt   = 1'b1;
            rx_ready_o_nxt    = 1'b0;
            rx_cyclecnt_nxt = 16'd1;
            rx_bitcnt_nxt   = 4'd0;
            if (!rs232_rxd_i)  //line is low, wait until it is high
               rx_pc_nxt = rx_pc;
         end

         1: begin  //line is high
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt != bit_duration_i) rx_pc_nxt = rx_pc;
            else if (!rs232_rxd_i)  //error: line returned to low early
               rx_pc_nxt = 3'd0;  //go back and resync
         end

         2: begin  //wait for start bit
            rx_cyclecnt_nxt = 16'd1;
            if (rs232_rxd_i)  //start bit (low) has not arrived, wait
               rx_pc_nxt = rx_pc;
         end

         3: begin  //start bit is here
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt != bit_duration_i / 2)  // wait half bit period
               rx_pc_nxt = rx_pc;
            else if (rs232_rxd_i)  //error: line returned to high unexpectedly 
               rx_pc_nxt = 3'd0;  //go back and resync
            else rx_cyclecnt_nxt = 16'd1;
         end

         default: begin  // receive data
            rx_cyclecnt_nxt = rx_cyclecnt + 16'd1;
            if (rx_cyclecnt_nxt == bit_duration_i) begin
               rx_cyclecnt_nxt = 16'd1;
               rx_bitcnt_nxt   = rx_bitcnt + 4'd1;
               rx_pattern_nxt  = {rs232_rxd_i, rx_pattern[7:1]};  //sample rx line
               if (rx_bitcnt == 4'd8) begin  //stop bit is here
                  rx_data_o_nxt   = rx_pattern;  //register rx data
                  rx_ready_o_nxt  = 1'b1;
                  rx_bitcnt_nxt = 4'd0;
                  rx_pc_nxt     = 3'd2;
               end else begin
                  rx_pc_nxt = rx_pc;  //wait for more bits
               end
            end else begin
               rx_pc_nxt = rx_pc;  //wait for more cycles
            end
         end
      endcase
   


            """,
        },
    }

    return attributes_dict
