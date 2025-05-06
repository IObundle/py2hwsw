/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_axistream_in.h"

void iob_axis_in_reset() {
  iob_axistream_in_csrs_set_soft_reset(1);
  iob_axistream_in_csrs_set_soft_reset(0);
}

uint32_t iob_axis_read(uint32_t *value) {
  if (iob_axistream_in_csrs_get_fifo_empty()) {
    return 0;
  } else {
    *value = iob_axistream_in_csrs_get_data();
    return 1;
  }
}
