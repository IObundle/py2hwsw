/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_s_axi_m_sim_controller.h"

void iob_s_axi_m_init_baseaddr(uint32_t addr);

void iob_s_axi_m_controller_init_baseaddr(uint32_t addr);

void iob_s_axi_m_reset();

void iob_s_axi_m_set_burst_length(uint16_t length);

uint16_t iob_s_axi_m_get_w_level();

uint16_t iob_s_axi_m_get_r_level();

void iob_s_axi_m_write_32b_data(uint32_t addr, uint32_t value);

uint32_t iob_s_axi_m_read_32b_data(uint32_t addr);
