/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/** @file iob_uart.h
 *  @brief High level iob_uart core functions
 *
 * The present IOb-UART software drivers implement a way to interface with the
 * IOb-UART peripheral for serial communication.
 *
 * The present drivers provide base functionalities such as:
 *      - initialization and setup
 *      - basic control functions
 *      - single character send and receive functions
 *      - simple protocol for multi byte transfers
 *
 */

#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>

#include "iob_uart_csrs.h"

/**
 * @def UART_PROGNAME
 * @brief Prefix to IOb-UART specific prints.
 */
#define UART_PROGNAME "IOb-UART"

// UART commands
/**
 * @def STX
 * @brief Start text.
 * Signal start of data sequence to be printed.
 */
/**
 * @def ETX
 *
 * @brief End text.
 * Signal end of data sequence to be printed.
 */
/**
 * @def EOT
 *
 * @brief End of transmission.
 * Signal end of UART connection.
 */
/**
 * @def ENQ
 *
 * @brief Enquiry.
 * Signal start of UART connection.
 */
/**
 * @def ACK
 *
 * @brief Acknowledge.
 * Signal reception of incomming message.
 */
/**
 * @def FTX
 *
 * @brief File transfer.
 * Signal file transfer request.
 */
/**
 * @def FRX
 *
 * @brief File reception.
 * Signal file reception request.
 */
#define STX 2 // start text
#define ETX 3 // end text
#define EOT 4 // end of transission
#define ENQ 5 // enquiry
#define ACK 6 // acklowledge
#define FTX 7 // transmit file
#define FRX 8 // receive file

// UART functions

/** @brief Initialize UART.
 *
 * Reset UART, set IOb-Uart base address and set the division factor.
 * The division factor is the number of clock cycles per simbol transfered.
 *
 * For example, for a case with fclk = 100 Mhz for a baudrate of 115200 we
 * should have `div=(100*10^6/115200) = (868)`.
 *
 * @param base_address IOb-Uart instance base address in the system.
 * @param div Equal to round (fclk/baudrate).
 * @return void.
 */
void uart_init(int base_address, uint16_t div);

/** @brief Close transmission.
 *
 * Send end of transmission (EOT) command via UART.
 * Active wait until TX transfer is complete.
 * Use this function to close console program.
 *
 * @return void.
 */
void uart_finish();

/** @brief Wait for TX.
 *
 * Active wait until TX is ready to process new byte to send.
 *
 * @return void.
 */
void uart_txwait();

/** @brief Print char.
 *
 * Send character via UART to be printed by in console program.
 *
 * @param c Character to print.
 * @return void.
 */
void uart_putc(char c);

/** @brief Print string.
 *
 * Send string via UART to be printed by in console program.
 *
 * @param s Pointer to char array to be printed.
 * @return void.
 */
void uart_puts(const char *s);

/** @brief Send file.
 *
 * Send variable size file via UART.
 * Order of commands:
 *  1. Send file transmit (FTX) comnand.
 *  2. Send file_name.
 *  3. Send file_size (in little endian format).
 *  4. Send file.
 *
 * @param file_name Pointer to file name string.
 * @param file_size Size of file to be sent.
 * @param mem Pointer to file.
 * @return void.
 */
void uart_sendfile(char *file_name, int file_size, char *mem);

/** @brief Wait for RX Data.
 *
 * Active wait for RX incomming data.
 *
 * @return void.
 */
void uart_rxwait();

/** @brief Get char.
 *
 * Active wait and receive char/byte from UART.
 *
 * @return received byte from UART.
 */
uint8_t uart_getc();

/** @brief Receive file.
 *
 * Request variable size file via UART.
 * Order of commands:
 *  1. Send file receive (FRX) command.
 *  2. Send file_name.
 *  3. Receive file_size (in little endian format).
 *  4. Send ACK command.
 *  5. Receive file.
 *
 * If memory pointer is not inicialized, allocates memory for incomming file.
 *
 * @param file_name Pointer to file name string.
 * @param mem Pointer in memory to store incomming file.
 * @return Size of received file.
 */
uint32_t uart_recvfile(char *file_name, char *mem);
