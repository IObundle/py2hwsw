/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_axistream_in_csrs.h"
#include "iob_axistream_out_csrs.h"
#include <stdio.h>

#define FREQ 100000000
#define BAUD 3000000

#define NWORDS 256

int iob_core_tb() {
  int failed = 0;
  uint32_t i, word;

  // print welcome message
  printf("IOb AXI-Stream testbench\n");

  // print the reset message
  printf("Reset complete\n");

  // axistream_in connected to first manager of split
  iob_axistream_in_csrs_init_baseaddr(0);
  // axistream_out connected to second manager of split
  iob_axistream_out_csrs_init_baseaddr(1 << 5);

  printf("Configure AXIStream IN\n");
  iob_axistream_in_csrs_set_soft_reset(0);
  iob_axistream_in_csrs_set_mode(0);
  iob_axistream_in_csrs_set_enable(1);

  printf("Configure AXIStream OUT\n");
  iob_axistream_out_csrs_set_soft_reset(0);
  iob_axistream_out_csrs_set_mode(0);
  iob_axistream_out_csrs_set_nwords(NWORDS);
  iob_axistream_out_csrs_set_enable(1);

  printf("Write data to AXIStream OUT\n");

  // write data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    iob_axistream_out_csrs_set_data(i);
  }

  printf("Read data from AXIStream IN\n");

  // read data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    word = iob_axistream_in_csrs_get_data();

    // check data
    if (word != i) {
      printf("Error: expected %d, got %d\n", i, word);
      failed = failed + 1;
    }
  }

  return failed;
}
