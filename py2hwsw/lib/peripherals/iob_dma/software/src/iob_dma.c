/*
 * SPDX-FileCopyrightText: 2026 IObundle
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include "iob_dma.h"

// DMA functions

// Initialize Base Address
void dma_init(uint32_t addr) { iob_dma_csrs_init_baseaddr(addr); }

// Start a DMA write transfer
// Write to memory
// phys_addr: Physical address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_write_transfer(uint32_t phys_addr, uint32_t size) {
  iob_dma_csrs_set_w_addr(phys_addr);
  iob_dma_csrs_set_w_length(size);
  iob_dma_csrs_set_w_start(1);
}

// Start a DMA read transfer
// Read from memory
// phys_addr: Physical address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_read_transfer(uint32_t phys_addr, uint32_t size) {
  iob_dma_csrs_set_r_addr(phys_addr);
  iob_dma_csrs_set_r_length(size);
  iob_dma_csrs_set_r_start(1);
}

// Check if DMA is busy for new write transfer
uint8_t dma_write_busy() { return (iob_dma_csrs_get_w_busy()); }

// Check if DMA is busy for new read transfer
uint8_t dma_read_busy() { return (iob_dma_csrs_get_r_busy()); }
