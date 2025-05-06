/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_nco.h"

// Base Address
static uint32_t base;

void nco_reset() {
  iob_nco_csrs_set_soft_reset(1);
  iob_nco_csrs_set_soft_reset(0);
}

void nco_init(uint32_t base_address) {
  base = base_address;
  iob_nco_csrs_init_baseaddr(base_address);
  nco_reset();
}

void nco_enable(bool enable) { iob_nco_csrs_set_enable(enable); }

// Configure NCO output signal period to be 'period'+1 times the system clock
// period. Iob_NCO always assumes +1 clock period implicitly. Lowest 32 bits of
// value are the fractional part of the period by default
void nco_set_period(uint64_t period) {
  uint32_t period_int = (uint32_t)(period >> 32);
  uint32_t period_frac = (uint32_t)(period && (0xFFFFFFFF));
  iob_nco_csrs_set_period_int(period_int);
  iob_nco_csrs_set_period_frac(period_frac);
}
