/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_plic.h"
#include "iob_printf.h"
#include "iob_system_conf.h"
#include "iob_system_mmap.h"
#include "iob_timer.h"
#include "iob_uart.h"
#include "riscv-csr.h"
#include "riscv-interrupts.h"
#include <stdint.h>
#include <string.h>

// Volatile flag to signal interrupt arrival
static volatile int timer_triggered = 0;

// Interrupt Service Routine (ISR)
// The 'interrupt("machine")' attribute tells the compiler to save and restore
// registers and return using 'mret'.
void irq_handler(void) __attribute__((interrupt("machine")));

// Force alignment of the trap handler to 4 bytes, as required for mtvec.BASE
#pragma GCC push_options
#pragma GCC optimize("align-functions=4")
void irq_handler(void) {
  // Read mcause to check if it's an external interrupt
  uint_xlen_t mcause = csr_read_mcause();
  if ((mcause & MCAUSE_INTERRUPT_BIT_MASK) &&
      ((mcause & 0xFF) == RISCV_INT_POS_MEI)) {
    // Claim the interrupt from PLIC
    int source_id = plic_claim_interrupt(0);
    printf("Detected interrupt. Source ID: %d.\n", source_id);

    // Source ID 1 is the TIMER0_INTERRUPT
    if (source_id == 1) {
      timer_triggered = 1;
      // Disable timer interrupt to avoid continuous triggering
      timer_set_interrupt(0);
    }

    // Complete the interrupt in PLIC
    plic_complete_interrupt(0, source_id);
  }
}
#pragma GCC pop_options

char *send_string = "Sending this string as a file to console.\n"
                    "The file is then requested back from console.\n"
                    "The sent file is compared to the received file to confirm "
                    "correct file transfer via UART using console.\n"
                    "Generating the file in the firmware creates an uniform "
                    "file transfer between pc-emul, simulation and fpga without"
                    " adding extra targets for file generation.\n";

int main() {
  char pass_string[] = "Test passed!";
  char fail_string[] = "Test failed!";

  // init timer
  timer_init(TIMER0_BASE);

  // init uart
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);
  printf_init(&uart_putc);

  // Initialize PLIC
  plic_init(PLIC0_BASE);

  // test puts
  uart_puts("\n\n\nHello world!\n\n\n");

  // --- Interrupt Demo Setup ---
  printf("Setting up Timer interrupt via PLIC...\n");

  // Configure CPU to handle interrupts
  csr_write_mtvec((uint_xlen_t)irq_handler);

  // Enable External Interrupts in CPU (MIE.MEIE)
  csr_set_bits_mie(MIE_MEI_BIT_MASK);

  // Enable Global Interrupts in CPU (MSTATUS.MIE)
  csr_set_bits_mstatus(MSTATUS_MIE_BIT_MASK);

  // Enable source ID 1 (Timer 0) in PLIC
  plic_enable_interrupt(0, 1);

  unsigned long long elapsed = timer_get_count();
  // printf("\Current timer count: %d clock cycles\n", (unsigned int)elapsed);

  // Set timer threshold for ~+1ms
  timer_set_interrupt(elapsed + (IOB_BSP_FREQ / 1000));

  // Wait for interrupt
  printf("Waiting for timer interrupt...\n");
  while (!timer_triggered)
    ;
  printf("SUCCESS: Timer interrupt received and handled by PLIC!\n\n");
  // ----------------------------

  // test printf with floats
  printf("Value of Pi = %f\n\n", 3.1415);

// Don't transfer files when running alongside tester
#ifndef TESTER
  // test file send
  char *sendfile = malloc(1000);
  int send_file_size = 0;
  send_file_size = strlen(strcpy(sendfile, send_string));
  uart_sendfile("Sendfile.txt", send_file_size, sendfile);

  // test file receive
  char *recvfile = malloc(10000);
  int file_size = 0;
  file_size = uart_recvfile("Sendfile.txt", recvfile);

  // compare files
  if (strcmp(sendfile, recvfile)) {
    printf("FAILURE: Send and received file differ!\n");
  } else {
    printf("SUCCESS: Send and received file match!\n");
  }

  free(sendfile);
  free(recvfile);

  uart_sendfile("test.log", strlen(pass_string), pass_string);
#endif // TESTER

  // read current timer count, compute elapsed time
  elapsed = timer_get_count();
  unsigned int elapsedu = elapsed / (IOB_BSP_FREQ / 1000000);

  printf("\nExecution time: %d clock cycles\n", (unsigned int)elapsed);
  printf("\nExecution time: %dus @%dMHz\n\n", elapsedu, IOB_BSP_FREQ / 1000000);

  uart_finish();
}
