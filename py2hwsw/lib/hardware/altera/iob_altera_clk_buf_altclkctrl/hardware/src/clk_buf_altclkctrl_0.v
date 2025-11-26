// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

//altclkctrl CBX_SINGLE_OUTPUT_FILE="ON" CLOCK_TYPE="Global Clock" DEVICE_FAMILY="Cyclone V" USE_GLITCH_FREE_SWITCH_OVER_IMPLEMENTATION="OFF" ena inclk outclk
//VERSION_BEGIN 18.0 cbx_altclkbuf 2018:04:18:06:50:44:SJ cbx_cycloneii 2018:04:18:06:50:44:SJ cbx_lpm_add_sub 2018:04:18:06:50:44:SJ cbx_lpm_compare 2018:04:18:06:50:44:SJ cbx_lpm_decode 2018:04:18:06:50:44:SJ cbx_lpm_mux 2018:04:18:06:50:44:SJ cbx_mgl 2018:04:18:07:37:08:SJ cbx_nadder 2018:04:18:06:50:44:SJ cbx_stratix 2018:04:18:06:50:44:SJ cbx_stratixii 2018:04:18:06:50:44:SJ cbx_stratixiii 2018:04:18:06:50:44:SJ cbx_stratixv 2018:04:18:06:50:44:SJ  VERSION_END
// synthesis VERILOG_INPUT_VERSION VERILOG_2001
// altera message_off 10463




//synthesis_resources = cyclonev_clkena 1 
//synopsys translate_off
`timescale 1 ps / 1 ps
//synopsys translate_on
module clk_buf_altclkctrl_0_sub (
   ena,
   inclk,
   outclk
)  /* synthesis synthesis_clearbox=1 */;
   input ena;
   input [3:0] inclk;
   output outclk;
`ifndef ALTERA_RESERVED_QIS
   // synopsys translate_off
`endif
   tri1       ena;
   tri0 [3:0] inclk;
`ifndef ALTERA_RESERVED_QIS
   // synopsys translate_on
`endif

   wire       wire_sd1_outclk;
   wire [1:0] clkselect;

   cyclonev_clkena sd1 (
      .ena   (ena),
      .enaout(),
      .inclk (inclk[0]),
      .outclk(wire_sd1_outclk)
   );
   // defparam sd1.clock_type = "Global Clock", sd1.ena_register_mode = "always enabled",
   //     sd1.lpm_type = "cyclonev_clkena";
   assign clkselect = {2{1'b0}}, outclk = wire_sd1_outclk;
endmodule  //clk_buf_altclkctrl_0_sub
//VALID FILE


// synopsys translate_off
`timescale 1 ps / 1 ps
// synopsys translate_on
module clk_buf_altclkctrl_0 (
   inclk,
   outclk
);

   input inclk;
   output outclk;

   wire       sub_wire0;
   wire       outclk;
   wire       sub_wire1;
   wire       sub_wire2;
   wire [3:0] sub_wire3;
   wire [2:0] sub_wire4;

   assign outclk         = sub_wire0;
   assign sub_wire1      = 1'h1;
   assign sub_wire2      = inclk;
   assign sub_wire3[3:0] = {sub_wire4, sub_wire2};
   assign sub_wire4[2:0] = 3'h0;

   clk_buf_altclkctrl_0_sub clk_buf_altclkctrl_0_sub_component (
      .ena   (sub_wire1),
      .inclk (sub_wire3),
      .outclk(sub_wire0)
   );

endmodule
