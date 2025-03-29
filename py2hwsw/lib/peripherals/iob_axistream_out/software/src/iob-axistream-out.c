/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob-axistream-out.h"

void iob_axis_out_reset() {
  iob_axistream_out_set_soft_reset(1);
  iob_axistream_out_set_soft_reset(0);
}

uint32_t iob_axis_write(uint32_t value) {
  if (iob_axistream_out_get_fifo_full()) {
    return 0;
  } else {
    iob_axistream_out_set_data(value);
    return 1;
  }
}
