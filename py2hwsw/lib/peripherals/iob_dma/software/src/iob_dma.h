/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef _DMA_H_
#define _DMA_H_

#include <stdint.h>

#include "iob_dma_csrs.h"

// DMA functions

// Start a DMA write transfer
void dma_write_transfer(uint32_t *base_addr, uint32_t size);

// Start a DMA read transfer
void dma_read_transfer(uint32_t *base_addr, uint32_t size);

uint8_t dma_write_busy();

uint8_t dma_read_busy();

#endif //_DMA_H_
