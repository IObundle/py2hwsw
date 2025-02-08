/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <verilated.h>
#if (VM_TRACE == 1) // If verilator was invoked with --trace
#include <verilated_vcd_c.h>
#endif
#include "iob_vlt_tb.h" //user file that defins the dut

#include "iob_bsp.h"

#ifndef CLK_PERIOD
#define CLK_PERIOD 1000000000 / FREQ // Example: 1/100MHz*10^9 = 10 ns
#endif

#if (VM_TRACE == 1)
#if (VM_TRACE_FST == 1)
VerilatedFstC *tfp = new VerilatedFstC; // Create tracing object
#else
VerilatedVcdC *tfp = new VerilatedVcdC; // Create tracing object
#endif
#endif

/*
double sc_time_stamp() { // Called by $time in Verilog
  return main_time;
}
*/

// simulation time
vluint64_t sim_time = 0;

// Delayed start time of VCD trace dump
// Used to avoid large VCD dump files during long simulations
#if (VM_TRACE == 1)
vluint64_t vcd_delayed_start = 0;
#endif

dut_t *dut = new dut_t;

// Clock tick
void clk_tick(unsigned int n = 1) {
  for (unsigned int i = 0; i < n; i++) {
    dut->clk_i = !dut->clk_i;
    dut->eval();
    sim_time += CLK_PERIOD / 2;
#if (VM_TRACE == 1)
    tfp->dump(sim_time); // Dump values into tracing file
#endif
    dut->clk_i = !dut->clk_i;
    dut->eval();
    sim_time += CLK_PERIOD / 2;
#if (VM_TRACE == 1)
    tfp->dump(sim_time);
#endif
  }
}

// Reset dut
void iob_hard_reset() {
  dut->clk_i = 0;
  dut->cke_i = 0;
  dut->arst_i = 0;
  dut->eval();
  clk_tick(100);
  dut->arst_i = 1;
  dut->eval();
  clk_tick(100);
  dut->arst_i = 0;
  dut->cke_i = 1;
#if (VM_TRACE == 1)
  tfp->dump(sim_time);
#endif
}

// Write data to IOb Native slave
void iob_write(unsigned int cpu_address, unsigned cpu_data_w,
               unsigned int cpu_data) {

  unsigned int nbytes = cpu_data_w / 8 + (cpu_data_w % 8 ? 1 : 0);

  dut->csrs_iob_addr_i = cpu_address;
  dut->csrs_iob_valid_i = 1;
  switch (nbytes) {
  case 1:
    dut->csrs_iob_wstrb_i = 0x1 << (cpu_address & 0x3);
    dut->csrs_iob_wdata_i = cpu_data << ((cpu_address & 0x3) * 8);
    break;
  case 2:
    dut->csrs_iob_wstrb_i = 0x3 << (cpu_address & 0x2);
    break;
  default:
    dut->csrs_iob_wstrb_i = 0xF;
    dut->csrs_iob_wdata_i = cpu_data;
    break;
  }
  while (dut->csrs_iob_ready_o == 0) {
    clk_tick();
  }
  dut->csrs_iob_valid_i = 0;
  dut->csrs_iob_wstrb_i = 0;
  clk_tick();
}

// Read data from IOb Native slave
unsigned int iob_read(unsigned int cpu_address, unsigned int cpu_data_w) {

  unsigned int nbytes = cpu_data_w / 8 + (cpu_data_w % 8 ? 1 : 0);
  unsigned int cpu_data;

  dut->csrs_iob_addr_i = cpu_address;
  dut->csrs_iob_valid_i = 1;
  while (dut->csrs_iob_ready_o == 0) {
    clk_tick();
  }
  dut->csrs_iob_valid_i = 0;
  clk_tick();
  switch (nbytes) {
  case 1:
    cpu_data = (dut->csrs_iob_rdata_o >> ((cpu_address & 0x3) * 8)) & 0xFF;
    break;
  case 2:
    cpu_data = (dut->csrs_iob_rdata_o >> ((cpu_address & 0x2) * 8)) & 0xFFFF;
    break;
  default:
    cpu_data = dut->csrs_iob_rdata_o;
    break;
  }
  return cpu_data;
}

int main(int argc, char **argv) {

  Verilated::commandArgs(argc, argv); // Init verilator context

#if (VM_TRACE == 1)
  Verilated::traceEverOn(true); // Enable tracing
  dut->trace(tfp, 1);
  tfp->open("uut.vcd");
#endif

  // hardware reset
  iob_hard_reset();

  //
  // CALL THE CORE TEST BENCH
  //
  int failed = iob_core_tb();

  // create test log file
  FILE *log = fopen("test.log", "w");
  if (failed != 0) {
    fprintf(log, "Test failed!");
  } else {
    fprintf(log, "Test passed!");
  }
  fclose(log);

  // terminate simulation and generate trace file
  dut->final();

#if (VM_TRACE == 1)
  tfp->close(); // Close tracing file
  fprintf(stdout, "Trace file created: uut.vcd\n");
  delete tfp;
#endif

  delete dut;

  exit(failed);
}
