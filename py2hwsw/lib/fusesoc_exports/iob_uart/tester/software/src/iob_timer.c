/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_timer.h"

// Base Address
static uint32_t base;

void timer_reset() {
  iob_timer_csrs_set_reset(1);
  iob_timer_csrs_set_reset(0);
}

void timer_init(uint32_t base_address) {
  base = base_address;
  iob_timer_csrs_init_baseaddr(base_address);
  timer_reset();
  iob_timer_csrs_set_enable(1);
}

uint64_t timer_get_count() {
  // sample timer counter
  iob_timer_csrs_set_sample(1);
  iob_timer_csrs_set_sample(0);

  uint64_t count = (uint64_t)iob_timer_csrs_get_data_high();
  count <<= IOB_TIMER_CSRS_DATA_LOW_W;
  count |= (uint64_t)iob_timer_csrs_get_data_low();

  return count;
}
