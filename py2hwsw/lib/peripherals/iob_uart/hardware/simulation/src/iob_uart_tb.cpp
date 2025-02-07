// SPDX-FileCopyrightText: 2024 IObundle
//
// SPDX-License-Identifier: MIT

#include "Viob_uart.h"
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <verilated.h>

#include "iob_tasks.h"

#if (VM_TRACE == 1) // If verilator was invoked with --trace
#include <verilated_vcd_c.h>
#endif

#define MAX_SIM_TIME 120000

extern vluint64_t main_time;
extern timer_settings_t task_timer_settings;

//////////////////////////////////////////
Viob_uart *dut = new Viob_uart;

// extern "C"
int iob_uart_core_tb();

//////////////////////////////////////////

void call_eval() { dut->eval(); }

#if (VM_TRACE == 1)
#if (VM_TRACE_FST == 1)
VerilatedFstC *tfp = new VerilatedFstC; // Create tracing object
#else
VerilatedVcdC *tfp = new VerilatedVcdC; // Create tracing object
#endif

void call_dump(vluint64_t time) { tfp->dump(time); }
#endif

double sc_time_stamp() { // Called by $time in Verilog
  return main_time;
}

// uart interface
iob_native_t uart_if = {&dut->iob_uart_csrs_iob_valid_i,
                        &dut->iob_uart_csrs_iob_addr_i,
                        UCHAR,
                        &dut->iob_uart_csrs_iob_wdata_i,
                        &dut->iob_uart_csrs_iob_wstrb_i,
                        &dut->iob_uart_csrs_iob_rdata_o,
                        &dut->iob_uart_csrs_iob_rvalid_o,
                        &dut->iob_uart_csrs_iob_ready_o};

void iob_hard_reset() {
  dut->clk_i = 0;
  dut->cke_i = 1;
  dut->arst_i = 0;
  for (int i = 0; i < 100; i++)
    Timer(CLK_PERIOD);
  dut->arst_i = 1;
  for (int i = 0; i < 100; i++)
    Timer(CLK_PERIOD);
  dut->arst_i = 0;
}

int main(int argc, char **argv) {

  Verilated::commandArgs(argc, argv); // Init verilator context
  task_timer_settings.clk = &dut->clk_i;
  task_timer_settings.eval = call_eval;
#if (VM_TRACE == 1)
  task_timer_settings.dump = call_dump;
#endif

#if (VM_TRACE == 1)
  Verilated::traceEverOn(true); // Enable tracing
  dut->trace(tfp, 1);
  tfp->open("uut.vcd");
#endif

  int failed = 0;
  iob_hard_reset();
  //
  // CALL THE CORE TEST BENCH
  //

  failed = iob_uart_core_tb();

  dut->final();

#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump last values
  tfp->close();         // Close tracing file
  std::cout << "Generated vcd file" << std::endl;
  delete tfp;
#endif

  delete dut;

  // create test log file
  FILE *log = fopen("test.log", "w");
  if (failed != 0) {
    fprintf(log, "Test failed!");
  } else {
    fprintf(log, "Test passed!");
  }
  fclose(log);

  exit(failed);
}
