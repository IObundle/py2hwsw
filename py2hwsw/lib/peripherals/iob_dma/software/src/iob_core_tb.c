/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_axistream_in_csrs.h"
#include "iob_axistream_out_csrs.h"
#include "iob_dma.h"
#include "iob_dma_csrs.h"

#include <stdio.h>

#define NWORDS 512
#define RAM_ADDR 4000

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

  unsigned int version, major, minor;
  uint32_t i, word;

  // Check versions
  // read version 20 times to burn time
  for (i = 0; i < 20; i++) {

    version = iob_dma_csrs_get_version();
  }
  major = version >> 16;
  minor = version & 0xFF;
  printf("DMA Version is %x.%x\n", major, minor);

  // 1. CPU -> AXIS OUT -> AXIS IN data transfer
  printf("1.1. Configure AXIStream IN\n");
  iob_axistream_in_csrs_set_soft_reset(1);
  iob_axistream_in_csrs_set_soft_reset(0);
  iob_axistream_in_csrs_set_mode(1);
  iob_axistream_in_csrs_set_enable(1);

  printf("1.2. Configure AXIStream OUT\n");
  iob_axistream_out_csrs_set_soft_reset(1);
  iob_axistream_out_csrs_set_soft_reset(0);
  iob_axistream_out_csrs_set_mode(0);
  iob_axistream_out_csrs_set_nwords(NWORDS);
  iob_axistream_out_csrs_set_enable(1);

  printf("1.3. Write data to AXIStream OUT\n");

  // write data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    iob_axistream_out_csrs_set_data(i);
  }

  // wait for data in AXIS IN
  while (iob_axistream_in_csrs_get_nwords() < NWORDS)
    ;
  // 2. Configure AXIS IN -> DMA -> AXI RAM write operation
  printf("2.1. Configure DMA write transfer\n");
  iob_dma_csrs_set_w_burstlen(100);
  dma_write_transfer((uint32_t *)RAM_ADDR, NWORDS);

  // 3. Wait for DMA transfer complete
  printf("3. Wait for DMA write transfer complete...");
  while (dma_write_busy())
    ;
  printf("done!\n");

  // 4. Configure AXIS OUT <- DMA <- AXI RAM read operation
  printf("4.1. Configure AXIStream IN\n");
  iob_axistream_in_csrs_set_soft_reset(1);
  iob_axistream_in_csrs_set_soft_reset(0);
  iob_axistream_in_csrs_set_mode(0);
  iob_axistream_in_csrs_set_enable(1);

  printf("4.2. Configure AXIStream OUT\n");
  iob_axistream_out_csrs_set_soft_reset(1);
  iob_axistream_out_csrs_set_soft_reset(0);
  iob_axistream_out_csrs_set_mode(1);
  iob_axistream_out_csrs_set_nwords(NWORDS);
  iob_axistream_out_csrs_set_enable(1);

  printf("4.3. Configure DMA read transfer\n");
  iob_dma_csrs_set_r_burstlen(200);
  dma_read_transfer((uint32_t *)RAM_ADDR, NWORDS);

  // 5. Wait for DMA transfer complete
  printf("5. Wait for DMA read transfer complete...");
  while (dma_read_busy())
    ;
  printf("done!\n");

  // 6. Read data from AXIS IN and validate
  printf("6. Read data from AXIStream IN\n");
  // read data loop
  for (i = 0; i < NWORDS; i = i + 1) {
    word = iob_axistream_in_csrs_get_data();

    // check data
    if (word != i) {
      printf("Error: expected %d, got %d\n", i, word);
      failed = failed + 1;
    }
  }

  printf("DMA test complete.\n");
  return failed;
}
