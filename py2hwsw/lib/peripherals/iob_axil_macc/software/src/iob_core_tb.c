/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_axil_macc_csrs.h"
#include <stdio.h>

int iob_core_tb() {

  // print welcome message
  printf("IOB AXIL MACC testbench\n");

  iob_axil_macc_csrs_set_load(1);
  iob_axil_macc_csrs_set_a(1);
  iob_axil_macc_csrs_set_b(2);

  iob_axil_macc_csrs_set_en(1);
  while (!iob_axil_macc_csrs_get_done())
    ;
  iob_axil_macc_csrs_set_en(0);
  iob_axil_macc_csrs_set_load(0);

  int i;

  for (i = 0; i < 10; i++) {
    iob_axil_macc_csrs_set_a(i + 3);
    iob_axil_macc_csrs_set_b(i + 4);
    iob_axil_macc_csrs_set_en(1);
    while (!iob_axil_macc_csrs_get_done())
      ;
    iob_axil_macc_csrs_set_en(0);
  }

  int acc_hw;
  acc_hw = iob_axil_macc_csrs_get_c();

  // compute in sw
  int acc = 2;
  for (i = 0; i < 10; i++)
    acc += (i + 3) * (i + 4);

  if (acc == acc_hw) {
    printf("SW and HW computation match\n");
    return 0;
  } else {
    printf("Error: SW and HW computation do not match\n");
    printf("Expected %d, got %d\n", acc, acc_hw);
    return 1;
  }
}
