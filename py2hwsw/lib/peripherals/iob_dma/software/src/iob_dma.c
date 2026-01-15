/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_dma.h"

// DMA functions

// Start a DMA write transfer
// Write to memory
// base_addr: Base address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_write_transfer(uint32_t *base_addr, uint32_t size) {
  // cast to uintptr_t to avoid compilation error in 64bit machines
  // example: when running verilator simulation
  iob_dma_csrs_set_w_addr((uint32_t)(uintptr_t)base_addr);
  iob_dma_csrs_set_w_length(size);
  iob_dma_csrs_set_w_start(1);
}

// Start a DMA read transfer
// Read from memory
// base_addr: Base address of external memory to start the data transfer.
// size: Amount of 32-bit words to transfer.
void dma_read_transfer(uint32_t *base_addr, uint32_t size) {
  // cast to uintptr_t to avoid compilation error in 64bit machines
  // example: when running verilator simulation
  iob_dma_csrs_set_r_addr((uint32_t)(uintptr_t)base_addr);
  iob_dma_csrs_set_r_length(size);
  iob_dma_csrs_set_r_start(1);
}

// Check if DMA is busy for new write transfer
uint8_t dma_write_busy() { return (iob_dma_csrs_get_w_busy()); }

// Check if DMA is busy for new read transfer
uint8_t dma_read_busy() { return (iob_dma_csrs_get_r_busy()); }
