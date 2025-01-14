`timescale 1ns / 1ps

`include "iob_eth_defines.vh"

module iob_eth_driver_tb #(
    `include "iob_eth_params.vs"
) (
    output [1-1:0] iob_valid_o,
    output [ADDR_W-1:0] iob_addr_o,
    output [DATA_W-1:0] iob_wdata_o,
    output [(DATA_W/8)-1:0] iob_wstrb_o,
    input [1-1:0] iob_rvalid_i,
    input [DATA_W-1:0] iob_rdata_i,
    input [1-1:0] iob_ready_i,
    input clk_i
);

  wire                             clk = clk_i;

  //IOb-SoC ethernet
  reg                              iob_valid_i;
  reg  [`IOB_ETH_CSRS_ADDR_W-1:0] iob_addr_i;
  reg  [               DATA_W-1:0] iob_wdata_i;
  reg  [                      3:0] iob_wstrb_i;
  wire [               DATA_W-1:0] iob_rdata_o;
  wire                             iob_ready_o;
  wire                             iob_rvalid_o;

  // Assign IOs to local wires
  // CPU req
  assign iob_valid_o  = iob_valid_i;
  assign iob_addr_o   = iob_addr_i;
  assign iob_wdata_o  = iob_wdata_i;
  assign iob_wstrb_o  = iob_wstrb_i;
  // CPU resp
  assign iob_rdata_o  = iob_rdata_i;
  assign iob_ready_o  = iob_ready_i;
  assign iob_rvalid_o = iob_rvalid_i;

  reg [10:0] rx_nbytes_reg;
  reg txread_reg;
  integer eth2soc_fd;
  integer soc2eth_fd;

  // Main program
  initial begin
    //init cpu bus signals
    iob_valid_i = 0;
    iob_wstrb_i = 0;

    // configure eth
    cpu_initeth();

    rx_nbytes_reg = 0;
    txread_reg = 0;


    // Init simulation/real ethernet relay files
    eth2soc_fd = $fopen("eth2soc", "rb");
    while (!eth2soc_fd) begin
      $display("Could not open \"eth2soc\"");
      eth2soc_fd = $fopen("eth2soc", "rb");
    end
    $fclose(eth2soc_fd);
    soc2eth_fd = $fopen("soc2eth", "wb");
    //$display("Opened eth2soc and soc2eth");  // DEBUG

    // Relay frames between files and ethernet core
    while (1) begin
      // Check if frames received via ethernet or files
      while (!(|rx_nbytes_reg) && !txread_reg) begin
        IOB_ETH_GET_RX_NBYTES(rx_nbytes_reg);
        eth_tx_ready(0, txread_reg);
      end
      // Relay ethernet frames from core to file
      if (|rx_nbytes_reg) begin
        //$display("$eth2file. %0t", $time);  // DEBUG
        relay_frame_eth_2_file(soc2eth_fd, rx_nbytes_reg);
        rx_nbytes_reg = 0;
        //$display("$eth2file_done");  // DEBUG
      end
      // Relay ethernet frames from file to core
      if (txread_reg) begin
        // Try to open file
        eth2soc_fd = $fopen("eth2soc", "rb");
        if (!eth2soc_fd) begin
          //wait 1 ms and try again
          #1_000_000 eth2soc_fd = $fopen("eth2soc", "rb");
          if (!eth2soc_fd) begin
            $fclose(soc2eth_fd);
            $finish();
          end
        end
        // Read file contents
        relay_frame_file_2_eth(eth2soc_fd);
        txread_reg = 0;
      end
    end
  end

  task static relay_frame_file_2_eth(input integer eth2soc_fd);
    begin
      reg [7:0] size_l, size_h, frame_byte;
      reg [15:0] frame_size;
      integer i, n;
      reg tx_ready_reg;
      tx_ready_reg = 0;

      // Read frame size (2 bytes)
      n = $fscanf(eth2soc_fd, "%c%c", size_l, size_h);
      // Continue if size read successfully
      if (n == 2) begin
        frame_size = (size_h << 8) | size_l;
        //$display("file2eth received %d bytes. %0t", frame_size, $time);  // DEBUG
        // wait for ready
        while (!tx_ready_reg) eth_tx_ready(0, tx_ready_reg);
        // set frame size
        eth_set_payload_size(0, frame_size);
        // Set ready bit
        eth_set_ready(0, 1);

        // Read RAW frame from binary encoded file, byte by byte
        for (i = 0; i < frame_size; i = i) begin
          n = $fscanf(eth2soc_fd, "%c", frame_byte);
          if (n > 0) begin
            IOB_ETH_SET_FRAME_WORD(frame_byte);
            i = i + 1;
          end
        end
        $fclose(eth2soc_fd);
        // Delete frame from file
        eth2soc_fd = $fopen("./eth2soc", "wb");
        //$display("$file2eth_done");  // DEBUG
      end  // n != 0
      $fclose(eth2soc_fd);
    end
  endtask

  task static relay_frame_eth_2_file(input integer soc2eth_fd, input reg [10:0] frame_size);
    begin
      reg [7:0] frame_byte;
      integer i;
      reg rval;

      // Write two bytes with frame size
      $fwrite(soc2eth_fd, "%c%c", frame_size[7:0], frame_size[10:8]);

      // Read frame bytes from core and write to file
      for (i = 0; i < frame_size; i = i + 1) begin
        IOB_ETH_GET_FRAME_WORD(frame_byte);
        $fwrite(soc2eth_fd, "%c", frame_byte);
      end
      $fflush(soc2eth_fd);

      // Wait for BD status update (via ready/empty bit)
      rval = 0;
      while (!rval) eth_rx_ready(64, rval);

      // Check bad CRC
      eth_bad_crc(64, rval);
      if (rval) $display("Bad CRC!");

      // Mark empty to allow receive next frame
      eth_set_empty(64, 1);
    end
  endtask


  task static cpu_initeth;
    begin
      eth_reset_bd_memory();

      /**** Configure receiver *****/
      // Mark empty; Set as last descriptor; Enable interrupt.
      eth_set_empty(64, 1);
      eth_set_wr(64, 1);
      eth_set_interrupt(64, 1);

      // Enable reception
      eth_receive(1);

      /**** Configure transmitter *****/
      // Enable CRC and PAD; Set as last descriptor; Enable interrupt.
      eth_set_crc(0, 1);
      eth_set_pad(0, 1);
      eth_set_wr(0, 1);
      eth_set_interrupt(0, 1);

      // enable transmission
      eth_send(1);
    end
  endtask

  `include "iob_eth_defines_tasks.vs"

  `include "iob_eth_csrs_emb_tb.vs"

  `include "iob_tasks.vs"

endmodule
