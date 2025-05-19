/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_s_axi_m.h"

#include <stdio.h>

#define FREQ 100000000
#define BAUD 3000000

#define NWORDS 256
// Start 96 words to 4kB to test crossing the 4kB boundary
#define START_ADDR 0xF60
#define BURST_SIZE 64

int iob_core_tb() {
  int failed = 0;
  uint32_t i, word;

  // print welcome message
  printf("IOb Slave to AXI master converter testbench\n");

  // Converter connected to first master of split
  iob_s_axi_m_init_baseaddr(0);
  // Converter controller connected to second master of split
  iob_s_axi_m_controller_init_baseaddr(1 << 16);

  printf("Set burst length to %d\n", BURST_SIZE);
  iob_s_axi_m_set_burst_length(BURST_SIZE);

  printf("Reset the converter\n");
  iob_s_axi_m_reset();

  printf("Write data to Converter\n");
  // write data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    // write data
    iob_s_axi_m_write_32b_data(START_ADDR + i * 4, i);
  }

  // wait for write to finish
  while (iob_s_axi_m_get_w_level() > 0) {
    // wait
  }

  // read data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    // read data
    word = iob_s_axi_m_read_32b_data(START_ADDR + i * 4);
    if (word != i) {
      printf("Error: Read %d, expected %d\n", word, i);
      failed = 1;
    }
  }

  return failed;
}
