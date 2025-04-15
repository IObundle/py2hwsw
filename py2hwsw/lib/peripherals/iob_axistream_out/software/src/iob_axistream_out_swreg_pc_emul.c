/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/* PC Emulation of axistream-out peripheral */

#include <stdint.h>

#include "iob_axistream_out_csrs.h"

// Base Address
static int base;
void iob_axistream_out_csrs_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
void iob_axistream_out_csrs_set_data(uint32_t value) {}

uint8_t iob_axistream_out_csrs_get_full() { return 0x00; }

void iob_axistream_out_csrs_set_soft_reset(uint8_t value) {}

void iob_axistream_out_csrs_set_enable(uint8_t value) {}

void iob_axistream_out_csrs_set_wstrb(uint8_t value) {}

void iob_axistream_out_csrs_set_last(uint8_t value) {}

void iob_axistream_out_csrs_set_fifo_threshold(uint32_t value) {}

uint32_t iob_axistream_out_csrs_get_fifo_level() { return 0x00; }

uint16_t iob_axistream_out_csrs_get_version() { return 0xaaaa; }
