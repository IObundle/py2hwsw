// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

`timescale 1ns / 1ps

module dma_tb;

   // TODO review variables
   localparam PER = 10;
   localparam DATA_W = 32;

   integer fd;

   reg     clk;
   initial clk = 0;
   always #(PER / 2) clk = ~clk;

   reg                 rst;

   reg                 TIMER_ENABLE;
   reg                 TIMER_SAMPLE;
   wire [2*DATA_W-1:0] TIMER_VALUE;

   // TODO review simulation loop program
   // - [ ] write data to axistream out
   // - [ ] configure dma to write from axistream out -> axi ram
   // - [ ] wait for transfer to complete
   // - [ ] configure dma to read from axi ram -> axistream in
   // - [ ] read data from axistream in
   // - [ ] compare data read with data written

   initial begin
`ifdef VCD
      $dumpfile("timer.vcd");
      $dumpvars();
`endif
      TIMER_ENABLE = 0;
      TIMER_SAMPLE = 0;

      rst          = 1;
      // deassert hard reset
      @(posedge clk) #1 rst = 0;
      @(posedge clk) #1 TIMER_ENABLE = 1;
      @(posedge clk) #1 TIMER_SAMPLE = 1;
      @(posedge clk) #1 TIMER_SAMPLE = 0;

      //uncomment to fail the test 
      //@(posedge clk) #1;

      $write("Current time: %d; Timer value %d\n", $time(), TIMER_VALUE);
      #(1000 * PER) @(posedge clk) #1 TIMER_SAMPLE = 1;
      @(posedge clk) #1 TIMER_SAMPLE = 0;
      $write("Current time: %d; Timer value %d\n", $time(), TIMER_VALUE);

      if (TIMER_VALUE == 1003) begin
         $display("%c[1;34m", 27);
         $display("Test completed successfully.");
         $display("%c[0m", 27);
         fd = $fopen("test.log", "w");
         $fdisplay(fd, "Test passed!");
         $fclose(fd);

      end else begin
         $display("Test failed: expecting timer value 1003 but got %d", TIMER_VALUE);
         fd = $fopen("test.log", "w");
         $fdisplay(fd, "Test failed: expecting timer value 1003 but got %d", TIMER_VALUE);
         $fclose(fd);
      end

      $finish();
   end

   //instantiate dma core
   iob_dma #(
        // TODO parameter values, check AC97
        .AXI_ADDR_W(),
        .AXI_LEN_W(),
        .AXI_DATA_W(),
        .AXI_ID_W(),
        .DMA_WLEN_W(),
        .DMA_RLEN_W()
   ) dma0 (
        // clk_en_rst_s
        .clk_i(),
        .cke_i(),
        .arst_i(),
        // rst_i
        .rst_i(),
        // config_write_io
        .w_addr_i(),
        .w_length_i(),
        .w_start_transfer_i(),
        .w_max_len_i(),
        .w_remaining_data_o(),
        .w_busy_o(),
        // config_read_io
        .r_addr_i(),
        .r_length_i(),
        .r_start_transfer_i(),
        .r_max_len_i(),
        .r_remaining_data_o(),
        .r_busy_o(),
        .// axis_in_io
        .axis_in_data_i(),
        .axis_in_valid_i(),
        .axis_in_ready_o(),
        .// axis_out_io
        .axis_out_data_o(),
        .axis_out_valid_o(),
        .axis_out_ready_i(),
        .// write_ext_mem_m
        .dma_write_clk_o(),
        .dma_write_r_data_i(),
        .dma_write_r_en_o(),
        .dma_write_r_ready_i(),
        .dma_write_r_addr_o(),
        .dma_write_w_data_o(),
        .dma_write_w_ready_i(),
        .dma_write_w_addr_o(),
        .dma_write_w_en_o(),
        .// read_ext_mem_m
        .dma_read_clk_o(),
        .dma_read_r_data_i(),
        .dma_read_r_en_o(),
        .dma_read_r_ready_i(),
        .dma_read_r_addr_o(),
        .dma_read_w_data_o(),
        .dma_read_w_ready_i(),
        .dma_read_w_addr_o(),
        .dma_read_w_en_o(),
        .// axi_m
        .axi_araddr_o(),
        .axi_arprot_o(),
        .axi_arvalid_o(),
        .axi_arready_i(),
        .axi_rdata_i(),
        .axi_rresp_i(),
        .axi_rvalid_i(),
        .axi_rready_o(),
        .axi_arid_o(),
        .axi_arlen_o(),
        .axi_arsize_o(),
        .axi_arburst_o(),
        .axi_arlock_o(),
        .axi_arcache_o(),
        .axi_arqos_o(),
        .axi_rid_i(),
        .axi_rlast_i(),
        .axi_awaddr_o(),
        .axi_awprot_o(),
        .axi_awvalid_o(),
        .axi_awready_i(),
        .axi_wdata_o(),
        .axi_wstrb_o(),
        .axi_wvalid_o(),
        .axi_wready_i(),
        .axi_bresp_i(),
        .axi_bvalid_i(),
        .axi_bready_o(),
        .axi_awid_o(),
        .axi_awlen_o(),
        .axi_awsize_o(),
        .axi_awburst_o(),
        .axi_awlock_o(),
        .axi_awcache_o(),
        .axi_awqos_o(),
        .axi_wlast_o(),
        .axi_bid_i()
   );

   // TODO: 
   // - [ ] add axi ram
   // - [ ] add axistream in
   // - [ ] add axistream out

endmodule
