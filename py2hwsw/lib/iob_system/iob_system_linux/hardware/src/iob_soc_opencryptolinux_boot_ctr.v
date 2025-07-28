`timescale 1 ns / 1 ps

module iob_soc_opencryptolinux_boot_ctr #(
    parameter ADDR_W = 0,
    parameter DATA_W = 0,
    parameter STRB_W = (DATA_W / 8)
) (
    output wire boot,
    output wire cpu_reset,

    input  wire [     1-1:0] iob_valid_i,
    input  wire [ADDR_W-1:0] iob_addr_i,
    input  wire [DATA_W-1:0] iob_wdata_i,
    input  wire [STRB_W-1:0] iob_wstrb_i,
    output wire [     1-1:0] iob_rvalid_o,
    output wire [DATA_W-1:0] iob_rdata_o,
    output wire [     1-1:0] iob_ready_o,

    `include "clk_en_rst_s_port.vs"
);

  //boot register: (1) load bootloader to sram and run it: (0) run program
  wire boot_wr;
  reg  boot_nxt;
  //create CPU reset pulse
  wire cpu_reset_req;
  wire rst_sync;

  assign boot_wr = iob_valid_i & (|iob_wstrb_i);
  assign cpu_reset_req = (iob_valid_i & (|iob_wstrb_i) & iob_wdata_i[1]) | rst_sync;

  // IOb-Bus
  assign iob_rvalid_o = 1'b0; // has no read registers
  assign iob_rdata_o = {DATA_W{1'b0}};
  assign iob_ready_o = 1'b1;

  iob_reg_re #(
      .DATA_W (1),
      .RST_VAL(1)
  ) bootnxt (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),
      .rst_i (1'b0),
      .en_i  (boot_wr),
      .data_i(iob_wdata_i[0]),
      .data_o(boot_nxt)
  );
  iob_reg_r #(
      .DATA_W (1),
      .RST_VAL(1)
  ) bootreg (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .cke_i (cke_i),
      .rst_i (1'b0),
      .data_i(boot_nxt),
      .data_o(boot)
  );
  iob_reset_sync sync_reset (
      .clk_i (clk_i),
      .arst_i(arst_i),
      .arst_o(rst_sync)
  );
  iob_pulse_gen #(
      .START   (0),
      .DURATION(100)
  ) reset_pulse (
      .clk_i  (clk_i),
      .arst_i (arst_i),
      .cke_i  (cke_i),
      .start_i(cpu_reset_req),
      .pulse_o(cpu_reset)
  );

endmodule
