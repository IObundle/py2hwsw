/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef H_IOB_UART_CSRS_H
#define H_IOB_UART_CSRS_H

#include <stdint.h>

// used address space width
#define IOB_UART_CSRS_ADDR_W 3

// Addresses
#define IOB_UART_SOFTRESET_ADDR 0
#define IOB_UART_DIV_ADDR 2
#define IOB_UART_TXDATA_ADDR 4
#define IOB_UART_TXEN_ADDR 5
#define IOB_UART_RXEN_ADDR 6
#define IOB_UART_TXREADY_ADDR 0
#define IOB_UART_RXREADY_ADDR 1
#define IOB_UART_RXDATA_ADDR 4
#define IOB_UART_VERSION_ADDR 6

// Data widths (bit)
#define IOB_UART_SOFTRESET_W 8
#define IOB_UART_DIV_W 16
#define IOB_UART_TXDATA_W 8
#define IOB_UART_TXEN_W 8
#define IOB_UART_RXEN_W 8
#define IOB_UART_TXREADY_W 8
#define IOB_UART_RXREADY_W 8
#define IOB_UART_RXDATA_W 8
#define IOB_UART_VERSION_W 16

// Core Setters and Getters
void iob_uart_set_baseaddr(uint32_t addr);
void iob_uart_set_softreset(uint8_t value);
void iob_uart_set_div(uint16_t value);
void iob_uart_set_txdata(uint8_t value);
void iob_uart_set_txen(uint8_t value);
void iob_uart_set_rxen(uint8_t value);
uint32_t iob_uart_get_baseaddr();
uint8_t iob_uart_get_txready();
uint8_t iob_uart_get_rxready();
uint8_t iob_uart_get_rxdata();
uint16_t iob_uart_get_version();

void iob_write(unsigned int cpu_address, unsigned cpu_data_w,
               unsigned int cpu_data);
unsigned int iob_read(unsigned int cpu_address, unsigned int cpu_data_w);

#endif // H_IOB_UART__CSRS_H
