/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "Viob_uart_sim.h"
typedef Viob_uart_sim dut_t;

// these defines will be deprecated when iob_uart_csrs_ becomes iob_csrs_
#define csrs_iob_valid_i iob_uart_csrs_iob_valid_i
#define csrs_iob_ready_o iob_uart_csrs_iob_ready_o

#define csrs_iob_addr_i iob_uart_csrs_iob_addr_i

#define csrs_iob_wdata_i iob_uart_csrs_iob_wdata_i
#define csrs_iob_wstrb_i iob_uart_csrs_iob_wstrb_i

#define csrs_iob_rdata_o iob_uart_csrs_iob_rdata_o
#define csrs_iob_rvalid_o iob_uart_csrs_iob_rvalid_o
