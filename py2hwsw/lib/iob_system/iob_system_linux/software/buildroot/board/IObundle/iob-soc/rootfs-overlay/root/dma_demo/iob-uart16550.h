/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>

#define UART_PROGNAME "IOb-UART"

// UART commands
#define STX 2 // start text
#define ETX 3 // end text
#define EOT 4 // end of transission
#define ENQ 5 // enquiry
#define ACK 6 // acklowledge
#define FTX 7 // transmit file
#define FRX 8 // receive file

// UART functions

// Init UART
void uart16550_init(char device_path[]);

// Close transmission
void uart16550_finish();

// Print char
void uart16550_putc(char c);

// Print string
void uart16550_puts(const char *s);

// Send file
void uart16550_sendfile(char *file_name, int file_size, char *mem);

// Get char
char uart16550_getc();

// Receive file
int uart16550_recvfile(char *file_name, char *mem);
