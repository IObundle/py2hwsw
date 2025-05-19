/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_s_axi_m.h"

// Base Address
static uint32_t base;
void iob_s_axi_m_init_baseaddr(uint32_t addr) { base = addr; }

void iob_s_axi_m_controller_init_baseaddr(uint32_t addr) {
  iob_s_axi_m_sim_controller_csrs_init_baseaddr(addr);
}

void iob_axis_in_reset() {
  iob_s_axi_m_sim_controller_csrs_set_soft_reset(1);
  iob_s_axi_m_sim_controller_csrs_set_soft_reset(0);
}

void iob_s_axi_m_set_burst_length(uint16_t length) {
  iob_s_axi_m_sim_controller_csrs_set_burst_length(length);
}

uint16_t iob_s_axi_m_get_w_level() {
  return iob_s_axi_m_sim_controller_csrs_get_w_level();
}

uint16_t iob_s_axi_m_get_r_level() {
  return iob_s_axi_m_sim_controller_csrs_get_r_level();
}

void iob_s_axi_m_write_32b_data(uint32_t addr, uint32_t value) {
  iob_write(base + addr, 32, value);
}

uint32_t iob_s_axi_m_read_32b_data(uint32_t addr) {
  return iob_read(base + addr, 32);
}
