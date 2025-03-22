/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "Viob_system_sim.h"
typedef Viob_system_sim dut_t;

// these defines will be deprecated when iob_uart_csrs_ becomes iob_csrs_
#define csrs_iob_valid_i uart_iob_valid_i
#define csrs_iob_ready_o uart_iob_ready_o

#define csrs_iob_addr_i uart_iob_addr_i

#define csrs_iob_wdata_i uart_iob_wdata_i
#define csrs_iob_wstrb_i uart_iob_wstrb_i

#define csrs_iob_rdata_o uart_iob_rdata_o
#define csrs_iob_rvalid_o uart_iob_rvalid_o
#define csrs_iob_rready_i uart_iob_rready_i

#ifdef IOB_SYSTEM_USE_ETHERNET
#define csrs_iob_valid_i ethernet_iob_valid_i
#define csrs_iob_ready_o ethernet_iob_ready_o

#define csrs_iob_addr_i ethernet_iob_addr_i

#define csrs_iob_wdata_i ethernet_iob_wdata_i
#define csrs_iob_wstrb_i ethernet_iob_wstrb_i

#define csrs_iob_rdata_o ethernet_iob_rdata_o
#define csrs_iob_rvalid_o ethernet_iob_rvalid_o
#define csrs_iob_rready_i ethernet_iob_rready_i
#endif
