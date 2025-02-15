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
void IOB_UART_SET_BASEADDR(uint32_t addr);
void IOB_UART_SET_SOFTRESET(uint8_t value);
void IOB_UART_SET_DIV(uint16_t value);
void IOB_UART_SET_TXDATA(uint8_t value);
void IOB_UART_SET_TXEN(uint8_t value);
void IOB_UART_SET_RXEN(uint8_t value);
uint32_t IOB_UART_GET_BASEADDR();
uint8_t IOB_UART_GET_TXREADY();
uint8_t IOB_UART_GET_RXREADY();
uint8_t IOB_UART_GET_RXDATA();
uint16_t IOB_UART_GET_VERSION();

void iob_write(unsigned int address, unsigned data_w, unsigned int cpu_data);
unsigned int iob_read(unsigned int address, unsigned int data_w);

#endif // H_IOB_UART__CSRS_H
