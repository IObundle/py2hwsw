/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/* PC Emulation of axistream-in peripheral */

#include <stdint.h>

#include "iob_axistream_in_csrs.h"

// Base Address
static int base;
void iob_axistream_in_csrs_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
uint32_t iob_axistream_in_csrs_get_data() { return 0x00; }

uint8_t iob_axistream_in_csrs_get_empty() { return 0x01; }

uint8_t iob_axistream_in_csrs_get_tlast_detected() { return 0x00; }

uint32_t iob_axistream_in_csrs_get_nwords() { return 0x00; }

void iob_axistream_in_csrs_set_soft_reset(uint8_t value) {}

void iob_axistream_in_csrs_set_enable(uint8_t value) {}

void iob_axistream_in_csrs_set_fifo_threshold(uint32_t value) {}

void iob_axistream_in_csrs_set_mode(uint8_t value) {}

uint32_t iob_axistream_in_csrs_get_fifo_level() { return 0x00; }

uint16_t iob_axistream_in_csrs_get_version() { return 0xaaaa; }
