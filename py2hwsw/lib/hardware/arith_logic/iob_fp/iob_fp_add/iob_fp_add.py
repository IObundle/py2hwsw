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
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "EXP_W",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "NA",
                "descr": "Exponent width",
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
                "descr": "Input port",
                "signals": [
                    {
                        "name": "start_i",
                        "width": 1,
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
                "descr": "Input port",
                "signals": [
                    {
                        "name": " op_a_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "op_b_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": " op_b_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "overflow_o",
                "descr": "Overflow signal",
                "signals": [
                    {
                        "name": "overflow_o",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "underflow_o",
                "descr": "Underflow signal",
                "signals": [
                    {
                        "name": "underflow_o",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "exception_o",
                "descr": "Exception signal",
                "signals": [
                    {
                        "name": "exception_o",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "res_o",
                        "isvar": True,
                        "width": "DATA_W",
                        "descr": "Result of the operation",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "comp",
                "descr": "Comparison wire",
                "signals": [
                    {
                        "name": "comp",
                        "isvar": True,
                        "width": "1",
                        "descr": "Comparison wire",
                    },
                ],
            },
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
                "name": "A_sign_reg",
                "descr": "Sign of operand A (registered)",
                "signals": [
                    {
                        "name": "A_sign_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand A (registered)",
                    },
                ],
            },
            {
                "name": "A_Exponent_reg",
                "descr": "Exponent of operand A (registered)",
                "signals": [
                    {
                        "name": "A_Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Exponent of operand A (registered)",
                    },
                ],
            },
            {
                "name": "A_Mantissa_reg",
                "descr": "Mantissa of operand A (registered)",
                "signals": [
                    {
                        "name": "A_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Mantissa of operand A (registered)",
                    },
                ],
            },
            {
                "name": "A_Mantissa_reg",
                "descr": "Mantissa of operand A (registered)",
                "signals": [
                    {
                        "name": "A_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Mantissa of operand A (registered)",
                    },
                ],
            },
            {
                "name": "B_sign_reg",
                "descr": "Sign of operand B (registered)",
                "signals": [
                    {
                        "name": "B_sign_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand B (registered)",
                    },
                ],
            },
            {
                "name": "B_Exponent_reg",
                "descr": "Exponent of operand B (registered)",
                "signals": [
                    {
                        "name": "B_Exponent_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Exponent of operand B (registered)",
                    },
                ],
            },
            {
                "name": "B_Mantissa_reg",
                "descr": "Mantissa of operand B (registered)",
                "signals": [
                    {
                        "name": "B_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Mantissa of operand B (registered)",
                    },
                ],
            },
            {
                "name": "done_int",
                "descr": "Internal done signal",
                "signals": [
                    {
                        "name": "done_int",
                        "isvar": True,
                        "width": "1",
                        "descr": "Internal done signal",
                    },
                ],
            },
            {
                "name": "diff_Exponent",
                "descr": "Difference of Exponents",
                "signals": [
                    {
                        "name": "diff_Exponent",
                        "width": "EXP_W",
                        "descr": "Difference of Exponents",
                    },
                ],
            },
            {
                "name": "B_Mantissa_in",
                "descr": "Mantissa of operand B (input)",
                "signals": [
                    {
                        "name": "B_Mantissa_in",
                        "width": "MAN_W+STICKY_BITS",
                        "descr": "Mantissa of operand B (input)",
                    },
                ],
            },
            {
                "name": "guard_bit",
                "descr": "Guard bit for rounding",
                "signals": [
                    {
                        "name": "guard_bit",
                        "width": "1",
                        "descr": "Guard bit for rounding",
                    },
                ],
            },
            {
                "name": "round_bit",
                "descr": "Round bit for rounding",
                "signals": [
                    {
                        "name": "round_bit",
                        "width": "1",
                        "descr": "Guard bit for rounding",
                    },
                ],
            },
            {
                "name": "sticky_bit",
                "descr": "Sticky bit for rounding",
                "signals": [
                    {
                        "name": "sticky_bit",
                        "width": "1",
                        "descr": "Sticky bit for rounding",
                    },
                ],
            },
            {
                "name": "A_sign_reg2",
                "descr": "Sign of operand A (registered, second stage)",
                "signals": [
                    {
                        "name": "A_sign_reg2",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand A (registered, second stage)",
                    },
                ],
            },
            {
                "name": "A_Exponent_reg2",
                "descr": "Exponent of operand A (registered, second stage)",
                "signals": [
                    {
                        "name": "A_Exponent_reg2",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Exponent of operand A (registered, second stage)",
                    },
                ],
            },
            {
                "name": "A_Mantissa_reg2",
                "descr": "Mantissa of operand A (registered, second stage)",
                "signals": [
                    {
                        "name": "A_Mantissa_reg2",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Mantissa of operand A (registered, second stage)",
                    },
                ],
            },
            {
                "name": "B_sign_reg2",
                "descr": "Sign of operand B (registered, second stage)",
                "signals": [
                    {
                        "name": "B_sign_reg2",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand B (registered, second stage)",
                    },
                ],
            },
            {
                "name": "B_Mantissa_reg2",
                "descr": "Mantissa of operand B (registered, second stage)",
                "signals": [
                    {
                        "name": "B_Mantissa_reg2",
                        "isvar": True,
                        "width": "MAN_W",
                        "descr": "Mantissa of operand B (registered, second stage)",
                    },
                ],
            },
            {
                "name": "guard_bit_reg",
                "descr": "Guard bit for rounding (registered)",
                "signals": [
                    {
                        "name": "guard_bit_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Guard bit for rounding (registered)",
                    },
                ],
            },
            {
                "name": "round_bit_reg",
                "descr": "Round bit for rounding (registered)",
                "signals": [
                    {
                        "name": "round_bit_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Round bit for rounding (registered)",
                    },
                ],
            },
            {
                "name": "sticky_bit_reg",
                "descr": "Sticky bit for rounding (registered)",
                "signals": [
                    {
                        "name": "sticky_bit_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sticky bit for rounding (registered)",
                    },
                ],
            },
            {
                "name": "done_int2",
                "descr": "Internal done signal (second stage)",
                "signals": [
                    {
                        "name": "done_int2",
                        "isvar": True,
                        "width": "1",
                        "descr": "Internal done signal (second stage)",
                    },
                ],
            },
            {
                "name": "Temp",
                "descr": "Temporary wire for intermediate results",
                "signals": [
                    {
                        "name": "Temp",
                        "width": "MAN_W+1",
                        "descr": "Temporary wire for intermediate results",
                    },
                ],
            },
            {
                "name": "carry",
                "descr": "Carry wire for addition",
                "signals": [
                    {
                        "name": "carry",
                        "width": "1",
                        "descr": "Carry wire for addition",
                    },
                ],
            },
            {
                "name": "A_sign_reg3",
                "descr": "Sign of operand A (registered, third stage)",
                "signals": [
                    {
                        "name": "A_sign_reg3",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand A (registered, third stage)",
                    },
                ],
            },
            {
                "name": "A_Exponent_reg3",
                "descr": "Exponent of operand A (registered, third stage)",
                "signals": [
                    {
                        "name": "A_Exponent_reg3",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Exponent of operand A (registered, third stage)",
                    },
                ],
            },
            {
                "name": "Temp_reg",
                "descr": "Temporary wire for intermediate results (registered)",
                "signals": [
                    {
                        "name": "Temp_reg",
                        "isvar": True,
                        "width": "MAN_W+EXTRA",
                        "descr": "Temporary wire for intermediate results (registered)",
                    },
                ],
            },
            {
                "name": "carry_reg",
                "descr": "Carry wire for addition (registered)",
                "signals": [
                    {
                        "name": "carry_reg",
                        "isvar": True,
                        "width": "1",
                        "descr": "Carry wire for addition (registered)",
                    },
                ],
            },
            {
                "name": "done_int3",
                "descr": "Internal done signal (third stage)",
                "signals": [
                    {
                        "name": "done_int3",
                        "isvar": True,
                        "width": "1",
                        "descr": "Internal done signal (third stage)",
                    },
                ],
            },
            {
                "name": "lzc",
                "descr": "Leading zero count",
                "signals": [
                    {
                        "name": "lzc",
                        "width": "$clog2(MAN_W+EXTRA+1)",
                        "descr": "Leading zero count",
                    },
                ],
            },
            {
                "name": "Temp_Mantissa",
                "descr": "Temporary Mantissa wire",
                "signals": [
                    {
                        "name": "Temp_Mantissa",
                        "width": "MAN_W+EXTRA",
                        "descr": "Temporary Mantissa wire",
                    },
                ],
            },
            {
                "name": "exp_adjust",
                "descr": "Exponent adjustment wire",
                "signals": [
                    {
                        "name": "exp_adjust",
                        "width": "EXP_W",
                        "descr": "Exponent adjustment wire",
                    },
                ],
            },
            {
                "name": "A_sign_reg4",
                "descr": "Sign of operand A (registered, fourth stage)",
                "signals": [
                    {
                        "name": "A_sign_reg4",
                        "isvar": True,
                        "width": "1",
                        "descr": "Sign of operand A (registered, fourth stage)",
                    },
                ],
            },
            {
                "name": "exp_adjust_reg",
                "descr": "Exponent adjustment wire (registered)",
                "signals": [
                    {
                        "name": "exp_adjust_reg",
                        "isvar": True,
                        "width": "EXP_W",
                        "descr": "Exponent adjustment wire (registered)",
                    },
                ],
            },
            {
                "name": "Temp_Mantissa_reg",
                "descr": "Temporary Mantissa wire (registered)",
                "signals": [
                    {
                        "name": "Temp_Mantissa_reg",
                        "isvar": True,
                        "width": "MAN_W+EXTRA",
                        "descr": "Temporary Mantissa wire (registered)",
                    },
                ],
            },
            {
                "name": "done_int4",
                "descr": "Internal done signal (fourth stage)",
                "signals": [
                    {
                        "name": "done_int4",
                        "isvar": True,
                        "width": "1",
                        "descr": "Internal done signal (fourth stage)",
                    },
                ],
            },
            {
                "name": "Temp_Mantissa_rnd",
                "descr": "Temporary Mantissa wire for rounding",
                "signals": [
                    {
                        "name": "Temp_Mantissa_rnd",
                        "width": "MAN_W",
                        "descr": "Temporary Mantissa wire for rounding",
                    },
                ],
            },
            {
                "name": "exp_adjust_rnd",
                "descr": "Exponent adjustment wire for rounding",
                "signals": [
                    {
                        "name": "exp_adjust_rnd",
                        "width": "EXP_W",
                        "descr": "Exponent adjustment wire for rounding",
                    },
                ],
            },
            {
                "name": "Mantissa",
                "descr": "Final Mantissa wire",
                "signals": [
                    {
                        "name": "Mantissa",
                        "width": "MAN_W-1",
                        "descr": "Exponent adjustment wire for rounding",
                    },
                ],
            },
            {
                "name": "Exponent",
                "descr": "Final Exponent wire",
                "signals": [
                    {
                        "name": "Exponent",
                        "width": "EXP_W",
                        "descr": "Final Exponent wire",
                    },
                ],
            },
            {
                "name": "Sign",
                "descr": "Final Sign wire",
                "signals": [
                    {
                        "name": "Sign",
                        "width": "1",
                        "descr": "Final Sign wire",
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
                "core_name": "iob_fp_clz",
                "instance_name": "clz0",
                "parameters": {
                    "DATA_W": "MAN_W+EXTRA",
                },
                "connect": {
                    "data_i": "Temp_reg",
                    "data_o": "lzc",
                },
            },
            {
                "core_name": "iob_fp_round",
                "instance_name": "round0",
                "parameters": {
                    "DATA_W": "MAN_W",
                    "EXP_W": "EXP_W",
                },
                "connect": {
                    "exponent_i": "exp_adjust_reg",
                    "mantissa_i": "Temp_Mantissa_reg",
                    "exponent_rnd_o": "exp_adjust_rnd",
                    "mantissa_rnd_o": "Temp_Mantissa_rnd",
                },
            },
        ],
        "comb": {
            "code": """
                comp = 1'b0;
                if (op_a_i[DATA_W-2-:EXP_W] == op_b_i[DATA_W-2-:EXP_W]) begin
                    if (op_a_i[MAN_W-2:0] > op_b_i[MAN_W-2:0]) comp = 1'b1;
                end
                if (op_a_i[DATA_W-2-:EXP_W] > op_b_i[DATA_W-2-:EXP_W]) comp = 1'b1;
            """,
        },
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
localparam STICKY_BITS = 2 * BIAS - 1;
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
   fp_special #(
      .DATA_W(DATA_W),
      .EXP_W (EXP_W)
   ) special_op_b (
      .data_i(op_b_i),

      .nan_o       (op_b_nan),
      .infinite_o  (op_b_inf),
      .zero_o      (op_b_zero),
      .sub_normal_o(op_b_sub)
   );

   wire              special;
   wire [DATA_W-1:0] res_special;
   assign special = op_a_nan | op_a_inf | op_b_nan | op_b_inf;
   assign res_special = (op_a_nan | op_b_nan)? `NAN:
                                          (op_a_inf & op_b_inf)? ((op_a_i[DATA_W-1] ^ op_b_i[DATA_W-1])? `NAN:
       `INF(op_a_i[DATA_W-1])
       ) : op_b_inf ? ((op_a_i[DATA_W-1] ^ op_b_i[DATA_W-1]) ?
       `INF(~op_b_i[DATA_W-1]) :
       `INF(op_b_i[DATA_W-1])
       ) :
       `INF(op_a_i[DATA_W-1]);
`endif
    // Unpack
   //wire                     comp;
   //assign                     comp = (op_a_i[DATA_W-2 -: EXP_W] >= op_b_i[DATA_W-2 -: EXP_W])? 1'b1 : 1'b0;
   assign A_Mantissa = comp ? {1'b1, op_a_i[MAN_W-2:0]} : {1'b1, op_b_i[MAN_W-2:0]};
   assign A_Exponent = comp ? op_a_i[DATA_W-2-:EXP_W] : op_b_i[DATA_W-2-:EXP_W];
   assign A_sign     = comp ? op_a_i : op_b_i[DATA_W-1];
   assign B_Mantissa = comp ? {1'b1, op_b_i[MAN_W-2:0]} : {1'b1, op_a_i[MAN_W-2:0]};
   assign B_Exponent = comp ? op_b_i[DATA_W-2-:EXP_W] : op_a_i[DATA_W-2-:EXP_W];
   assign B_sign     = comp ? op_b_i : op_a_i[DATA_W-1];
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
   assign diff_Exponent = A_Exponent_reg - B_Exponent_reg;
   assign B_Mantissa_in = {B_Mantissa_reg, {STICKY_BITS{1'b0}}} >> diff_Exponent;
   assign guard_bit  = B_Mantissa_in[STICKY_BITS-1];
   assign round_bit  = B_Mantissa_in[STICKY_BITS-2];
   assign sticky_bit = |B_Mantissa_in[STICKY_BITS-3:0];
   always @(posedge clk_i) begin
      if (rst_i) begin
         A_sign_reg2     <= 1'b0;
         A_Exponent_reg2 <= {EXP_W{1'b0}};
         A_Mantissa_reg2 <= {MAN_W{1'b0}};

         B_sign_reg2     <= 1'b0;
         B_Mantissa_reg2 <= {MAN_W{1'b0}};

         guard_bit_reg   <= 1'b0;
         round_bit_reg   <= 1'b0;
         sticky_bit_reg  <= 1'b0;

         done_int2       <= 1'b0;
      end else begin
         A_sign_reg2     <= A_sign_reg;
         A_Exponent_reg2 <= A_Exponent_reg;
         A_Mantissa_reg2 <= A_Mantissa_reg;

         B_sign_reg2     <= B_sign_reg;
         B_Mantissa_reg2 <= B_Mantissa_in[STICKY_BITS+:MAN_W];

         guard_bit_reg   <= guard_bit;
         round_bit_reg   <= round_bit;
         sticky_bit_reg  <= sticky_bit;

         done_int2       <= done_int;
      end
   end
   assign           Temp = (A_sign_reg2 ^ B_sign_reg2)? A_Mantissa_reg2 - B_Mantissa_reg2 : A_Mantissa_reg2 + B_Mantissa_reg2;
   assign carry = Temp[MAN_W];
   always @(posedge clk_i) begin
      if (rst_i) begin
         A_sign_reg3     <= 1'b0;
         A_Exponent_reg3 <= {EXP_W{1'b0}};

         Temp_reg        <= {(MAN_W + EXTRA) {1'b0}};
         carry_reg       <= 1'b0;

         done_int3       <= 1'b0;
      end else begin
         A_sign_reg3     <= A_sign_reg2;
         A_Exponent_reg3 <= A_Exponent_reg2;

         Temp_reg        <= {Temp[MAN_W-1:0], guard_bit_reg, round_bit_reg, sticky_bit_reg};
         carry_reg       <= carry;

         done_int3       <= done_int2;
      end
   end
   assign Temp_Mantissa = carry_reg ? {1'b1, Temp_reg[MAN_W+EXTRA-1:1]} : Temp_reg << lzc;
   assign exp_adjust = carry_reg ? A_Exponent_reg3 + 1'b1 : A_Exponent_reg3 - {{EXTRA{1'b0}}, lzc};
   always @(posedge clk_i) begin
      if (rst_i) begin
         A_sign_reg4       <= 1'b0;

         exp_adjust_reg    <= {EXP_W{1'b0}};
         Temp_Mantissa_reg <= {(MAN_W + EXTRA) {1'b0}};

         done_int4         <= 1'b0;
      end else begin
         A_sign_reg4       <= A_sign_reg3;

         exp_adjust_reg    <= exp_adjust;
         Temp_Mantissa_reg <= {Temp_Mantissa[MAN_W+EXTRA-1:1], Temp_Mantissa[0] | Temp_reg[0]};

         done_int4         <= done_int3;
      end
   end
   assign Mantissa = Temp_Mantissa_rnd[MAN_W-2:0];
   assign Exponent = exp_adjust_rnd;
   assign Sign     = A_sign_reg4;
`ifdef SPECIAL_CASES
   wire [DATA_W-1:0] res_in;
   wire              done_in;
   assign res_in  = special ? res_special : {Sign, Exponent, Mantissa};
   assign done_in = special ? start_i : done_int4;
`else
   wire [DATA_W-1:0] res_in;
   wire              done_in;
   assign res_in  = {Sign, Exponent, Mantissa};
   assign done_in = done_int4;
`endif
    // pipeline stage 5
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
