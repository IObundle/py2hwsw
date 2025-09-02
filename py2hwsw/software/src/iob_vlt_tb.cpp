/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include <verilated.h>
#if (VM_TRACE == 1) // If verilator was invoked with --trace
#if (VM_TRACE_FST == 1)
#include <verilated_fst_c.h>
#else
#include <verilated_vcd_c.h>
#endif
#endif

#include "Viob_uut.h" //user file that defins the dut

#ifndef CLK_PERIOD
#define FREQ 100000000
#define CLK_PERIOD 1000000000 / FREQ // Example: 1/100MHz*10^9 = 10 ns
#endif

#if (VM_TRACE == 1)
#if (VM_TRACE_FST == 1)
VerilatedFstC *tfp = new VerilatedFstC; // Create tracing object
#else
VerilatedVcdC *tfp = new VerilatedVcdC; // Create tracing object
#endif
#endif

// simulation time
vluint64_t sim_time = 0;

// Delayed start time of VCD trace dump
// Used to avoid large VCD dump files during long simulations
#if (VM_TRACE == 1)
vluint64_t vcd_delayed_start = 0;
#endif

Viob_uut *dut = new Viob_uut; // Create instance of module

int iob_core_tb();

// Clock tick
void clk_tick(unsigned int n = 1) {
  for (unsigned int i = 0; i < n; i++) {
    dut->eval();
#if (VM_TRACE == 1)
    tfp->dump(sim_time); // Dump values into tracing file
#endif
    sim_time += CLK_PERIOD / 2;
    dut->clk_i = !dut->clk_i; // negedge
    dut->eval();
#if (VM_TRACE == 1)
    tfp->dump(sim_time);
#endif
    sim_time += CLK_PERIOD / 2;
    dut->clk_i = !dut->clk_i; // posedge
    dut->eval();
  }
}

// Reset dut
void iob_hard_reset() {
  dut->clk_i = 1;
  dut->cke_i = 0;
  dut->arst_i = 0;
  clk_tick(100);
  dut->arst_i = 1;
  clk_tick(100);
  dut->arst_i = 0;
  dut->cke_i = 1;
  clk_tick(100);
}

// Write data to IOb Native subordinate
void iob_write(unsigned int address, unsigned data_w, unsigned int data) {

  unsigned int nbytes = data_w / 8 + (data_w % 8 ? 1 : 0);

  dut->iob_addr_i = address; // remove byte address
  dut->iob_valid_i = 1;
  switch (nbytes) {
  case 1:
    dut->iob_wstrb_i = 0x1 << (address & 0x3);
    dut->iob_wdata_i = data << ((address & 0x3) * 8);
    break;
  case 2:
    dut->iob_wstrb_i = 0x3 << (address & 0x2);
    dut->iob_wdata_i = data << ((address & 0x2) * 8);
    break;
  default:
    dut->iob_wstrb_i = 0xF;
    dut->iob_wdata_i = data;
    break;
  }
  dut->eval(); // Some cores may change ready when they receive valid
  while (dut->iob_ready_o == 0) {
    clk_tick();
  }
  clk_tick();
  dut->iob_valid_i = 0;
  dut->iob_wstrb_i = 0;
}

// Read data from IOb Native subordinate
unsigned int iob_read(unsigned int address, unsigned int data_w) {

  unsigned int nbytes = data_w / 8 + (data_w % 8 ? 1 : 0);
  unsigned int data;

  dut->iob_addr_i = address; // remove byte address
  dut->iob_valid_i = 1;
  dut->eval(); // Some cores may change ready when they receive valid
  while (dut->iob_ready_o == 0) {
    clk_tick();
  }
  clk_tick();
  dut->iob_valid_i = 0;
  while (dut->iob_rvalid_o == 0) {
    clk_tick();
  }
  switch (nbytes) {
  case 1:
    data = (dut->iob_rdata_o >> ((address & 0x3) * 8)) & 0xFF;
    break;
  case 2:
    data = (dut->iob_rdata_o >> ((address & 0x2) * 8)) & 0xFFFF;
    break;
  default:
    data = dut->iob_rdata_o;
    break;
  }
  clk_tick();
  return data;
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
