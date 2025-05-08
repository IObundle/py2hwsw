/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_axistream_in_csrs.h"
#include "iob_axistream_out_csrs.h"
#include "iob_dma_csrs.h"
#include <stdio.h>

int iob_core_tb() {

  int failed = 0;

  // print welcome message
  printf("IOB DMA testbench\n");

  // print the reset message
  printf("Reset complete\n");

  //
  // axistream_in connected to first master of split
  iob_axistream_in_csrs_init_baseaddr(0);
  // axistream_out connected to second master of split
  iob_axistream_out_csrs_init_baseaddr(1 << 5);
  // dma connected to third master of split
  iob_dma_csrs_init_baseaddr(2 << 5);

  unsigned int version;
  int i;

  // Check versions
  version = iob_axistream_in_csrs_get_version();
  printf("AXIS IN Version is %d\n", version);
  version = iob_axistream_out_csrs_get_version();
  printf("AXIS OUT Version is %d\n", version);
  // read version 20 times to burn time
  for (i = 0; i < 20; i++) {
    version = iob_dma_csrs_get_version();
  }
  printf("DMA Version is %d\n", version);

  printf("DMA test complete.\n");
  return failed;
}
