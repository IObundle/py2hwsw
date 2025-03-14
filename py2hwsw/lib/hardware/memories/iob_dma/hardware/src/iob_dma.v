`timescale 1ns / 1ps

/*
Internal DMA for AC97
   This unit breaks down an AXIS into multiple bursts of AXI.
   Address (and length) are set by using the write_ or read_ interfaces.
   The busy signals can be used to probe the state of the transfer. When asserted,
   they indicate that the unit is doing a data transfer.
   Both AXIS In and AXIS Out operate individually and can work simultaneously (these units can also
   be instantiated individually)
   4k boundaries are handled automatically.

AXIS Out:
   After configuring read_addr and read_length, the axis_out transfer can start by setting the
   read_start_transfer signal. There is no limit to the amount of data that can be sent.

AXIS In:
   After configuring write_addr and write_length, the axis_in transfer can start by setting the
   write_start_transfer signal.
   Length is given as the amount of dwords. A length of 1 means that one transfer is performed.
   If the axis_in interface is stalled permanently before completing the full transfer, the unit
   might block the entire system, as it will continue to keep the AXI connection alive.
   If for some reason the user realises that it requested a length bigger then need, the user still
   needs to keep outputing data out of the axis_in interface. Only when write_busy is de-asserted
   has the transfer fully completed.

Note: if the transfer goes over the maximum size, given by AXI_ADDR_W,
   the transfer will wrap around and will start reading/writing to the lower addresses.
*/

`include "iob_dma_conf.vh"

module iob_dma_core #(
   `include "iob_dma_params.vs"
) (
   `include "iob_dma_io.vs"
);

   // AXIS In (DMA Read)
   iob_dma_read #(
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_ID_W  (AXI_ID_W),
      .DMA_RLEN_W(DMA_RLEN_W)
   ) ac97_dma_read (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i(rst_i),

      .r_addr_i          (r_addr_i),
      .r_length_i        (r_length_i),
      .r_start_transfer_i(r_start_transfer_i),
      .r_max_len_i       (r_max_len_i),
      .r_remaining_data_o(r_remaining_data_o),
      .r_busy_o          (r_busy_o),

      .axis_out_tdata_o (axis_out_data_o),
      .axis_out_tvalid_o(axis_out_valid_o),
      .axis_out_tready_i(axis_out_ready_i),

      .ext_mem_clk_o   (r_ext_mem_clk_o),
      .ext_mem_w_en_o  (r_ext_mem_w_en_o),
      .ext_mem_w_addr_o(r_ext_mem_w_addr_o),
      .ext_mem_w_data_o(r_ext_mem_w_data_o),
      .ext_mem_r_en_o  (r_ext_mem_r_en_o),
      .ext_mem_r_addr_o(r_ext_mem_r_addr_o),
      .ext_mem_r_data_i(r_ext_mem_r_data_i),

      `include "iob_dma_read_m_axi_read_m_m_portmap.vs"

   );

   // AXIS Out (DMA Write)
   iob_dma_write #(
      .AXI_ADDR_W(AXI_ADDR_W),
      .AXI_LEN_W (AXI_LEN_W),
      .AXI_DATA_W(AXI_DATA_W),
      .AXI_ID_W  (AXI_ID_W),
      .DMA_WLEN_W(DMA_WLEN_W)
   ) ac97_dma_write (
      .clk_i(clk_i),
      .cke_i(cke_i),
      .arst_i(arst_i),
      .rst_i(rst_i),

      .w_addr_i          (w_addr_i),
      .w_length_i        (w_length_i),
      .w_start_transfer_i(w_start_transfer_i),
      .w_max_len_i       (w_max_len_i),
      .w_remaining_data_o(w_remaining_data_o),
      .w_busy_o          (w_busy_o),

      .axis_in_data_i (axis_in_data_i),
      .axis_in_valid_i(axis_in_valid_i),
      .axis_in_ready_o(axis_in_ready_o),

      .ext_mem_clk_o   (w_ext_mem_clk_o),
      .ext_mem_w_en_o  (w_ext_mem_w_en_o),
      .ext_mem_w_addr_o(w_ext_mem_w_addr_o),
      .ext_mem_w_data_o(w_ext_mem_w_data_o),
      .ext_mem_r_en_o  (w_ext_mem_r_en_o),
      .ext_mem_r_addr_o(w_ext_mem_r_addr_o),
      .ext_mem_r_data_i(w_ext_mem_r_data_i),

      `include "iob_dma_write_m_axi_write_m_m_portmap.vs"

   );

endmodule
