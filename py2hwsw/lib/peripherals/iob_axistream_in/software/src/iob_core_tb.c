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

int iob_core_tb() {
  int failed = 0;
  uint32_t i, word;

  // print welcome message
  printf("IOb AXI-Stream testbench\n");

  // print the reset message
  printf("Reset complete\n");

  iob_axistream_in_init_baseaddr(0);
  iob_axistream_out_init_baseaddr(TODO);

  printf("Configure AXIStream IN");
  iob_axistream_in_csrs_set_softreset(0);
  iob_axistream_in_csrs_set_mode(0);
  // iob_axistream_in_csrs_set_nwords(NWORDS);
  iob_axistream_in_csrs_enable(1);

  printf("Configure AXIStream OUT");
  iob_axistream_out_csrs_set_softreset(0);
  iob_axistream_out_csrs_set_mode(0);
  iob_axistream_out_csrs_set_nwords(NWORDS);
  iob_axistream_out_csrs_enable(1);

  printf("Write data to AXIStream OUT");

  // write data loop
  for (i = 0; i < 256; i = i + 1) {
    iob_axistream_out_csrs_set_data(i);
  }

  printf("Read data from AXIStream IN");

  // read data loop
  for (i = 0; i < 256; i = i + 1) {
    word = iob_axistream_in_csrs_get_data();

    // check data
    if (word != i) {
      printf("Error: expected %d, got %d", i, word);
      failed = failed + 1;
    }
  }

  return failed;
}
