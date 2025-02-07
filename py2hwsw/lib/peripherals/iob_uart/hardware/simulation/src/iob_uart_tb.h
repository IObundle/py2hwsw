/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_uart_csrs.h"

// Core Setters and Getters
void IOB_UART_SET_SOFTRESET(uint8_t value);

void IOB_UART_SET_DIV(uint16_t value);

void IOB_UART_SET_TXDATA(uint8_t value);

void IOB_UART_SET_TXEN(uint8_t value);

void IOB_UART_SET_RXEN(uint8_t value);

uint8_t IOB_UART_GET_TXREADY();

uint8_t IOB_UART_GET_RXREADY();

uint8_t IOB_UART_GET_RXDATA();

uint16_t IOB_UART_GET_VERSION();
