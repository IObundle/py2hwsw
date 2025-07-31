# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": 32,
                "min": "NA",
                "max": "NA",
                "descr": "Width of the data in bits",
            },
            {
                "name": "EXP_W",
                "type": "P",
                "val": 8,
                "min": "NA",
                "max": "NA",
                "descr": "Width of the exponent in bits",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                    "params": "r",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "start_i",
                "descr": "start signal for the multiplier",
                "signals": [
                    {
                        "name": "start_i",
                        "width": "1",
                        "descr": "Start signal for the multiplier",
                    },
                ],
            },
            {
                "name": "done_o",
                "descr": "done signal for the multiplier",
                "signals": [
                    {
                        "name": "done_o",
                        "isvar": True,
                        "width": "1",
                        "descr": "Done signal for the multiplier",
                    },
                ],
            },
            {
                "name": "op_a_i",
                "descr": "Input operand A for the multiplier",
                "signals": [
                    {
                        "name": "op_a_i",
                        "width": "DATA_W",
                        "descr": "Input operand A for the multiplier",
                    },
                ],
            },
            {
                "name": "op_b_i",
                "descr": "Input operand B for the multiplier",
                "signals": [
                    {
                        "name": "op_b_i",
                        "width": "DATA_W",
                        "descr": "Input operand B for the multiplier",
                    },
                ],
            },
            {
                "name": "overflow_o",
                "descr": "Overflow signal for the multiplier",
                "signals": [
                    {
                        "name": "overflow_o",
                        "width": "1",
                        "descr": "Overflow signal for the multiplier",
                    },
                ],
            },
            {
                "name": "underflow_o",
                "descr": "Underflow signal for the multiplier",
                "signals": [
                    {
                        "name": "underflow_o",
                        "width": "1",
                        "descr": "Underflow signal for the multiplier",
                    },
                ],
            },
            {
                "name": "exception_o",
                "descr": "Exception signal for the multiplier",
                "signals": [
                    {
                        "name": "exception_o",
                        "width": "1",
                        "descr": "Exception signal for the multiplier",
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Result output of the multiplier",
                "signals": [
                    {
                        "name": "res_o",
                        "isvar": True,
                        "width": "DATA_W",
                        "descr": "Result output of the multiplier",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "A_Mantissa",
                "descr": "Mantissa of operand A",
                "signals": [
                    {
                        "name": "A_Mantissa",
                        "width": "MAN_W",
                        "descr": "Mantissa of operand A",
                    },
                ],
            },
            {
                "name": "A_Exponent",
                "descr": "Exponent of operand A",
                "signals": [
                    {
                        "name": "A_Exponent",
                        "width": "EXP_W",
                        "descr": "Exponent of operand A",
                    },
                ],
            },
            {
                "name": "A_sign",
                "descr": "Sign of operand A",
                "signals": [
                    {
                        "name": "A_sign",
                        "width": "1",
                        "descr": "Sign of operand A",
                    },
                ],
            },
            {
                "name": "B_Mantissa",
                "descr": "Mantissa of operand B",
                "signals": [
                    {
                        "name": "B_Mantissa",
                        "width": "MAN_W",
                        "descr": "Mantissa of operand B",
                    },
                ],
            },
            {
                "name": "B_Exponent",
                "descr": "Exponent of operand B",
                "signals": [
                    {
                        "name": "B_Exponent",
                        "width": "EXP_W",
                        "descr": "Exponent of operand B",
                    },
                ],
            },
            {
                "name": "B_sign",
                "descr": "Sign of operand B",
                "signals": [
                    {
                        "name": "B_sign",
                        "width": "1",
                        "descr": "Sign of operand B",
                    },
                ],
            },
            {
                "name": "Temp_sign",
                "descr": "Temporary sign for the multiplication result",
                "signals": [
                    {
                        "name": "Temp_sign",
                        "width": "1",
                        "descr": "Temporary sign for the multiplication result",
                    },
                ],
            },
            {
                "name": "Temp_Exponent",
                "descr": "Temporary exponent for the multiplication result",
                "signals": [
                    {
                        "name": "Temp_Exponent",
                        "width": "EXP_W",
                        "descr": "Temporary exponent for the multiplication result",
                    },
                ],
            },
            {
                "name": "Temp_Mantissa",
                "descr": "Temporary mantissa for the multiplication result",
                "signals": [
                    {
                        "name": "Temp_Mantissa",
                        "width": "2*MAN_W",
                        "descr": "Temporary mantissa for the multiplication result",
                    },
                ],
            },
            {
                "name": "Mantissa_int",
                "descr": "Intermediate mantissa for the multiplication result",
                "signals": [
                    {
                        "name": "Mantissa_int",
                        "width": "MAN_W+EXTRA",
                        "descr": "Intermediate mantissa for the multiplication result",
                    },
                ],
            },
            {
                "name": "Exponent_int",
                "descr": "Intermediate exponent for the multiplication result",
                "signals": [
                    {
                        "name": "Exponent_int",
                        "width": "EXP_W",
                        "descr": "Intermediate exponent for the multiplication result",
                    },
                ],
            },
            {
                "name": "Mantissa_rnd",
                "descr": "Rounded mantissa for the multiplication result",
                "signals": [
                    {
                        "name": "Mantissa_rnd",
                        "width": "MAN_W",
                        "descr": "Rounded mantissa for the multiplication result",
                    },
                ],
            },
            {
                "name": "Exponent_rnd",
                "descr": "Rounded exponent for the multiplication result",
                "signals": [
                    {
                        "name": "Exponent_rnd",
                        "width": "EXP_W",
                        "descr": "Rounded exponent for the multiplication result",
                    },
                ],
            },
            {
                "name": "Mantissa",
                "descr": "Final mantissa for the multiplication result",
                "signals": [
                    {
                        "name": "Mantissa",
                        "width": "MAN_W-1",
                        "descr": "Final mantissa for the multiplication result",
                    },
                ],
            },
            {
                "name": "Exponent",
                "descr": "Final exponent for the multiplication result",
                "signals": [
                    {
                        "name": "Exponent",
                        "width": "EXP_W",
                        "descr": "Final exponent for the multiplication result",
                    },
                ],
            },
            {
                "name": "Sign",
                "descr": "Final sign for the multiplication result",
                "signals": [
                    {
                        "name": "Sign",
                        "width": "1",
                        "descr": "Final sign for the multiplication result",
                    },
                ],
            },
            {
                "name": "A_sign_reg",
                "descr": "Register for the sign of operand A",
                "signals": [
                    {
                        "name": "A_sign_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Register for the sign of operand A",
                    },
                ],
            },
            {
                "name": "A_Exponent_reg",
                "descr": "Register for the exponent of operand A",
                "signals": [
                    {
                        "name": "A_Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Register for the exponent of operand A",
                    },
                ],
            },
            {
                "name": "A_Mantissa_reg",
                "descr": "Register for the mantissa of operand A",
                "signals": [
                    {
                        "name": "A_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Register for the mantissa of operand A",
                    },
                ],
            },
            {
                "name": "B_sign_reg",
                "descr": "Register for the sign of operand B",
                "signals": [
                    {
                        "name": "B_sign_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Register for the sign of operand B",
                    },
                ],
            },
            {
                "name": "B_Exponent_reg",
                "descr": "Register for the exponent of operand B",
                "signals": [
                    {
                        "name": "B_Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Register for the exponent of operand B",
                    },
                ],
            },
            {
                "name": "B_Mantissa_reg",
                "descr": "Register for the mantissa of operand B",
                "signals": [
                    {
                        "name": "B_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Register for the mantissa of operand B",
                    },
                ],
            },
            {
                "name": "done_int",
                "descr": "Register for the mantissa of operand B",
                "signals": [
                    {
                        "name": "done_int",
                        "isvar": True,
                        "width": "1",
                        "descr": "Done signal for the internal operations",
                    },
                ],
            },
            {
                "name": "Temp_sign_reg",
                "descr": "Register for the temporary sign of the multiplication result",
                "signals": [
                    {
                        "name": "Temp_sign_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Register for the temporary sign of the multiplication result",
                    },
                ],
            },
            {
                "name": "Temp_Exponent_reg",
                "descr": "Register for the temporary exponent of the multiplication result",
                "signals": [
                    {
                        "name": "Temp_Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Register for the temporary exponent of the multiplication result",
                    },
                ],
            },
            {
                "name": "Temp_Mantissa_reg",
                "descr": "Register for the temporary mantissa of the multiplication result",
                "signals": [
                    {
                        "name": "Temp_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W+EXTRA+1",
                        "descr": "Register for the temporary mantissa of the multiplication result",
                    },
                ],
            },
            {
                "name": "done_int2",
                "descr": "Register for the done signal of the internal operations",
                "signals": [
                    {
                        "name": "done_int2",
                        "isvar": True,
                        "width": "1",
                        "descr": "Done signal for the internal operations",
                    },
                ],
            },
            {
                "name": "Temp_sign_reg2",
                "descr": "Register for the temporary sign of the multiplication result",
                "signals": [
                    {
                        "name": "Temp_sign_reg2",
                        "isvar": True,
                        "width": "1",
                        "descr": "Register for the temporary sign of the multiplication result",
                    },
                ],
            },
            {
                "name": "Exponent_reg",
                "descr": "Register for the final exponent of the multiplication result",
                "signals": [
                    {
                        "name": "Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Register for the final exponent of the multiplication result",
                    },
                ],
            },
            {
                "name": "Mantissa_reg",
                "descr": "Register for the final mantissa of the multiplication result",
                "signals": [
                    {
                        "name": "Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W+EXTRA",
                        "descr": "Register for the final mantissa of the multiplication result",
                    },
                ],
            },
            {
                "name": "done_int3",
                "descr": "Register for the done signal of the internal operations",
                "signals": [
                    {
                        "name": "done_int3",
                        "isvar": True,
                        "width": "1",
                        "descr": "Done signal for the internal operations",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_fp_special",
                "instantiate": False,
            },
            {
                "core_name": "iob_fp_round",
                "instance_name": "round0",
                "parameters": {
                    "DATA_W": "MAN_W",
                    "EXP_W": "EXP_W",
                },
                "connect": {
                    "exponent_i": "Exponent_reg",
                    "mantissa_i": "Mantissa_reg",
                    "exponent_rnd_o": "Exponent_rnd",
                    "mantissa_rnd_o": "Mantissa_rnd",
                },
            },
        ],
        "snippets": [
            {
                "verilog_code": r"""
                // Canonical NAN
`define NAN {1'b0, {EXP_W{1'b1}}, 1'b1, {(DATA_W-EXP_W-2){1'b0}}}

// Infinite
`define INF(SIGN) {SIGN, {EXP_W{1'b1}}, {(DATA_W-EXP_W-1){1'b0}}}
   localparam MAN_W = DATA_W - EXP_W;
   localparam BIAS = 2 ** (EXP_W - 1) - 1;
   localparam EXTRA = 3;
      // Special cases
`ifdef SPECIAL_CASES
   wire op_a_nan, op_a_inf, op_a_zero, op_a_sub;
   iob_fp_special #(
      .DATA_W(DATA_W),
      .EXP_W (EXP_W)
   ) special_op_a (
      .data_i(op_a_i),

      .nan_o       (op_a_nan),
      .infinite_o  (op_a_inf),
      .zero_o      (op_a_zero),
      .sub_normal_o(op_a_sub)
   );

   wire op_b_nan, op_b_inf, op_b_zero, op_b_sub;
   iob_fp_special #(
      .DATA_W(DATA_W),
      .EXP_W (EXP_W)
   ) special_op_b (
      .data_i(op_b_i),

      .nan_o       (op_b_nan),
      .infinite_o  (op_b_inf),
      .zero_o      (op_b_zero),
      .sub_normal_o(op_b_sub)
   );

   wire special;
   assign special = op_a_nan | op_a_inf | op_b_nan | op_b_inf;
   wire [DATA_W-1:0] res_special;
   assign  res_special = (op_a_nan | op_b_nan)? `NAN:
                                          (op_a_inf & op_b_inf)? `NAN:
                                        (op_a_zero | op_b_zero)? `NAN:
                                                                 `INF(
           op_b_i[DATA_W-1] ^ op_b_i[DATA_W-1]);
`endif
   assign A_Mantissa = {1'b1, op_a_i[MAN_W-2:0]};
   assign A_Exponent = op_a_i[DATA_W-2-:EXP_W];
   assign A_sign = op_a_i[DATA_W-1];
   assign B_Mantissa = {1'b1, op_b_i[MAN_W-2:0]};
   assign B_Exponent = op_b_i[DATA_W-2-:EXP_W];
   assign B_sign = op_b_i[DATA_W-1];
   always @(posedge clk_i) begin
      if (rst_i) begin
         A_sign_reg     <= 1'b0;
         A_Exponent_reg <= {EXP_W{1'b0}};
         A_Mantissa_reg <= {MAN_W{1'b0}};

         B_sign_reg     <= 1'b0;
         B_Exponent_reg <= {EXP_W{1'b0}};
         B_Mantissa_reg <= {MAN_W{1'b0}};

         done_int       <= 1'b0;
      end else begin
         A_sign_reg     <= A_sign;
         A_Exponent_reg <= A_Exponent;
         A_Mantissa_reg <= A_Mantissa;

         B_sign_reg     <= B_sign;
         B_Exponent_reg <= B_Exponent;
         B_Mantissa_reg <= B_Mantissa;

         done_int       <= start_i;
      end
   end
   assign Temp_sign     = A_sign_reg ^ B_sign_reg;
   assign Temp_Exponent = A_Exponent_reg + B_Exponent_reg - BIAS;
   assign Temp_Mantissa = A_Mantissa_reg * B_Mantissa_reg;
   always @(posedge clk_i) begin
      if (rst_i) begin
         Temp_sign_reg     <= 1'b0;
         Temp_Exponent_reg <= {EXP_W{1'b0}};
         Temp_Mantissa_reg <= {(MAN_W + EXTRA + 1) {1'b0}};

         done_int2         <= 1'b0;
      end else begin
         Temp_sign_reg     <= Temp_sign;
         Temp_Exponent_reg <= Temp_Exponent;
         Temp_Mantissa_reg <= Temp_Mantissa[2*MAN_W-1-:MAN_W+EXTRA+1];

         done_int2         <= done_int;
      end
   end
   assign   Mantissa_int = Temp_Mantissa_reg[MAN_W+EXTRA]? Temp_Mantissa_reg[MAN_W+EXTRA:1] : Temp_Mantissa_reg[MAN_W+EXTRA-1:0];
   assign         Exponent_int = Temp_Mantissa_reg[MAN_W+EXTRA]? Temp_Exponent_reg + 1'b1 : Temp_Exponent_reg;
   always @(posedge clk_i) begin
      if (rst_i) begin
         Temp_sign_reg2 <= 1'b0;

         Exponent_reg   <= {EXP_W{1'b0}};
         Mantissa_reg   <= {(MAN_W + EXTRA) {1'b0}};

         done_int3      <= 1'b0;
      end else begin
         Temp_sign_reg2 <= Temp_sign_reg;

         Exponent_reg   <= Exponent_int;
         Mantissa_reg   <= {Mantissa_int[MAN_W+EXTRA-1:1], Mantissa_int[0] | Temp_Mantissa_reg[0]};

         done_int3      <= done_int2;
      end
   end
   assign Mantissa = Mantissa_rnd[MAN_W-2:0];
   assign Exponent = Exponent_rnd;
   assign Sign     = Temp_sign_reg2;
`ifdef SPECIAL_CASES
   wire [DATA_W-1:0] res_in;
   wire              done_in;
   assign res_in  = special ? res_special : {Sign, Exponent, Mantissa};
   assign done_in = special ? start_i : done_int3;
`else
   wire [DATA_W-1:0] res_in;
   wire              done_in;
   assign res_in  = {Sign, Exponent, Mantissa};
   assign done_in = done_int3;
`endif   
   // pipeline stage 4
   always @(posedge clk_i) begin
      if (rst_i) begin
         res_o  <= {DATA_W{1'b0}};
         done_o <= 1'b0;
      end else begin
         res_o  <= res_in;
         done_o <= done_in;
      end
   end
   // Not implemented yet!
   assign overflow_o  = 1'b0;
   assign underflow_o = 1'b0;
   assign exception_o = 1'b0;


                """
            }
        ],
    }

    return attributes_dict
