#include "Viob_eth_mem_wrapper.h"
#include <fstream>
#include <iostream>
#include <verilated.h>

#include "bsp.h"
#include "iob_eth_defines_verilator.h"
#include "iob_tasks.h"

#if (VM_TRACE == 1) // If verilator was invoked with --trace
#include <verilated_vcd_c.h>
#endif

extern vluint64_t main_time;
extern timer_settings_t task_timer_settings;

typedef struct {
  short unsigned int *tb_addr;
  unsigned char *tb_awvalid;
  unsigned char *tb_awready;
  unsigned char *tb_arvalid;
  unsigned char *tb_arready;
  unsigned int *tb_wdata;
  unsigned char *tb_wvalid;
  unsigned char *tb_wready;
  unsigned int *tb_rdata;
  unsigned char *tb_rvalid;
  unsigned char *tb_rready;
} tb_mem_if_t;

void cpu_initeth(iob_native_t *eth_if);
void reset_tb_memory(tb_mem_if_t *mem_if);
void tb_mem_write(unsigned int addr, unsigned int data, tb_mem_if_t *mem_if);
unsigned int tb_mem_read(unsigned int addr, tb_mem_if_t *mem_if);

Viob_eth_mem_wrapper *dut = new Viob_eth_mem_wrapper; // Create DUT object

void call_eval() { dut->eval(); }

#if (VM_TRACE == 1)
VerilatedVcdC *tfp = new VerilatedVcdC; // Create tracing object

void call_dump(vluint64_t time) { tfp->dump(time); }
#endif

double sc_time_stamp() { // Called by $time in Verilog
  return main_time;
}

//
// Main program
//
int main(int argc, char **argv) {
  unsigned int i, frame_word;

  Verilated::commandArgs(argc, argv); // Init verilator context
  task_timer_settings.clk = &dut->clk_i;
  task_timer_settings.eval = call_eval;
#if (VM_TRACE == 1)
  task_timer_settings.dump = call_dump;
#endif

  iob_native_t eth_if = {
      &dut->iob_valid_i,  &dut->iob_addr_i,  USINT,
      &dut->iob_wdata_i,  &dut->iob_wstrb_i, &dut->iob_rdata_o,
      &dut->iob_rvalid_o, &dut->iob_ready_o};

  tb_mem_if_t mem_if = {&dut->tb_addr,    &dut->tb_awvalid, &dut->tb_awready,
                        &dut->tb_arvalid, &dut->tb_arready, &dut->tb_wdata,
                        &dut->tb_wvalid,  &dut->tb_wready,  &dut->tb_rdata,
                        &dut->tb_rvalid,  &dut->tb_rready};

  unsigned char frame_data[] = {
      // Frame header
      0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
      0x00, 0x06,
      // Frame payload
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
      22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
      40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
      58, 59, 60, 61, 62, 63, 64, 65, 66};

  // Frame size (header + payload)
  unsigned int frame_size = sizeof(frame_data);

#if (VM_TRACE == 1)
  Verilated::traceEverOn(true); // Enable tracing
  dut->trace(tfp, 99);          // Trace 99 levels of hierarchy
  tfp->open("uut.vcd");         // Open tracing file
#endif

  // init cpu bus signals
  *(eth_if.iob_valid) = 0;
  *(eth_if.iob_wstrb) = 0;

  dut->cke_i = 1;

  // Reset signal
  dut->arst_i = 0;
  for (i = 0; i < 100; i++)
    Timer(CLK_PERIOD);
  dut->arst_i = 1;
  for (i = 0; i < 1000; i++)
    Timer(CLK_PERIOD);
  dut->arst_i = 0;
  for (i = 0; i < 100; i++)
    Timer(CLK_PERIOD);

  reset_tb_memory(&mem_if);

  // configure eth core
  cpu_initeth(&eth_if);

  VL_PRINTF("Writing test frame to memory...\n");
  VL_PRINTF("\nTest frame data: ");
  for (i = 0; i < frame_size; i = i + 4) {
    if (i % 16 == 0)
      VL_PRINTF("\n");
    tb_mem_write(i,
                 frame_data[i + 3] << 24 | frame_data[i + 2] << 16 |
                     frame_data[i + 1] << 8 | frame_data[i],
                 &mem_if);
    VL_PRINTF("%02x %02x %02x %02x ", frame_data[i], frame_data[i + 1],
              frame_data[i + 2], frame_data[i + 3]);
  }

  VL_PRINTF("\n\nWaiting for PHY reset...\n");
  eth_wait_phy_rst(&eth_if);

  VL_PRINTF("Starting ethernet frame transmission via DMA...\n");

  // set frame size
  eth_set_payload_size(0, frame_size, &eth_if);
  // Set ready bit
  eth_set_ready(0, 1, &eth_if);

  VL_PRINTF("Verifying received frame via DMA...\n");

  // wait until data received
  while (!eth_rx_ready(64, &eth_if))
    ;

  // Check bad CRC
  if (eth_bad_crc(64, &eth_if))
    VL_PRINTF("Bad CRC!\n");

  VL_PRINTF("\nReceived frame data: ");
  for (i = 0; i < frame_size; i = i + 4) {
    if (i % 16 == 0)
      VL_PRINTF("\n");
    frame_word = tb_mem_read(i, &mem_if);
    VL_PRINTF("%02x %02x %02x %02x ", frame_data[i], frame_data[i + 1],
              frame_data[i + 2], frame_data[i + 3]);
    if (frame_word != (frame_data[i + 3] << 24 | frame_data[i + 2] << 16 |
                       frame_data[i + 1] << 8 | frame_data[i])) {
      VL_PRINTF("\nERROR: Received frame data mismatch!\n");
      dut->final();
      delete dut;
      exit(EXIT_FAILURE);
    }
  }
  VL_PRINTF("\n");

  dut->final();

#if (VM_TRACE == 1)
  tfp->dump(main_time); // Dump last values
  tfp->close();         // Close tracing file
  std::cout << "Generated vcd file" << std::endl;
  delete tfp;
#endif

  delete dut;

  std::cout << "\x1b[1;34m" << std::endl;
  std::cout << "Test completed successfully." << std::endl;
  std::cout << "\x1b[0m" << std::endl;

  std::ofstream log_file;
  log_file.open("test.log");
  log_file << "Test passed!" << std::endl;
  log_file.close();
  exit(EXIT_SUCCESS);
}

void cpu_initeth(iob_native_t *eth_if) {
  VL_PRINTF("Initializing ethernet core...\n");
  eth_reset_bd_memory(eth_if);

  /**** Configure receiver *****/
  // set frame pointer (starting at half memory)
  eth_set_ptr(64, 1 << 9, eth_if);

  // Mark empty; Set as last descriptor; Enable interrupt.
  eth_set_empty(64, 1, eth_if);
  eth_set_wr(64, 1, eth_if);
  eth_set_interrupt(64, 1, eth_if);

  // Enable reception
  eth_receive(1, eth_if);

  /**** Configure transmitter *****/
  // set frame pointer (starting at beginning of memory)
  eth_set_ptr(0, 0, eth_if);

  // Enable CRC and PAD; Set as last descriptor; Enable interrupt.
  eth_set_crc(0, 1, eth_if);
  eth_set_pad(0, 1, eth_if);
  eth_set_wr(0, 1, eth_if);
  eth_set_interrupt(0, 1, eth_if);

  // enable transmission
  eth_send(1, eth_if);
}

//
// Testbench memory control
//

void reset_tb_memory(tb_mem_if_t *mem_if) {
  int i;
  VL_PRINTF("Resetting AXI memory...\n");
  // Only reset first 2^10 addresses. The rest is not used.
  for (i = 0; i < 1 << 10; i = i + 1) {
    tb_mem_write(i, 0, mem_if);
  }
}

void tb_mem_write(unsigned int addr, unsigned int data, tb_mem_if_t *mem_if) {
  Timer(1);
  *(mem_if->tb_awvalid) = 1; // sync and assign
  *(mem_if->tb_addr) = addr;
  while (!*(mem_if->tb_awready))
    Timer(CLK_PERIOD);
  Timer(CLK_PERIOD); // Sync with next clk posedge + 1ns
  *(mem_if->tb_awvalid) = 0;
  *(mem_if->tb_addr) = 0;

  *(mem_if->tb_wvalid) = 1;
  *(mem_if->tb_wdata) = data;
  while (!*(mem_if->tb_wready))
    Timer(CLK_PERIOD);
  Timer(CLK_PERIOD); // Sync with next clk posedge + 1ns
  *(mem_if->tb_wvalid) = 0;
  *(mem_if->tb_wdata) = 0;
  Timer(CLK_PERIOD - 1); // Sync with next clk posedge
}

unsigned int tb_mem_read(unsigned int addr, tb_mem_if_t *mem_if) {
  unsigned int data;

  Timer(1);
  *(mem_if->tb_arvalid) = 1; // sync and assign
  *(mem_if->tb_addr) = addr;
  while (!*(mem_if->tb_arready))
    Timer(CLK_PERIOD);
  *(mem_if->tb_arvalid) = 0;
  *(mem_if->tb_addr) = 0;

  while (!*(mem_if->tb_rvalid))
    Timer(CLK_PERIOD);
  data = *(mem_if->tb_rdata);
  *(mem_if->tb_rready) = 1;
  Timer(CLK_PERIOD - 1); // Sync with next clk posedge
  return data;
}
