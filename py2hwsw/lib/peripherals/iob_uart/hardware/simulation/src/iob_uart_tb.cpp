// SPDX-FileCopyrightText: 2024 IObundle
//
// SPDX-License-Identifier: MIT

#include "Viob_uart.h"
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <verilated.h>

#if (VM_TRACE == 1) // If verilator was invoked with --trace
#include <verilated_vcd_c.h>
#endif

#define MAX_SIM_TIME 120000

vluint64_t main_time = 0;
Viob_uart *dut;
VerilatedVcdC *tfp;

extern "C" {
int iob_uart_core_tb();
}

double sc_time_stamp() { // Called by $time in Verilog
  return main_time;
}

void tick() {
  if (main_time >= MAX_SIM_TIME) {
#if (VM_TRACE == 1)
    tfp->dump(main_time); // Dump last values
    tfp->close();         // Close tracing file
    std::cout << "Generated vcd file" << std::endl;
    delete tfp;
#endif

    throw std::runtime_error(
        "Simulation time exceeded maximum simulation time");
  }
  dut->clk_i = !dut->clk_i;
  dut->eval();
#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump values into tracing file
#endif
  main_time++;
  dut->clk_i = !dut->clk_i;
  dut->eval();
#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump values into tracing file
#endif
  main_time++;
}

void iob_arst_pulse() {
  dut->clk_i = 0;
  dut->cke_i = 1;
  dut->arst_i = 0;
  tick();
  dut->arst_i = 1;
  for (uint32_t i = 0; i < 8; i++) {
    tick();
  }
  dut->arst_i = 0;
  tick();
}

// write to the UART
void iob_write(uint32_t addr, uint8_t size, uint32_t data) {

  // compute wstrb from size and address (assumes 32-bit bus)
  uint8_t wstrb = 0;
  if (size == 32) {
    wstrb = 0xF;
  } else if (size == 16) {
    wstrb = 0x3 << (addr & 0x2);
  } else if (size == 8) {
    wstrb = 0x1 << (addr & 0x3);
  }

  dut->iob_uart_csrs_iob_valid_i = 1;
  dut->iob_uart_csrs_iob_addr_i = addr;
  dut->iob_uart_csrs_iob_wdata_i = data;
  dut->iob_uart_csrs_iob_wstrb_i = wstrb;
  tick();
  while (!dut->iob_uart_csrs_iob_ready_o) {
    tick();
  }
  dut->iob_uart_csrs_iob_valid_i = 0;
  tick();
}

// read from the UART
uint32_t iob_read(uint32_t addr, uint8_t size) {
  dut->iob_uart_csrs_iob_valid_i = 1;
  dut->iob_uart_csrs_iob_addr_i = addr;
  dut->iob_uart_csrs_iob_wstrb_i = 0;
  tick();
  while (!dut->iob_uart_csrs_iob_ready_o) {
    tick();
  }
  dut->iob_uart_csrs_iob_valid_i = 0;
  int data = dut->iob_uart_csrs_iob_rdata_o;

  if (size == 16) {
    data = (data >> (addr & 0x2)) & 0xFFFF;
  } else if (size == 8) {
    return (data >> (addr & 0x3)) & 0xFF;
  }
  tick();
  return data;
}

int main(int argc, char **argv) {

  Verilated::commandArgs(argc, argv); // Init verilator context
  dut = new Viob_uart;                // Create DUT object

#if (VM_TRACE == 1)
  Verilated::traceEverOn(true); // Enable tracing
  tfp = new VerilatedVcdC;      // Create tracing object
  dut->trace(tfp, 99);          // Trace 99 levels of hierarchy
  tfp->open("uut.vcd");         // Open tracing file
#endif

  //
  // CALL THE CORE TEST BENCH
  //
  int failed = iob_uart_core_tb();

#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump values into tracing file
#endif

  main_time++;

  dut->final();

#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump last values
  tfp->close();         // Close tracing file
  std::cout << "Generated vcd file" << std::endl;
  delete tfp;
#endif

  delete dut;
  exit(failed);
}
