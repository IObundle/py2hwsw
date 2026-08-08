/*
 * SPDX-FileCopyrightText: 2026 IObundle
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#ifndef _DMA_H_
#define _DMA_H_

#include <stdint.h>

#include "iob_dma_csrs.h"

// DMA functions

// Initialize Base Address
void dma_init(uint32_t addr);

// Start a DMA write transfer
void dma_write_transfer(uint32_t phys_addr, uint32_t size);

// Start a DMA read transfer
void dma_read_transfer(uint32_t phys_addr, uint32_t size);

uint8_t dma_write_busy();

uint8_t dma_read_busy();

#endif //_DMA_H_
