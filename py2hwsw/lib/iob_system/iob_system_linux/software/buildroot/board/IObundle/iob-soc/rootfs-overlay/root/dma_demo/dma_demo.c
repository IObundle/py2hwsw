/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/*********************************************************
 *                   DMA demo Program                    *
 *********************************************************/

// #include "bsp.h"
#include "iob-axistream-in-user.h"
#include "iob-axistream-out-user.h"
#include "iob-dma-user.h"

#include <stdio.h>
#include <stdlib.h>

// We should ideally receive the INIT_MEM information from the PC
// However, since most of the time we run linux on the FPGA,
// the INIT_MEM will be 0, therefore we hardcode it for now.
#undef IOB_SYSTEM_LINUX_INIT_MEM

void send_axistream();
void receive_axistream();

int main() {
  // init axistream
  iob_sysfs_write_file(IOB_AXISTREAM_IN_SYSFILE_ENABLE, 1);
  iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_ENABLE, 1);

  // Send byte stream via AXI stream
  send_axistream();
  // Read byte stream via AXI stream
  receive_axistream();
}

void send_axistream() {
  uint8_t i;
  uint8_t words_in_byte_stream = 4;
  // Allocate memory for byte stream
  uint32_t *byte_stream =
      (uint32_t *)malloc(words_in_byte_stream * sizeof(uint32_t));
  // Fill byte stream to send
  byte_stream[0] = 0x03020100;
  byte_stream[1] = 0x07060504;
  byte_stream[2] = 0xbbaa0908;
  byte_stream[3] = 0xffeeddcc;

  // Print byte stream to send
  printf("Sending AXI stream bytes: ");
  for (i = 0; i < words_in_byte_stream; i++)
    printf("0x%08x ", byte_stream[i]);
  printf("\n");

  // Send bytes to AXI stream output via DMA
  printf("Loading AXI words via DMA...\n\n");
  iob_axis_out_reset();
  iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_ENABLE, 1);
  iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_MODE, 1);
  iob_sysfs_write_file(IOB_AXISTREAM_OUT_SYSFILE_NWORDS, words_in_byte_stream);
  dma_start_transfer(byte_stream, words_in_byte_stream, 0, 0);

  free(byte_stream);
}

void receive_axistream() {
  uint8_t i;
  uint32_t n_received_words = 0;
  iob_sysfs_read_file(IOB_AXISTREAM_IN_SYSFILE_NWORDS, &n_received_words);

  // Allocate memory for byte stream
  volatile uint32_t *byte_stream =
      (volatile uint32_t *)malloc((n_received_words) * sizeof(uint32_t));
  for (i = 0; i < n_received_words; i++)
    byte_stream[i] = 0;

  // Transfer bytes from AXI stream input via DMA
  printf("Storing AXI words via DMA...\n");
  iob_sysfs_write_file(IOB_AXISTREAM_IN_SYSFILE_MODE, 1);
  dma_start_transfer((uint32_t *)byte_stream, n_received_words, 1, 0);

  // clear_cache();

  // Print byte stream received
  printf("Received AXI stream %d bytes: ", n_received_words * 4);
  for (i = 0; i < n_received_words; i++)
    printf("0x%08x ", byte_stream[i]);
  printf("\n\n");

  free((uint32_t *)byte_stream);
}
