#include "iob_dma.h"

// DMA functions

// Start a DMA write transfer
// Write to memory
// base_addr: Base address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_write_transfer(uint32_t *base_addr, uint32_t size) {
  iob_dma_csrs_set_w_addr((uint32_t)base_addr);
  iob_dma_csrs_set_w_length(size);
  iob_dma_csrs_set_w_start(1);
}

// Start a DMA read transfer
// Read from memory
// base_addr: Base address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_read_transfer(uint32_t *base_addr, uint32_t size) {
  iob_dma_csrs_set_r_addr((uint32_t)base_addr);
  iob_dma_csrs_set_r_length(size);
  iob_dma_csrs_set_r_start(1);
}

// Check if DMA is busy for new write transfer
uint8_t dma_write_busy() { return (iob_dma_csrs_get_w_busy()); }

// Check if DMA is busy for new read transfer
uint8_t dma_read_busy() { return (iob_dma_csrs_get_r_busy()); }
