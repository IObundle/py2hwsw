/*
 * SPDX-FileCopyrightText: 2025 IObundle, Lda
 *
 * SPDX-License-Identifier: MIT
 *
 * Py2HWSW Version 0.81 has generated this code
 * (https://github.com/IObundle/py2hwsw).
 */

#include "iob_timer_csrs.h"

// Base Address
static uint32_t base;
void iob_timer_csrs_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
void iob_timer_csrs_set_reset(uint8_t value) {
  iob_write(base + IOB_TIMER_CSRS_RESET_ADDR, IOB_TIMER_CSRS_RESET_W, value);
}

void iob_timer_csrs_set_enable(uint8_t value) {
  iob_write(base + IOB_TIMER_CSRS_ENABLE_ADDR, IOB_TIMER_CSRS_ENABLE_W, value);
}

void iob_timer_csrs_set_sample(uint8_t value) {
  iob_write(base + IOB_TIMER_CSRS_SAMPLE_ADDR, IOB_TIMER_CSRS_SAMPLE_W, value);
}

uint32_t iob_timer_csrs_get_data_low() {
  return iob_read(base + IOB_TIMER_CSRS_DATA_LOW_ADDR,
                  IOB_TIMER_CSRS_DATA_LOW_W);
}

uint32_t iob_timer_csrs_get_data_high() {
  return iob_read(base + IOB_TIMER_CSRS_DATA_HIGH_ADDR,
                  IOB_TIMER_CSRS_DATA_HIGH_W);
}

uint16_t iob_timer_csrs_get_version() {
  return iob_read(base + IOB_TIMER_CSRS_VERSION_ADDR, IOB_TIMER_CSRS_VERSION_W);
}
