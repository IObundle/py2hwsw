/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "Viob_uart.h"
#include "iob_bsp.h"
#include "iob_tasks_tb.h"
#include "iob_uart_csrs.h"
#include <fstream>
#include <iostream>
#include <verilated.h>

#if (VM_TRACE == 1) // If verilator was invoked with --trace
#include <verilated_vcd_c.h>
#endif

#define MAX_SIM_TIME 120

vluint64_t main_time = 0;
Viob_uart *dut;
VerilatedVcdC *tfp;

double sc_time_stamp() { // Called by $time in Verilog
  return main_time;
}

void tick() {
  if (main_time >= MAX_SIM_TIME) {
    throw std::runtime_error(
        "Simulation time exceeded maximum simulation time");
  }
  dut->clk_i = !dut->clk_i;
  dut->eval();
  dut->clk_i = !dut->clk_i;
  dut->eval();
#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump values into tracing file
#endif
  main_time++;
}

iob_arst_pulse() {
  dut->clk_i = 0;
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
void iob_write(uint32_t addr, uint32_t data) {
  dut->iob_uart_csrs_addr_i = addr;
  dut->iob_uart_csrs_wdata_i = data;
  dut->iob_uart_csrs_we_i = 1;
  while (!dut->iob_csrs_iob_ready_o) {
    tick();
  }
  tick();
  dut->iob_uart_csrs_we_i = 0;
}

// read from the UART
uint32_t iob_read(uint32_t addr) {
  dut->iob_uart_csrs_addr_i = addr;
  dut->iob_uart_csrs_we_i = 0;
  tick();
  while (!dut->iob_csrs_iob_ready_o) {
    tick();
  }
  tick();
  return dut->iob_uart_csrs_rdata_o;
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

  // issue a hard async reset to the DUT
  iob_arst_pulse();

  // hold soft reset low
  IOB_UART_SET_SOFTRESET(0);

  // disable TX and RX
  IOB_UART_SET_TXEN(0);
  IOB_UART_SET_RXEN(0);

  // set the divisor
  IOB_UART_SET_DIV(FREQ / BAUD);

  // assert tx and rx not ready
  uint8_t tx_ready = IOB_UART_GET_TXREADY();
  if (tx_ready != 0) {
    std::cout << "Error: TX ready initially" << std::endl;
    return 1;
  }
  uint8_t rx_ready = IOB_UART_GET_RXREADY();
  if (rx_ready != 0) {
    std::cout << "Error: RX ready initially" << std::endl;
    return 1;
  }

  // pulse soft reset
  IOB_UART_SET_SOFTRESET(1);
  IOB_UART_SET_SOFTRESET(0);

  // enable RX and TX
  IOB_UART_SET_RXEN(1);
  IOB_UART_SET_TXEN(1);

  int failed = 0;

  // open test log file
  std::ofstream log_file;
  log_file.open("test.log");

  // data send/receive loop
  for (int i = 0; i < 256; i++) {
    // wait for tx ready
    while (!IOB_UART_GET_TXREADY())
      ;

    // write word to send
    IOB_UART_SET_TXDATA(i);

    // wait for rx ready
    while (!IOB_UART_GET_RXREADY())
      ;

    // read received word
    uint8_t rx_data = IOB_UART_GET_RXDATA();

    // check if received word is the same as sent word
    if (rx_data != i) {
      // signal error printing expected and received word
      std::cout << "Error: Expected " << i << " but received " << rx_data
                << std::endl;
      failed += 1;
    }

    if (failed != 0) {
      log_file << "Test failed!" << std::endl;
      log_file.close();
      exit(EXIT_FAILURE);
    }
  }

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

  std::ofstream log_file;
  log_file.open("test.log");
  log_file << "Test passed!" << std::endl;
  log_file.close();
  exit(EXIT_SUCCESS);
}
