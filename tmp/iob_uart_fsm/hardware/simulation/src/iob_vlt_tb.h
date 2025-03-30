/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "Viob_uart.h"
typedef Viob_uart dut_t;

void iob_write(unsigned int cpu_address, unsigned cpu_data_w,
               unsigned int cpu_data);
unsigned int iob_read(unsigned int cpu_address, unsigned int cpu_data_w);

int iob_core_tb();

// these defines will be deprecated when iob_uart_csrs_ becomes csrs_iob_
#define csrs_iob_valid_i iob_uart_csrs_iob_valid_i
#define csrs_iob_ready_o iob_uart_csrs_iob_ready_o

#define csrs_iob_addr_i iob_uart_csrs_iob_addr_i

#define csrs_iob_wdata_i iob_uart_csrs_iob_wdata_i
#define csrs_iob_wstrb_i iob_uart_csrs_iob_wstrb_i

#define csrs_iob_rdata_o iob_uart_csrs_iob_rdata_o
#define csrs_iob_rvalid_o iob_uart_csrs_iob_rvalid_o
#define csrs_iob_rready_i iob_uart_csrs_iob_rready_i
