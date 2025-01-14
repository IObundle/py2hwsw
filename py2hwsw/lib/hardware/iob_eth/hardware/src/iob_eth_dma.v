`timescale 1ns / 1ps

`include "iob_eth_conf.vh"
`include "iob_eth_csrs_def.vh"

`define IOB_MIN(a, b) (((a) < (b)) ? (a) : (b))

module iob_eth_dma #(
    parameter AXI_ADDR_W = 0,
    parameter AXI_DATA_W = 32,  // We currently only support 4 byte transfers
    parameter AXI_LEN_W  = 8,
    parameter AXI_ID_W   = 1,
    parameter BUFFER_W   = 11,
    parameter BD_ADDR_W  = 8    // 128 buffers = 256 addresses (2x 32-bit words each buffer)
) (
    // Control interface
    input                 rx_en_i,
    input                 tx_en_i,
    input [BD_ADDR_W-2:0] tx_bd_num_i,
    //TODO: What should happen if the value of `tx_bd_num_i` changes? Should
    //the RX state machine be reset to this buffer descriptor?
    //For example, if the state machine is reading BD number 64, and the value
    //changes to 65, should the state machine be reset to BD number 65? Or keep
    //reading 64?

    // Buffer descriptors
    output                 bd_en_o,
    output [BD_ADDR_W-1:0] bd_addr_o,
    output                 bd_wen_o,
    input  [       32-1:0] bd_i,
    output [       32-1:0] bd_o,

    // TX Front-End
    output reg                eth_data_wr_wen_o,
    output reg [BUFFER_W-1:0] eth_data_wr_addr_o,
    output reg [       8-1:0] eth_data_wr_wdata_o,
    input                     tx_ready_i,
    output                    crc_en_o,
    output     [      11-1:0] tx_nbytes_o,
    output                    send_o,

    // RX Back-End
    output                    eth_data_rd_ren_o,
    output reg [BUFFER_W-1:0] eth_data_rd_addr_o,
    input      [       8-1:0] eth_data_rd_rdata_i,
    input                     rx_data_rcvd_i,
    input                     crc_err_i,
    input      [      11-1:0] rx_nbytes_i,
    output                    rcv_ack_o,

    // AXI master interface
    `include "iob_eth_axi_m_port.vs"

    // Interrupts
    output reg tx_irq_o,
    output reg rx_irq_o,

    // No-DMA interface
    output reg [BD_ADDR_W-2:0] tx_bd_cnt_o,
    output reg [11-1:0] tx_word_cnt_o,
    input tx_frame_word_wen_i,
    input [8-1:0] tx_frame_word_wdata_i,
    output reg tx_frame_word_ready_o,
    output reg [BD_ADDR_W-2:0] rx_bd_cnt_o,
    output reg [11-1:0] rx_word_cnt_o,
    input rx_frame_word_ren_i,
    output reg [8-1:0] rx_frame_word_rdata_o,
    output reg rx_frame_word_ready_o,

    input clk_i,
    input cke_i,
    input arst_i
);

  localparam AXI_MAX_BURST_LEN = 16;
  localparam PRE_FRAME_LEN = `IOB_ETH_PREAMBLE_LEN + 1;

  // ############# Transmitter #############

  reg rx_req;
  reg tx_req;
  wire [1:0] bd_mem_arbiter_req = {rx_req, tx_req};
  wire [1:0] bd_mem_arbiter_ack;
  wire [1:0] bd_mem_arbiter_grant;
  wire bd_mem_arbiter_grant_valid;
  wire [$clog2(2)-1:0] bd_mem_arbiter_grant_encoded;
  iob_arbiter #(
      .PORTS(2),
      // arbitration type: "PRIORITY" or "ROUND_ROBIN"
      .TYPE("ROUND_ROBIN"),
      // block type: "NONE", "REQUEST", "ACKNOWLEDGE"
      .BLOCK("NONE"),
      // LSB priority: "LOW", "HIGH"
      .LSB_PRIORITY("LOW")
  ) bd_mem_arbiter (
      .clk(clk_i),
      .rst(arst_i),

      .request(bd_mem_arbiter_req),
      .acknowledge(bd_mem_arbiter_ack),

      .grant(bd_mem_arbiter_grant),
      .grant_valid(bd_mem_arbiter_grant_valid),
      .grant_encoded(bd_mem_arbiter_grant_encoded)
  );

  assign bd_mem_arbiter_ack = bd_mem_arbiter_grant & bd_mem_arbiter_grant_valid;


  reg [ BD_ADDR_W-1:0] tx_bd_addr_o;
  reg [ BD_ADDR_W-1:0] rx_bd_addr_o;
  reg                  tx_bd_wen_o;
  reg                  rx_bd_wen_o;
  reg [        32-1:0] tx_bd_o;
  reg [        32-1:0] rx_bd_o;

  reg [AXI_ADDR_W-1:0] axi_araddr_o_reg;
  reg                  axi_arvalid_o_reg;
  reg                  axi_rready_o_reg;
  assign axi_araddr_o  = axi_araddr_o_reg;
  assign axi_arvalid_o = axi_arvalid_o_reg;
  assign axi_rready_o  = axi_rready_o_reg;

  reg [AXI_ADDR_W-1:0] axi_awaddr_o_reg;
  reg                  axi_awvalid_o_reg;
  reg                  axi_wvalid_o_reg;
  reg [         4-1:0] axi_wstrb_o_reg;
  reg [AXI_DATA_W-1:0] axi_wdata_o_reg;
  reg                  axi_wlast_o_reg;
  assign axi_awaddr_o = axi_awaddr_o_reg;
  assign axi_awvalid_o = axi_awvalid_o_reg;
  assign axi_wvalid_o = axi_wvalid_o_reg;
  assign axi_wstrb_o = axi_wstrb_o_reg;
  assign axi_wdata_o = axi_wdata_o_reg;
  assign axi_wlast_o = axi_wlast_o_reg;


  // Connect BD memory bus based on arbiter selection
  assign bd_addr_o = bd_mem_arbiter_grant_encoded == 0 ? tx_bd_addr_o : rx_bd_addr_o;
  assign bd_wen_o = bd_mem_arbiter_grant_encoded == 0 ? tx_bd_wen_o : rx_bd_wen_o;
  assign bd_o = bd_mem_arbiter_grant_encoded == 0 ? tx_bd_o : rx_bd_o;

  assign bd_en_o = 1'b1;
  assign eth_data_rd_ren_o = 1'b1;

  //tx program
  reg  [4-1:0] tx_state_nxt;
  wire [4-1:0] tx_state;
  iob_reg #(
      .DATA_W (4),
      .RST_VAL(8)
  ) tx_state_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_state_nxt),
      .data_o(tx_state)
  );

  reg  [32-1:0] tx_buffer_byte_counter_nxt;
  wire [32-1:0] tx_buffer_byte_counter;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) tx_buffer_byte_counter_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_buffer_byte_counter_nxt),
      .data_o(tx_buffer_byte_counter)
  );

  reg  [BD_ADDR_W-2:0] tx_bd_num_nxt;
  wire [BD_ADDR_W-2:0] tx_bd_num;
  iob_reg #(
      .DATA_W (BD_ADDR_W - 1),
      .RST_VAL(0)
  ) tx_bd_num_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_bd_num_nxt),
      .data_o(tx_bd_num)
  );

  reg  [32-1:0] tx_buffer_descriptor_nxt;
  wire [32-1:0] tx_buffer_descriptor;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) tx_buffer_descriptor_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_buffer_descriptor_nxt),
      .data_o(tx_buffer_descriptor)
  );

  reg  [32-1:0] tx_buffer_ptr_nxt;
  wire [32-1:0] tx_buffer_ptr;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) tx_buffer_ptr_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_buffer_ptr_nxt),
      .data_o(tx_buffer_ptr)
  );

  reg  [AXI_LEN_W-1:0] axi_arlen_nxt;
  wire [AXI_LEN_W-1:0] axi_arlen;
  iob_reg #(
      .DATA_W (AXI_LEN_W),
      .RST_VAL(0)
  ) axi_arlen_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(axi_arlen_nxt),
      .data_o(axi_arlen)
  );
  assign axi_arlen_o = axi_arlen_nxt;

  reg  [1-1:0] crc_en_nxt;
  wire [1-1:0] crc_en;
  iob_reg #(
      .DATA_W (1),
      .RST_VAL(0)
  ) crc_en_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(crc_en_nxt),
      .data_o(crc_en)
  );
  assign crc_en_o = crc_en;

  reg  [11-1:0] tx_nbytes_nxt;
  wire [11-1:0] tx_nbytes;
  iob_reg #(
      .DATA_W (11),
      .RST_VAL(0)
  ) tx_nbytes_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(tx_nbytes_nxt),
      .data_o(tx_nbytes)
  );
  assign tx_nbytes_o = tx_nbytes;

  reg  [1-1:0] send_nxt;
  wire [1-1:0] send;
  iob_reg #(
      .DATA_W (1),
      .RST_VAL(0)
  ) send_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(send_nxt),
      .data_o(send)
  );
  assign send_o = send;

  always @* begin
    tx_req                     = 1'b0;
    tx_state_nxt               = tx_state + 1'b1;
    tx_bd_num_nxt              = tx_bd_num;
    tx_bd_addr_o               = 1'b0;
    tx_bd_wen_o                = 1'b0;
    tx_bd_o                    = 1'b0;
    send_nxt                   = send;
    axi_arvalid_o_reg          = 1'b0;
    axi_rready_o_reg           = 1'b0;
    eth_data_wr_wen_o          = 1'b0;
    eth_data_wr_wdata_o        = 1'b0;
    eth_data_wr_addr_o         = 1'b0;
    tx_frame_word_ready_o      = 1'b0;
    tx_irq_o                   = 1'b0;
    // No-DMA interface
    tx_bd_cnt_o                = 1'b0;
    tx_word_cnt_o              = 1'b0;

    tx_buffer_byte_counter_nxt = tx_buffer_byte_counter;
    axi_araddr_o_reg           = 1'b0;
    axi_arlen_nxt              = axi_arlen;
    crc_en_nxt                 = crc_en;
    tx_nbytes_nxt              = tx_nbytes;
    tx_buffer_descriptor_nxt   = tx_buffer_descriptor;
    tx_buffer_ptr_nxt          = tx_buffer_ptr;

    if (arst_i) begin

      tx_state_nxt      = 8;  // Fill Preamble and SFD
      tx_bd_num_nxt     = 1'b0;
      tx_bd_addr_o      = 1'b0;
      tx_bd_wen_o       = 1'b0;
      tx_bd_o           = 1'b0;
      send_nxt          = 1'b0;
      axi_arvalid_o_reg = 1'b0;
      axi_rready_o_reg  = 1'b0;
      eth_data_wr_wen_o = 1'b0;
      tx_frame_word_ready_o = 1'b0;
      tx_irq_o          = 1'b0;
      // No-DMA interface
      tx_bd_cnt_o       = 1'b0;
      tx_word_cnt_o     = 1'b0;

    end else begin

      case (tx_state)

        0: begin  // Request buffer descriptor
          tx_bd_addr_o = tx_bd_num << 1;
          tx_req = 1'b1;
          send_nxt = 1'b0;
          tx_irq_o = 1'b0;
          tx_bd_wen_o = 1'b0;

          // Wait for arbiter
          if (!bd_mem_arbiter_grant[0] || !bd_mem_arbiter_grant_valid) tx_state_nxt = tx_state;
        end

        1: begin  // Read buffer descriptor.
          tx_buffer_descriptor_nxt = bd_i;

          // Wait for ready bit and tx enable
          if (!tx_buffer_descriptor_nxt[15] || !tx_en_i) tx_state_nxt = tx_state - 1'b1;
        end

        2: begin  //Request buffer pointer
          tx_bd_addr_o = (tx_bd_num << 1) + 1;
          tx_req = 1'b1;

          // Wait for arbiter
          if (!bd_mem_arbiter_grant[0] || !bd_mem_arbiter_grant_valid) tx_state_nxt = tx_state;
        end

        3: begin  // Read buffer pointer
          tx_buffer_ptr_nxt = bd_i;
          tx_buffer_byte_counter_nxt = 0;

          // Wait for buffer ready for next frame
          if (!tx_ready_i) tx_state_nxt = tx_state - 1'b1;
        end

        4: begin  // Start frame transfer from external memory
          axi_araddr_o_reg = tx_buffer_ptr + tx_buffer_byte_counter;
          axi_arlen_nxt =
          `IOB_MIN(AXI_MAX_BURST_LEN, tx_buffer_descriptor[31:16] - tx_buffer_byte_counter)
          - 1'b1;
          axi_arvalid_o_reg = 1'b1;
          axi_rready_o_reg = 1'b0;
          eth_data_wr_wen_o = 1'b0;

          // Wait for address ready
          if (!axi_arready_i) tx_state_nxt = tx_state;

          // Check if frame transfer is complete
          if (tx_buffer_descriptor[31:16] - tx_buffer_byte_counter == 0) begin
            axi_arvalid_o_reg = 1'b0;

            // Configure transmitter settings
            crc_en_nxt = tx_buffer_descriptor[11];
            tx_nbytes_nxt = PRE_FRAME_LEN + tx_buffer_descriptor[26:16]; // 11 bits is enough for frame size
            send_nxt = 1'b1;

            // Disable ready bit
            tx_buffer_descriptor_nxt[15] = 1'b0;

            // Write transmit status
            tx_state_nxt = 6;
          end

          // No-DMA interface
          tx_bd_cnt_o   = tx_bd_num;
          tx_word_cnt_o = tx_buffer_byte_counter;
	  tx_frame_word_ready_o = 1'b1;
          if (tx_frame_word_wen_i) begin
            tx_buffer_byte_counter_nxt = tx_buffer_byte_counter + 1'b1;
            // Send word from CPU to buffer
            eth_data_wr_wen_o = 1'b1;
            eth_data_wr_addr_o = PRE_FRAME_LEN + tx_buffer_byte_counter;
            eth_data_wr_wdata_o = tx_frame_word_wdata_i;
          end

        end

        5: begin  // Transfer frame word from memory to buffer
          tx_state_nxt = tx_state;
          axi_rready_o_reg = 1'b0;
          axi_arvalid_o_reg = 1'b0;

          if (axi_rvalid_i == 1) begin
            tx_buffer_byte_counter_nxt = tx_buffer_byte_counter + 1'b1;
            axi_rready_o_reg = 1'b1;
            // Send word to buffer
            eth_data_wr_wen_o = 1'b1;
            eth_data_wr_addr_o = PRE_FRAME_LEN + tx_buffer_byte_counter;

            axi_araddr_o_reg = tx_buffer_ptr + tx_buffer_byte_counter;
            eth_data_wr_wdata_o = axi_rdata_i[axi_araddr_o_reg[1:0]*8+:8];

            if (axi_rlast_i == 1) tx_state_nxt = tx_state - 1'b1;
          end

        end

        6: begin  // Wait for send_o to be read by transmitter
          tx_state_nxt = tx_state;
	  tx_frame_word_ready_o = 1'b0;
          if (!tx_ready_i) begin
            send_nxt = 1'b0;
            tx_state_nxt = tx_state + 1'b1;
          end
        end

        7: begin  // Write transmit status
          tx_state_nxt = tx_state;

          tx_bd_addr_o = tx_bd_num << 1;
          tx_bd_wen_o = 1'b1;
          tx_bd_o = tx_buffer_descriptor;
          tx_req = 1'b1;

          // Wait for arbiter
          if (bd_mem_arbiter_grant[0] && bd_mem_arbiter_grant_valid) begin
            // Generate interrupt
            tx_irq_o = tx_buffer_descriptor[14];

            // Select next BD address based on WR bit
            if (tx_buffer_descriptor[13] == 0) tx_bd_num_nxt = tx_bd_num + 1'b1;
            else tx_bd_num_nxt = 1'b0;

            // Reset BD number if reached maximum
            if (tx_buffer_descriptor[13] == 0 && &tx_bd_num) tx_bd_num_nxt = 1'b0;

            // Go to next buffer descriptor
            tx_state_nxt = 1'b0;
          end
        end

        8: begin  // Wirte Preamble and SFD (runs at arst)
          tx_state_nxt = tx_state;
          eth_data_wr_wen_o = 1'b1;
          if (tx_buffer_byte_counter == `IOB_ETH_PREAMBLE_LEN) eth_data_wr_wdata_o = `IOB_ETH_SFD;
          else eth_data_wr_wdata_o = `IOB_ETH_PREAMBLE;
          eth_data_wr_addr_o = tx_buffer_byte_counter;
          tx_buffer_byte_counter_nxt = tx_buffer_byte_counter + 1'b1;
          if (tx_buffer_byte_counter == PRE_FRAME_LEN) tx_state_nxt = 1'b0;
        end

        default: ;

      endcase

    end
  end

  // AXI Master Read interface
  // Constants
  assign axi_arid_o    = 0;
  assign axi_arsize_o  = 0; // arsize=0 to transfer 8-bit data
  assign axi_arburst_o = 1;
  assign axi_arlock_o  = 0;
  assign axi_arcache_o = 2;
  assign axi_arprot_o  = 2;
  assign axi_arqos_o   = 0;
  //axi_rid_i
  //axi_rresp_i

  // ############# Receiver #############

  //rx program
  reg  [3-1:0] rx_state_nxt;
  wire [3-1:0] rx_state;
  iob_reg #(
      .DATA_W (3),
      .RST_VAL(0)
  ) rx_state_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_state_nxt),
      .data_o(rx_state)
  );

  reg  [32-1:0] rx_buffer_byte_counter_nxt;
  wire [32-1:0] rx_buffer_byte_counter;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) rx_buffer_byte_counter_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_buffer_byte_counter_nxt),
      .data_o(rx_buffer_byte_counter)
  );

  reg  [BD_ADDR_W-2:0] rx_bd_num_nxt;
  wire [BD_ADDR_W-2:0] rx_bd_num;
  iob_reg #(
      .DATA_W(BD_ADDR_W - 1),
      .RST_VAL(32'd64)  // Same as default value of 'TX_BD_NUM' register
  ) rx_bd_num_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_bd_num_nxt),
      .data_o(rx_bd_num)
  );

  reg  [32-1:0] rx_burst_word_num_nxt;
  wire [32-1:0] rx_burst_word_num;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) rx_burst_word_num_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_burst_word_num_nxt),
      .data_o(rx_burst_word_num)
  );

  reg  [32-1:0] rx_buffer_descriptor_nxt;
  wire [32-1:0] rx_buffer_descriptor;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) rx_buffer_descriptor_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_buffer_descriptor_nxt),
      .data_o(rx_buffer_descriptor)
  );

  reg  [32-1:0] rx_buffer_ptr_nxt;
  wire [32-1:0] rx_buffer_ptr;
  iob_reg #(
      .DATA_W (32),
      .RST_VAL(0)
  ) rx_buffer_ptr_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rx_buffer_ptr_nxt),
      .data_o(rx_buffer_ptr)
  );

  reg  [AXI_LEN_W-1:0] axi_awlen_nxt;
  wire [AXI_LEN_W-1:0] axi_awlen;
  iob_reg #(
      .DATA_W (AXI_LEN_W),
      .RST_VAL(0)
  ) axi_awlen_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(axi_awlen_nxt),
      .data_o(axi_awlen)
  );
  assign axi_awlen_o = axi_awlen_nxt;

  reg  [1-1:0] rcv_ack_nxt;
  wire [1-1:0] rcv_ack;
  iob_reg #(
      .DATA_W (1),
      .RST_VAL(0)
  ) rcv_ack_reg (
      .clk_i (clk_i),
      .cke_i (cke_i),
      .arst_i(arst_i),
      .data_i(rcv_ack_nxt),
      .data_o(rcv_ack)
  );
  assign rcv_ack_o = rcv_ack;

  always @* begin
    rx_req                     = 1'b0;
    rx_state_nxt               = rx_state + 1'b1;
    rx_bd_num_nxt              = rx_bd_num;
    rx_bd_addr_o               = 1'b0;
    rx_bd_wen_o                = 1'b0;
    rx_bd_o                    = 1'b0;
    rcv_ack_nxt                = rcv_ack;
    axi_awvalid_o_reg          = 1'b0;
    axi_wvalid_o_reg           = 1'b0;
    axi_wlast_o_reg            = 1'b0;
    rx_irq_o                   = 1'b0;
    // No-DMA interface
    rx_bd_cnt_o                = 1'b0;
    rx_word_cnt_o              = 1'b0;
    rx_frame_word_rdata_o      = 1'b0;
    rx_frame_word_ready_o      = 1'b0;

    axi_awaddr_o_reg           = 1'b0;
    axi_wstrb_o_reg            = 1'b0;
    axi_wdata_o_reg            = 1'b0;
    eth_data_rd_addr_o         = 1'b0;
    rx_buffer_byte_counter_nxt = rx_buffer_byte_counter;
    rx_burst_word_num_nxt      = rx_burst_word_num;
    axi_awlen_nxt              = axi_awlen;
    rx_buffer_descriptor_nxt   = rx_buffer_descriptor;
    rx_buffer_ptr_nxt          = rx_buffer_ptr;


    if (arst_i) begin

      rx_state_nxt           = 1'b0;
      rx_bd_num_nxt          = tx_bd_num_i;
      rx_bd_addr_o           = 1'b0;
      rx_bd_wen_o            = 1'b0;
      rx_bd_o                = 1'b0;
      rcv_ack_nxt            = 1'b0;
      axi_awvalid_o_reg      = 1'b0;
      axi_wvalid_o_reg       = 1'b0;
      axi_wlast_o_reg        = 1'b0;
      rx_irq_o               = 1'b0;
      // No-DMA interface
      rx_bd_cnt_o            = 1'b0;
      rx_word_cnt_o          = 1'b0;
      rx_frame_word_rdata_o  = 1'b0;
      rx_frame_word_ready_o  = 1'b0;

    end else begin

      case (rx_state)

        0: begin  // Request buffer descriptor
          rx_bd_addr_o = rx_bd_num << 1;
          rx_req = 1'b1;
          rcv_ack_nxt = 1'b0;
          rx_irq_o = 1'b0;
          rx_bd_wen_o = 1'b0;

          // Wait for arbiter
          if (!bd_mem_arbiter_grant[1] || !bd_mem_arbiter_grant_valid) rx_state_nxt = rx_state;

        end

        1: begin  // Read buffer descriptor.
          rx_buffer_descriptor_nxt = bd_i;

          // Wait for ready bit and rx enable
          if (!rx_buffer_descriptor_nxt[15] || !rx_en_i) rx_state_nxt = rx_state - 1'b1;
        end

        2: begin  //Request buffer pointer
          rx_bd_addr_o = (rx_bd_num << 1) + 1;
          rx_req = 1'b1;

          // Wait for arbiter
          if (!bd_mem_arbiter_grant[1] || !bd_mem_arbiter_grant_valid) rx_state_nxt = rx_state;
        end

        3: begin  // Read buffer pointer
          rx_buffer_ptr_nxt = bd_i;
          rx_buffer_byte_counter_nxt = 0;

          // Wait for buffer to be filled with next frame
          if (!rx_data_rcvd_i) rx_state_nxt = rx_state - 1'b1;
        end

        4: begin  // Start frame transfer to external memory
          // TODO: If awlen > 0, ensure that awaddr does not cause
          // a transaction that may cross the AXI 4k boundary
          axi_awaddr_o_reg = rx_buffer_ptr + rx_buffer_byte_counter;
          axi_awlen_nxt = `IOB_MIN(AXI_MAX_BURST_LEN, rx_nbytes_i - rx_buffer_byte_counter) - 1'b1;
          axi_awvalid_o_reg = 1'b1;
          axi_wvalid_o_reg = 1'b0;
          axi_wlast_o_reg = 1'b0;
          // Get word from buffer
          eth_data_rd_addr_o = rx_buffer_byte_counter;
          rx_burst_word_num_nxt = 1'b0;

          // Wait for address ready
          if (!axi_awready_i) rx_state_nxt = rx_state;

          // Check if frame transfer is complete
          if (rx_nbytes_i - rx_buffer_byte_counter == 0) begin
            axi_awvalid_o_reg = 1'b0;

            // Disable ready bit
            rx_buffer_descriptor_nxt[15] = 1'b0;
            // Write crc_err
            rx_buffer_descriptor_nxt[1] = crc_err_i;
            // Write buffer size
            rx_buffer_descriptor_nxt[31:16] = rx_nbytes_i;

            // Acknowledge read complete
            rcv_ack_nxt = 1'b1;

            // Write receive status
            rx_state_nxt = 6;
          end

          // No-DMA interface
          rx_bd_cnt_o            = rx_bd_num;
          rx_word_cnt_o          = rx_buffer_byte_counter;
    	  rx_frame_word_ready_o  = 1'b1;
          if (rx_frame_word_ren_i) begin
            rx_buffer_byte_counter_nxt = rx_buffer_byte_counter + 1'b1;
            eth_data_rd_addr_o         = rx_buffer_byte_counter + 1'b1;  // Update next word addr
            // Send word from buffer to CPU
            rx_frame_word_rdata_o      = eth_data_rd_rdata_i;
          end

        end

        5: begin  // Transfer frame word from buffer to memory
          rx_state_nxt = rx_state;
          axi_awvalid_o_reg = 1'b0;
          axi_wvalid_o_reg = 1'b1;

          axi_awaddr_o_reg = rx_buffer_ptr + rx_buffer_byte_counter;
          axi_wstrb_o_reg = 1 << axi_awaddr_o_reg[1:0];
          axi_wdata_o_reg = eth_data_rd_rdata_i << (axi_awaddr_o_reg[1:0] * 8);

          eth_data_rd_addr_o = rx_buffer_byte_counter;

          // Enable wlast in last transfer of the burst
          if (rx_burst_word_num == axi_awlen) begin
            axi_wlast_o_reg = 1'b1;
          end

          // wait for write ready
          if (axi_wready_i == 1) begin
            rx_buffer_byte_counter_nxt = rx_buffer_byte_counter + 1'b1;
            eth_data_rd_addr_o = rx_buffer_byte_counter + 1'b1;  // Update next word addr
            rx_burst_word_num_nxt = rx_burst_word_num + 1'b1;

            // Burst complete
            if (rx_burst_word_num == axi_awlen) begin
              rx_state_nxt = rx_state - 1'b1;
            end
          end

        end

        6: begin  // Wait for rcv_ack to be read by receiver
          rx_state_nxt = rx_state;
	  rx_frame_word_ready_o = 1'b0;
          if (!rx_data_rcvd_i) begin
            rcv_ack_nxt  = 1'b0;
            rx_state_nxt = rx_state + 1'b1;
          end
        end

        7: begin  // Write receive status
          rx_state_nxt = rx_state;

          rx_bd_addr_o = rx_bd_num << 1;
          rx_bd_wen_o = 1'b1;
          rx_bd_o = rx_buffer_descriptor;
          rx_req = 1'b1;

          // Wait for arbiter
          if (bd_mem_arbiter_grant[1] && bd_mem_arbiter_grant_valid) begin
            // Generate interrupt
            rx_irq_o = rx_buffer_descriptor[14];

            // Select next BD address based on WR bit
            if (rx_buffer_descriptor[13] == 0) rx_bd_num_nxt = rx_bd_num + 1'b1;
            else rx_bd_num_nxt = tx_bd_num_i;

            // Reset BD number if reached maximum
            if (rx_buffer_descriptor[13] == 0 && &rx_bd_num) rx_bd_num_nxt = tx_bd_num_i;


            // Go to next buffer descriptor
            rx_state_nxt = 1'b0;
          end
        end

        default: ;

      endcase

    end
  end

  // AXI Master Write interface
  // Constants
  assign axi_awid_o    = 0;
  assign axi_awsize_o  = 0; // awsize=0 to transfer 8-bit data
  assign axi_awburst_o = 1;
  assign axi_awlock_o  = 0;
  assign axi_awcache_o = 2;
  assign axi_awprot_o  = 2;
  assign axi_awqos_o   = 0;
  assign axi_bready_o  = 1'b1;
  // axi_bid_i
  // axi_bresp_i,
  // axi_bvalid_i



endmodule
