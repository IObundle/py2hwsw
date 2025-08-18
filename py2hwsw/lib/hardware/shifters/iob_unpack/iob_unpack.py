# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": False,
        "confs": [
            {
                "name": "DATA_W",
                "descr": "Data width",
                "type": "P",
                "val": "21",
                "min": "NA",
                "max": "NA",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "c_a_r",
                },
                "descr": "Clock, clock enable, async and sync reset",
            },
            {
                "name": "wrap_i",
                "descr": "Wrap input",
                "signals": [
                    {
                        "name": "wrap_i",
                        "width": "1",
                        "descr": "Wrap input signal",
                    },
                ],
            },
            {
                "name": "width_i",
                "descr": "Width input",
                "signals": [
                    {
                        "name": "width_i",
                        "width": "$clog2(DATA_W)+1",
                        "descr": "Width input signal",
                    },
                ],
            },
            {
                "name": "read_o",
                "descr": "Read output",
                "signals": [
                    {
                        "name": "read_o",
                        "width": "1",
                        "descr": "Read output signal",
                    },
                ],
            },
            {
                "name": "rready_i",
                "descr": "Read ready input",
                "signals": [
                    {
                        "name": "rready_i",
                        "width": "1",
                        "descr": "Read ready input signal",
                    },
                ],
            },
            {
                "name": "rdata_i",
                "descr": "Read data input",
                "signals": [
                    {
                        "name": "rdata_i",
                        "width": "DATA_W",
                        "descr": "Read data input signal",
                    },
                ],
            },
            {
                "name": "write_o",
                "descr": "Write output",
                "signals": [
                    {
                        "name": "write_o",
                        "width": "1",
                        "descr": "Write output signal",
                    },
                ],
            },
            {
                "name": "wready_i",
                "descr": "Write ready input",
                "signals": [
                    {
                        "name": "wready_i",
                        "width": "1",
                        "descr": "Write ready input signal",
                    },
                ],
            },
            {
                "name": "wdata_o",
                "descr": "Write data output",
                "signals": [
                    {
                        "name": "wdata_o",
                        "width": "DATA_W",
                        "descr": "Write data output signal",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "push_level",
                "descr": "Push level wire",
                "signals": [
                    {
                        "name": "push_level",
                        "width": "$clog2(2*DATA_W)+1",
                        "descr": "Push Level Wire",
                    },
                ],
            },
            {
                "name": "push_width",
                "descr": "Push width wire",
                "signals": [
                    {
                        "name": "push_width",
                        "isvar": True,
                        "width": "$clog2(DATA_W)+1",
                        "descr": "Push Width Wire",
                    },
                ],
            },
            {
                "name": "push",
                "descr": "Push wire",
                "signals": [
                    {
                        "name": "push",
                        "isvar": True,
                        "width": "1",
                        "descr": "Push Wire",
                    },
                ],
            },
            {
                "name": "pop_level",
                "descr": "Pop level wire",
                "signals": [
                    {
                        "name": "pop_level",
                        "width": "$clog2(2*DATA_W)+1",
                        "descr": "Pop Level Wire",
                    },
                ],
            },
            {
                "name": "pop",
                "descr": "Pop wire",
                "signals": [
                    {
                        "name": "pop",
                        "isvar": True,
                        "width": "1",
                        "descr": "Pop Wire",
                    },
                ],
            },
            {
                "name": "wrap_acc_nxt",
                "descr": "Wrap next wire",
                "signals": [
                    {
                        "name": "wrap_acc_nxt",
                        "isvar": True,
                        "width": "$clog2(DATA_W)+1",
                        "descr": "Wrap Next Wire",
                    },
                ],
            },
            {
                "name": "wrap_acc",
                "descr": "Wrap current wire",
                "signals": [
                    {
                        "name": "wrap_acc",
                        "width": "$clog2(DATA_W)+1",
                        "descr": "Wrap Current Wire",
                    },
                ],
            },
            {
                "name": "wrap_acc_int",
                "descr": "Wrap current internal wire",
                "signals": [
                    {
                        "name": "wrap_acc_int",
                        "isvar": True,
                        "width": "$clog2(DATA_W)+2",
                        "descr": "Wrap Current Internal Wire",
                    },
                ],
            },
            {
                "name": "pcnt",
                "descr": "Push count wire",
                "signals": [
                    {
                        "name": "pcnt",
                        "width": "2",
                        "descr": "Push Count Wire",
                    },
                ],
            },
            {
                "name": "pcnt_nxt",
                "descr": "Push count next wire",
                "signals": [
                    {
                        "name": "pcnt_nxt",
                        "isvar": True,
                        "width": "2",
                        "descr": "Push Count Next Wire",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_bfifo",
                "instance_name": "bfifo",
                "parameters": {
                    "DATA_W": "DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "write_io": (
                        "write_io",
                        [
                            "write_i: push",
                            "wwidth_i: push_width",
                            "wdata_i: rdata_i",
                            "wlevel_o: push_level",
                        ],
                    ),
                    "read_io": (
                        "read_io",
                        [
                            "read_i: pop",
                            "rwidth_i: width_i",
                            "rdata_o: wdata_o",
                            "rlevel_o: pop_level",
                        ],
                    ),
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "wrap_acc_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "$clog2(DATA_W)+1",
                    "RST_VAL": "{$clog2(DATA_W) + 1{1'b0}}",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "wrap_acc_nxt",
                    "data_o": "wrap_acc",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "pcnt_reg",
                "port_params": {
                    "clk_en_rst_s": "c_a_r",
                },
                "parameters": {
                    "DATA_W": "2",
                    "RST_VAL": "2'b0",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "data_i": "pcnt_nxt",
                    "data_o": "pcnt",
                },
            },
        ],
        "comb": {
            "code": """
            //read unpacked data from external input fifo
            read_o  = read;
            //write packed data to external output fifo
            write_o = pop;
 push_width   = wrap_i ? wrap_acc : DATA_W;
    wrap_acc_int = {1'd0, wrap_acc} + {1'd0, width_i};

    //defaults
    pop          = 1'b0;
    push         = 1'b0;
    read_o       = 1'b0;
    wrap_acc_nxt = wrap_acc;
    pcnt_nxt     = pcnt + 1'b1;

    case (pcnt)
      CALC_PUSH_WIDTH: begin  //compute push width
        if (wrap_i && (wrap_acc_int <= DATA_W)) begin
          pcnt_nxt     = pcnt;
          wrap_acc_nxt = wrap_acc_int[0+:$clog2(DATA_W)+1];
        end
      end
      WAIT_DATA: begin  //wait to read data from input fifo
        if (rready_i && (push_level >= {1'd0, push_width})) begin
          read_o = 1'b1;
        end else begin
          pcnt_nxt = POP_DATA;
        end
      end
      PUSH_DATA: begin  //push data to bit fifo
        push = 1'b1;
      end
      default: begin  //wait to pop data from bit fifo
        if ((pop_level >= {1'd0, width_i}) && wready_i) begin
          pop = 1'b1;
        end
        pcnt_nxt = WAIT_DATA;
      end
    endcase


            """,
        },
        "snippets": [
            {
                "verilog_code": r"""
              localparam CALC_PUSH_WIDTH = 2'd0;
              localparam WAIT_DATA = 2'd1;
              localparam PUSH_DATA = 2'd2;
              localparam POP_DATA = 2'd3;


                """
            }
        ],
    }

    return attributes_dict
