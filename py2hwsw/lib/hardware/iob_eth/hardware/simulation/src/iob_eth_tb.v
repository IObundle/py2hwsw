`timescale 1ns / 1ps

`include "iob_utils.vh"
`include "iob_eth_defines.vh"

module iob_eth_tb;
  parameter integer CLK_PER = 10;
  parameter integer ADDR_W = `IOB_ETH_CSRS_ADDR_W;
  parameter integer DATA_W = 32;
  parameter integer AXI_ID_W = 1;
  // Fit at least two frames in memory (2 * 2^9 words * 4 byte-word)
  // 12 is the minimum supported by axi_interconnect
  parameter integer AXI_ADDR_W = 12;
  parameter integer AXI_DATA_W = 32;
  parameter integer AXI_LEN_W = 8;
  parameter integer MEM_ADDR_OFFSET = `IOB_ETH_MEM_ADDR_OFFSET;
  parameter integer PHY_RST_CNT = `IOB_ETH_PHY_RST_CNT;
  parameter integer BD_NUM_LOG2 = `IOB_ETH_BD_NUM_LOG2;
  parameter integer BUFFER_W = `IOB_ETH_BUFFER_W;

  // CPU SIDE
  reg                   arst;
  reg                   clk = 0;
  wire                  cke = 1'b1;

  //IOb-SoC ethernet
  reg                   iob_valid_i;
  reg  [    ADDR_W-1:0] iob_addr_i;
  reg  [    DATA_W-1:0] iob_wdata_i;
  reg  [           3:0] iob_wstrb_i;
  wire [    DATA_W-1:0] iob_rdata_o;
  wire                  iob_ready_o;
  wire                  iob_rvalid_o;

  // Testbench memory control
  reg  [AXI_ADDR_W-1:0] tb_addr = {AXI_ADDR_W{1'b0}};
  reg                   tb_awvalid = 1'b0;
  wire                  tb_awready;
  reg                   tb_arvalid = 1'b0;
  wire                  tb_arready;
  reg  [AXI_DATA_W-1:0] tb_wdata = {AXI_DATA_W{1'b0}};
  reg                   tb_wvalid = 1'b0;
  wire                  tb_wready;
  wire [AXI_DATA_W-1:0] tb_rdata;
  wire                  tb_rvalid;
  reg                   tb_rready = 1'b0;

  iob_eth_mem_wrapper #(
      .ADDR_W(ADDR_W),
      .DATA_W(DATA_W),
      .AXI_ID_W(AXI_ID_W),
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_LEN_W(AXI_LEN_W),
      .MEM_ADDR_OFFSET(MEM_ADDR_OFFSET),
      .PHY_RST_CNT(PHY_RST_CNT),
      .BD_NUM_LOG2(BD_NUM_LOG2),
      .BUFFER_W(BUFFER_W)
  ) mem_wrapper (
      // Eth IOb csrs interface
      `include "iob_s_s_portmap.vs"

      // Testbench memory control
      .tb_addr(tb_addr),
      .tb_awvalid(tb_awvalid),
      .tb_awready(tb_awready),
      .tb_arvalid(tb_arvalid),
      .tb_arready(tb_arready),
      .tb_wdata(tb_wdata),
      .tb_wvalid(tb_wvalid),
      .tb_wready(tb_wready),
      .tb_rdata(tb_rdata),
      .tb_rvalid(tb_rvalid),
      .tb_rready(tb_rready),

      `include "clk_en_rst_s_portmap.vs"
  );

  // Drive clock
  always #(CLK_PER / 2) clk = ~clk;

  // Testbench vars
  integer            i;
  reg     [    15:0] frame_size;
  reg     [1514-1:0] frame_data;
  reg     [  32-1:0] frame_word;
  reg                rval;
  integer            fd;

  //
  // Main program
  //
  initial begin

    //Frame header
    frame_data = 'h66_55_44_33_22_11;
    frame_data = frame_data | ('hFF_EE_DD_CC_BB_AA) << (6 * 8);
    frame_data = frame_data | ('h06_00) << (12 * 8);

    // Frame payload
    frame_data = frame_data | ('h16_15_14_13_12_11_10_09_08_07_06_05_04_03_02_01) << (14 * 8);
    frame_data = frame_data | ('h32_31_30_29_28_27_26_25_24_23_22_21_20_19_18_17) << (30 * 8);
    frame_data = frame_data | ('h48_47_46_45_44_43_42_41_40_39_38_37_36_35_34_33) << (46 * 8);
    frame_data = frame_data | ('h64_63_62_61_60_59_58_57_56_55_54_53_52_51_50_49) << (62 * 8);
    frame_data = frame_data | ('h66_65) << (78 * 8);

    // Frame size (header + payload)
    frame_size = 14 + 66;

`ifdef VCD
    $dumpfile("iob_eth.vcd");
    $dumpvars;
`endif

    //init cpu bus signals
    iob_valid_i = 0;
    iob_wstrb_i = 0;

    // Reset signal
    arst = 0;
    #100 arst = 1;
    #1_000 arst = 0;
    #100;
    @(posedge clk) #1;

    reset_tb_memory();

    // configure eth core
    cpu_initeth();

    $display("Writing test frame to memory...");
    $write("\nTest frame data: ");
    for (i = 0; i < frame_size; i = i + 4) begin
      if (i % 16 == 0) $display("");
      tb_mem_write(i, frame_data[i*8+:32]);
      $write("%02x %02x %02x %02x ", frame_data[i*8+:8], frame_data[i*8+8+:8],
             frame_data[i*8+16+:8], frame_data[i*8+24+:8]);
    end

    $display("\n\nWaiting for PHY reset...");
    wait_phy_rst();

    $display("Starting ethernet frame transmission via DMA...");

    // set frame size
    eth_set_payload_size(0, frame_size);
    // Set ready bit
    eth_set_ready(0, 1);

    $display("Verifying received frame via DMA...");

    // wait until data received
    rval = 0;
    while (!rval) eth_rx_ready(64, rval);

    // Check bad CRC
    eth_bad_crc(64, rval);
    if (rval) $display("Bad CRC!");

    $write("\nReceived frame data: ");
    for (i = 0; i < frame_size; i = i + 4) begin
      if (i % 16 == 0) $display("");
      tb_mem_read(i, frame_word);
      $write("%02x %02x %02x %02x ", frame_data[i*8+:8], frame_data[i*8+8+:8],
             frame_data[i*8+16+:8], frame_data[i*8+24+:8]);
      if (frame_word != frame_data[i*8+:32]) begin
        $display("\nERROR: Received frame data mismatch!");
        $finish;
      end
    end

    $display("\n%c[1;34m", 27);
    $display("Test completed successfully.");
    $display("%c[0m", 27);
    fd = $fopen("test.log", "w");
    $fdisplay(fd, "Test passed!");
    $fclose(fd);
    $finish;
  end

  task static cpu_initeth;
    begin
      $display("Initializing ethernet core...");
      eth_reset_bd_memory();

      /**** Configure receiver *****/
      // set frame pointer (starting at half memory)
      eth_set_ptr(64, 1 << 9);

      // Mark empty; Set as last descriptor; Enable interrupt.
      eth_set_empty(64, 1);
      eth_set_wr(64, 1);
      eth_set_interrupt(64, 1);

      // Enable reception
      eth_receive(1);

      /**** Configure transmitter *****/
      // set frame pointer (starting at beginning of memory)
      eth_set_ptr(0, 0);

      // Enable CRC and PAD; Set as last descriptor; Enable interrupt.
      eth_set_crc(0, 1);
      eth_set_pad(0, 1);
      eth_set_wr(0, 1);
      eth_set_interrupt(0, 1);

      // enable transmission
      eth_send(1);
    end
  endtask

  //
  // Testbench memory control
  //

  task static reset_tb_memory;
    begin
      integer i;
      $display("Resetting AXI memory...");
      // Only reset first 2^10 addresses. The rest is not used.
      for (i = 0; i < 1 << 10; i = i + 1) begin
        tb_mem_write(i, 0);
      end
    end
  endtask

  task static tb_mem_write(input reg [AXI_ADDR_W-1:0] addr, input reg [AXI_DATA_W-1:0] data);
    begin
      @(posedge clk) #1 tb_awvalid = 1;  //sync and assign
      tb_addr = addr;
      #1 while (!tb_awready) #1;
      @(posedge clk) #1;
      tb_awvalid = 0;
      tb_addr = 0;

      tb_wvalid = 1;
      tb_wdata = data;
      #1 while (!tb_wready) #1;
      @(posedge clk) #1;
      tb_wvalid = 0;
      tb_wdata  = 0;

    end
  endtask

  task static tb_mem_read(input reg [AXI_ADDR_W-1:0] addr, output reg [AXI_DATA_W-1:0] data);
    begin
      @(posedge clk) #1 tb_arvalid = 1;  //sync and assign
      tb_addr = addr;
      #1 while (!tb_arready) #1;
      tb_arvalid = 0;
      tb_addr = 0;

      #1 while (!tb_rvalid) #1;
      data = tb_rdata;
      tb_rready = 1;
      #1;
    end
  endtask

  `include "iob_eth_defines_tasks.vs"

  `include "iob_eth_csrs_emb_tb.vs"

  `include "iob_tasks.vs"

endmodule
