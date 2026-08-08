/*
 * SPDX-FileCopyrightText: 2026 IObundle
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include "clint.h"
#include "iob_bsp.h"
#include "iob_printf.h"
// #include "iob_spi.h"
// #include "iob_spidefs.h"
// #include "iob_spiplatform.h"
#include "iob_system_linux_conf.h"
#include "iob_system_linux_mmap.h"
#include "iob_uart16550.h"
#ifdef IOB_SYSTEM_LINUX_USE_ETHERNET
#include "iob_eth.h"
#include "iob_eth_csrs.h"
#include "iob_eth_macros.h"
#endif
#include "plic.h"
#include <string.h>
#ifdef IOB_SYSTEM_LINUX_DMA_DEMO
#include "iob_axistream_in.h"
#include "iob_axistream_out.h"
#include "iob_dma.h"
#endif

#include "riscv-csr.h"
#include "riscv-interrupts.h"

// #define IOB_SYSTEM_LINUX_VERSAT_DEMO
#ifdef IOB_SYSTEM_LINUX_VERSAT_DEMO
#include "versat_crypto_tests.h"
#endif

#ifdef SIMULATION
#define WAIT_TIME 0.001
#else
#define WAIT_TIME 1
#endif

#define MTIMER_SECONDS_TO_CLOCKS(SEC) ((uint64_t)(((SEC) * (IOB_BSP_FREQ))))

#define NSAMPLES 16

// Machine mode interrupt service routine
static void irq_entry(void) __attribute__((interrupt("machine")));

// Global to hold current timestamp
static volatile uint64_t timestamp = 0;

void send_axistream();
void receive_axistream();

void clear_cache() {
  // Delay to ensure all data is written to memory
  for (unsigned int i = 0; i < 10; i++)
    asm volatile("nop");
  // Flush VexRiscv CPU internal cache
  asm volatile(".word 0x500F" ::: "memory");
}

#ifdef IOB_SYSTEM_LINUX_USE_ETHERNET
// Send signal by uart to receive file by ethernet
uint32_t uart_recvfile_ethernet(const char *file_name) {

  uart16550_puts(UART_PROGNAME);
  uart16550_puts(": requesting to receive file by ethernet\n");

  // send file receive by ethernet request
  uart16550_putc(0x13);

  // send file name (including end of string)
  uart16550_puts(file_name);
  uart16550_putc(0);

  // receive file size
  uint32_t file_size = uart16550_getc();
  file_size |= ((uint32_t)uart16550_getc()) << 8;
  file_size |= ((uint32_t)uart16550_getc()) << 16;
  file_size |= ((uint32_t)uart16550_getc()) << 24;

  // send ACK before receiving file
  uart16550_putc(ACK);

  return file_size;
}
#endif // IOB_SYSTEM_LINUX_USE_ETHERNET

// copy src to dst
// return number of copied chars (excluding '\0')
int string_copy(char *dst, char *src) {
  if (dst == NULL || src == NULL) {
    return -1;
  }
  int cnt = 0;
  while (src[cnt] != 0) {
    dst[cnt] = src[cnt];
    cnt++;
  }
  dst[cnt] = '\0';
  return cnt;
}

// 0: same string
// otherwise: different
int compare_str(char *str1, char *str2, int str_size) {
  int c = 0;
  while (c < str_size) {
    if (str1[c] != str2[c]) {
      return str1[c] - str2[c];
    }
    c++;
  }
  return 0;
}

// Needed by crypto side to time algorithms.
// Does not need to return seconds or any time unit, we are comparing directly
// with the software implementation. Only care about the relative differences
int GetTime() { return clint_getTime(CLINT0_BASE); }

#ifdef IOB_SYSTEM_LINUX_USE_ETHERNET
static uint16_t mii_read(int phy, int reg_addr) {
  iob_eth_csrs_set_miiaddress(MIIADDRESS_ADDR(phy, reg_addr));
  iob_eth_csrs_set_miicommand(MIICOMMAND_READ);
  int timeout = 100000;
  while (iob_eth_csrs_get_miicommand() && timeout > 0)
    timeout--;
  iob_eth_csrs_set_miicommand(0);
  if (timeout == 0)
    printf("    [!] mii_read(phy=%d, reg=%d) TIMEOUT\n", phy, reg_addr);
  return iob_eth_csrs_get_miirx_data() & 0xFFFF;
}

static void mii_write(int phy, int reg_addr, uint16_t val) {
  iob_eth_csrs_set_miiaddress(MIIADDRESS_ADDR(phy, reg_addr));
  iob_eth_csrs_set_miitx_data(MIITX_DATA_VAL(val));
  iob_eth_csrs_set_miicommand(MIICOMMAND_WRITE);
  int timeout = 100000;
  while (iob_eth_csrs_get_miicommand() && timeout > 0)
    timeout--;
  iob_eth_csrs_set_miicommand(0);
  if (timeout == 0)
    printf("    [!] mii_write(phy=%d, reg=%d) TIMEOUT\n", phy, reg_addr);
}

void debug_phy_connection() {
  printf("\n--- Starting Ethernet PHY Connection Debug Tests ---\n");

  // Initialize MII management clock division (MDC clock <= 2.5 MHz)
  // Assuming frequency is around 50MHz, divider 40 gives 1.25 MHz.
  iob_eth_csrs_set_miimoder(MIIMODER_CLKDIV(40));

  // 1. Scan MII bus to discover the PHY address
  int found_phy_addr = -1;
  printf("Scanning MII PHY addresses (0-31):\n");
  for (int phy = 0; phy < 32; phy++) {
    uint16_t id1 = mii_read(phy, 2);
    uint16_t id2 = mii_read(phy, 3);

    if (id1 != 0x0000 && id1 != 0xFFFF) {
      printf("  [+] Found PHY at address %d: ID1=0x%04X, ID2=0x%04X\n", phy,
             id1, id2);
      found_phy_addr = phy;
    }
  }

  if (found_phy_addr == -1) {
    printf("  [!] ERROR: No PHY found on MII management bus!\n");
    printf("--- Ethernet PHY Connection Debug Tests Complete ---\n\n");
    return;
  }

  // 2. Read and print standard PHY registers for the found PHY
  int phy = found_phy_addr;
  printf("\nReading registers for PHY at address %d:\n", phy);

  uint16_t bmcr = mii_read(phy, 0);      // Basic Mode Control Register
  uint16_t bmsr = mii_read(phy, 1);      // Basic Mode Status Register
  uint16_t advertise = mii_read(phy, 4); // Auto-Negotiation Advertisement
  uint16_t lpa = mii_read(phy, 5); // Auto-Negotiation Link Partner Ability

  printf("  Reg 0 (Control): 0x%04X\n", bmcr);
  printf("    - Reset: %d\n", (bmcr >> 15) & 1);
  printf("    - Loopback: %d\n", (bmcr >> 14) & 1);
  printf("    - Speed Selection: %s\n",
         ((bmcr >> 13) & 1) ? "100 Mbps" : "10 Mbps");
  printf("    - Auto-Negotiation Enable: %d\n", (bmcr >> 12) & 1);
  printf("    - Power Down: %d\n", (bmcr >> 11) & 1);
  printf("    - Duplex Mode: %s\n", (bmcr >> 8) & 1 ? "Full" : "Half");

  printf("  Reg 1 (Status): 0x%04X\n", bmsr);
  printf("    - Auto-Negotiation Complete: %d\n", (bmsr >> 5) & 1);
  printf("    - Link Status: %s\n", (bmsr >> 2) & 1 ? "UP" : "DOWN");

  printf("  Reg 4 (AN Advertisement): 0x%04X\n", advertise);
  printf("  Reg 5 (AN Link Partner Ability): 0x%04X\n", lpa);

  // 3. Check link status (before write test to avoid AN disruption)
  printf("\nChecking link status...\n");
  uint16_t status = mii_read(phy, 1);
  int link_up = (status & (1 << 2)) != 0;

  if (link_up) {
    printf("  [+] SUCCESS: Ethernet link is UP!\n");
    bmcr = mii_read(phy, 0);
    printf("  Speed: %s, Duplex: %s\n",
           ((bmcr >> 13) & 1) ? "100 Mbps" : "10 Mbps",
           (bmcr >> 8) & 1 ? "Full" : "Half");
  } else {
    printf("  [!] WARNING: Ethernet link is DOWN. Please check cable "
           "connection.\n");
  }

  // 4. Test writing to some register to verify write communication
  printf("\nTesting MII write to PHY...\n");
  uint16_t orig_bmcr = bmcr;
  uint16_t test_bmcr = orig_bmcr | (1 << 14); // loopback bit
  mii_write(phy, 0, test_bmcr);
  uint16_t read_bmcr = mii_read(phy, 0);
  if (read_bmcr & (1 << 14)) {
    printf("  [+] Write test successful: Loopback bit set in Reg 0.\n");
  } else {
    printf("  [!] ERROR: Write test failed! Read back 0x%04X, expected bit 14 "
           "set.\n",
           read_bmcr);
  }
  // Restore original control register
  mii_write(phy, 0, orig_bmcr);

  printf("--- Ethernet PHY Connection Debug Tests Complete ---\n\n");
}
#endif

int main() {
  char pass_string[] = "Test passed!";
  uint_xlen_t irq_entry_copy;
  int i;
  int test_result = 0;

  // init uart
  uart16550_init(UART0_BASE, IOB_BSP_FREQ / (16 * IOB_BSP_BAUD));
  clint_setCmp(CLINT0_BASE, 0xffffffffffffffff, 0);
  printf_init(&uart16550_putc);
#ifdef IOB_SYSTEM_LINUX_USE_ETHERNET
  // init eth
  eth_init(ETH0_BASE, &clear_cache);
  eth_wait_phy_rst();
  // Run PHY connection debug tests
  debug_phy_connection();
#endif // IOB_SYSTEM_LINUX_USE_ETHERNET

#ifdef IOB_SYSTEM_LINUX_DMA_DEMO
  // init dma
  dma_init(DMA0_BASE);
  // init axistream
  IOB_AXISTREAM_IN_INIT_BASEADDR(AXISTREAMIN0_BASE);
  IOB_AXISTREAM_OUT_INIT_BASEADDR(AXISTREAMOUT0_BASE);
  IOB_AXISTREAM_IN_SET_ENABLE(1);
  IOB_AXISTREAM_OUT_SET_ENABLE(1);
#endif

  char buffer[5096];
#ifdef IOB_SYSTEM_LINUX_USE_ETHERNET
  // Receive data from console via Ethernet
  uint32_t file_size = uart_recvfile_ethernet("../src/eth_example.txt");
  eth_rcv_file(buffer, file_size);
  uart16550_puts("\nFile received from console via ethernet:\n");
  for (i = 0; i < file_size; i++)
    uart16550_putc(buffer[i]);
#endif // IOB_SYSTEM_LINUX_USE_ETHERNET

#ifdef IOB_SYSTEM_LINUX_VERSAT_DEMO
  InitializeCryptoSide(VERSAT0_BASE);
#endif

  printf("\n\n\nHello world!\n\n\n");

#ifdef IOB_SYSTEM_LINUX_DMA_DEMO
  send_axistream();
  receive_axistream();
#endif

  // Global interrupt disable
  csr_clr_bits_mstatus(MSTATUS_MIE_BIT_MASK);

  // #ifdef SIMULATION
  // #ifndef VERILATOR
  //   unsigned int word = 0xA3A2A1A0;
  //   unsigned int address = 0x000100;
  //   unsigned int read_mem = 0xF0F0F0F0;
  //   printf("\nTest: %x, %x.\n", word, read_mem);
  //   // init spi flash controller
  //   spiflash_init(SPI0_BASE);
  //   printf("\nTesting SPI flash controller\n");
  //   // Reading Status Reg
  //   unsigned int reg = 0x00;
  //   spiflash_readStatusReg(&reg);
  //   printf("\nStatus reg (%x)\n", reg);
  //
  //   // Testing Fast Read in single, dual, quad
  //   unsigned bytes = 4, readid = 0;
  //   unsigned frame = 0x00000000;
  //   unsigned commFastRead = 0x0b;
  //   unsigned fastReadmem0 = 0, fastReadmem1 = 0, fastReadmem2 = 0;
  //   unsigned dummycycles = 8;
  //
  //   // Read ID
  //   bytes = 4;
  //   readid = 0;
  //   spiflash_executecommand(COMMANS, 0, 0, ((bytes * 8) << 8) | READ_ID,
  //   &readid);
  //
  //   printf("\nREAD_ID: (%x)\n", readid);
  //   // Read from flash memory
  //   printf("\nReading from flash (address: (%x))\n", address);
  //   read_mem = spiflash_readmem(address);
  //
  //   if (word == read_mem) {
  //     printf("\nMemory Read (%x) got same word as Programmed(%x)\nSuccess\n",
  //            read_mem, word);
  //   } else {
  //     printf("\nDifferent word from memory\nRead: (%x), Programmed: (%x)\n",
  //            read_mem, word);
  //     test_result = 1;
  //   }
  //
  //   address = 0x0;
  //   read_mem = 1;
  //   printf("\nTesting dual output fast read\n");
  //   read_mem = spiflash_readfastDualOutput(address, 0);
  //   printf("\nRead from memory address (%x) the word: (%x)\n", address,
  //   read_mem); word = read_mem;
  //
  //   read_mem = 2;
  //   printf("\nTesting quad output fast read\n");
  //   read_mem = spiflash_readfastQuadOutput(address, 0);
  //   if (read_mem == word) {
  //     printf(
  //         "\nQuadFastOutput Read (%x) got same word as Expected
  //         (%x)\nSuccess\n", address, read_mem);
  //   } else {
  //     printf("\nQuadFastOutput Read (%x) Different word from memory\nRead:
  //     (%x), "
  //            "Read: (%x),Expected: (%x)\n",
  //            address, read_mem, word);
  //     test_result = 1;
  //   }
  //
  //   read_mem = 3;
  //   printf("\nTesting dual input output fast read 0xbb\n");
  //   read_mem = spiflash_readfastDualInOutput(address, 0);
  //   if (read_mem == word) {
  //     printf("\nDualFastInOutput Read (%x) got same word as Expected "
  //            "(%x)\nSuccess\n",
  //            address, read_mem);
  //   } else {
  //     printf("\nDualFastInOutput Read (%x) Different word from memory\nRead:
  //     "
  //            "(%x), Read: (%x),Expected: (%x)\n",
  //            address, read_mem, word);
  //     test_result = 1;
  //   }
  //
  //   read_mem = 4;
  //   printf("\nTesting quad input output fast read 0xeb\n");
  //   read_mem = spiflash_readfastQuadInOutput(address, 0);
  //   if (read_mem == word) {
  //     printf("\nQuadFastInOutput Read (%x) got same word as Expected "
  //            "(%x)\nSuccess\n",
  //            address, read_mem);
  //   } else {
  //     printf("\nQuadFastInOutput Read (%x) Different word from memory\nRead:
  //     "
  //            "(%x), Read: (%x),Expected: (%x)\n",
  //            address, read_mem, word);
  //     test_result = 1;
  //   }
  //
  //   printf("\nRead Non volatile Register\n");
  //   unsigned nonVolatileReg = 0;
  //   bytes = 2;
  //   unsigned command_aux = 0xb5;
  //   spiflash_executecommand(COMMANS, 0, 0, ((bytes * 8) << 8) | command_aux,
  //                           &nonVolatileReg);
  //   printf("\nNon volatile Register (16 bits):(%x)\n", nonVolatileReg);
  //
  //   printf("\nRead enhanced volatile Register\n");
  //   unsigned enhancedReg = 0;
  //   bytes = 1;
  //   command_aux = 0x65;
  //   frame = 0x00000000;
  //   spiflash_executecommand(COMMANS, 0, 0,
  //                           (frame << 20) | ((bytes * 8) << 8) | command_aux,
  //                           &enhancedReg);
  //   printf("\nEnhanced volatile Register (8 bits):(%x)\n", enhancedReg);
  //
  //   // Testing xip bit enabling and xip termination sequence
  //   printf("\nTesting xip enabling through volatile bit and termination by "
  //          "sequence\n");
  //   unsigned volconfigReg = 0;
  //
  //   printf("\nResetting flash registers...\n");
  //   spiflash_resetmem();
  //
  //   spiflash_readVolConfigReg(&volconfigReg);
  //   printf("\nVolatile Configuration Register (8 bits):(%x)\n",
  //   volconfigReg);
  //
  //   spiflash_XipEnable();
  //
  //   volconfigReg = 0;
  //   spiflash_readVolConfigReg(&volconfigReg);
  //   printf(
  //       "\nAfter xip bit write, Volatile Configuration Register (8
  //       bits):(%x)\n", volconfigReg);
  //
  //   // Confirmation bit 0
  //   read_mem = 1;
  //   printf("\nTesting quad input output fast read with xip confirmation bit
  //   0\n"); read_mem = spiflash_readfastQuadInOutput(address, ACTIVEXIP);
  //   printf("\nRead from memory address (%x) the word: (%x)\n", address,
  //   read_mem); if (read_mem == word) {
  //     printf("\nQuadFastInOutput XIP Read (%x) got same word as Expected "
  //            "(%x)\nSuccess\n",
  //            address, read_mem);
  //   } else {
  //     printf("\nQuadFastInOutput XIP Read (%x) Different word from
  //     memory\nRead: "
  //            "(%x), Read: (%x),Expected: (%x)\n",
  //            address, read_mem, word);
  //     test_result = 1;
  //   }
  //
  //   int xipEnabled = 10;
  //   xipEnabled = spiflash_terminateXipSequence();
  //   printf("\nAfter xip termination sequence: %d\n", xipEnabled);
  //   volconfigReg = 0;
  //   spiflash_readVolConfigReg(&volconfigReg);
  //   printf("\nAfter xip termination sequence, Volatile Configuration Register
  //   (8 "
  //          "bits):(%x)\n",
  //          volconfigReg);
  //
  //   // XIP Bit 0 -> XIP ON
  //   if (((volconfigReg >> VOLCFG_XIP) & 0x1) == 0) {
  //     printf("\nAssuming Xip active, read from memory, confirmation bit
  //     1\n"); read_mem = 1; read_mem = spiflash_readMemXip(address,
  //     TERMINATEXIP); printf("\nRead from memory address (%x) the word:
  //     (%x)\n", address,
  //            read_mem);
  //   }
  //
  //   printf("Testing program flash\n");
  //   char prog_data[NSAMPLES] = {0};
  //   char *char_data = NULL;
  //   unsigned int read_data[NSAMPLES] = {0};
  //   int sample = 0;
  //   for (sample = 0; sample < NSAMPLES; sample++) {
  //     prog_data[sample] = sample;
  //   }
  //   spiflash_memProgram(prog_data, NSAMPLES, 0x104);
  //   for (sample = 0; sample < NSAMPLES; sample = sample + 4) {
  //     read_data[sample >> 2] = spiflash_readmem(0x104 + sample);
  //   }
  //   // check prog vs read data
  //   char_data = (char *)read_data;
  //   for (sample = 0; sample < NSAMPLES; sample++) {
  //     if (prog_data[sample] != char_data[sample]) {
  //       printf("Error: data[%x] = %08x != read_data[%x] = %08x\n", sample,
  //              prog_data[sample], sample, char_data[sample]);
  //       test_result = 1;
  //     }
  //   }
  //
  // #endif // #ifndef VERILATOR
  // #endif // #ifdef SIMULATION

#ifdef IOB_SYSTEM_LINUX_VERSAT_DEMO
  // Tests are too big and slow to perform during simulation.
  // Comment out the source files in sw_build.mk to also reduce binary size and
  // speedup simulation.
#ifndef SIMULATION
  test_result |= VersatSHATests();
  test_result |= VersatAESTests();
  test_result |= VersatMcElieceTests();
#else
  test_result |= VersatSimpleSHATests();
  test_result |= VersatSimpleAESTests();
#endif
#endif // IOB_SYSTEM_LINUX_VERSAT_DEMO

  if (test_result) {
    uart16550_sendfile("test.log", 12, "Test failed!");
  } else {
    uart16550_sendfile("test.log", 12, "Test passed!");
  }
  printf("Exit...\n");
  uart16550_finish();

  return 0;
}

#pragma GCC push_options
#pragma GCC optimize("align-functions=2")
static void irq_entry(void) {
  printf("Entered IRQ.\n");
  uint32_t this_cause = csr_read_mcause();
  timestamp = clint_getTime(CLINT0_BASE);
  if (this_cause & MCAUSE_INTERRUPT_BIT_MASK) {
    this_cause &= 0xFF;
    // Known exceptions
    switch (this_cause) {
    case RISCV_INT_POS_MTI:
      printf("Time interrupt.\n");
      // Timer exception, keep up the one second tick.
      clint_setCmp(CLINT0_BASE,
                   MTIMER_SECONDS_TO_CLOCKS(WAIT_TIME) + (uint32_t)timestamp,
                   0);
      break;
    }
  }
}
#pragma GCC pop_options

#ifdef IOB_SYSTEM_LINUX_DMA_DEMO
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
  uart16550_puts("Sending AXI stream bytes: ");
  for (i = 0; i < words_in_byte_stream * 4; i++)
    printf("0x%02x ", ((uint8_t *)byte_stream)[i]);
  uart16550_puts("\n");

  // Send bytes to AXI stream output via DMA
  uart16550_puts("Loading AXI words via DMA...\n\n");
  iob_axis_out_reset();
  IOB_AXISTREAM_OUT_SET_ENABLE(1);
  IOB_AXISTREAM_OUT_SET_MODE(1);
  IOB_AXISTREAM_OUT_SET_NWORDS(words_in_byte_stream);
  dma_start_transfer(byte_stream, words_in_byte_stream, 0, 0);

  free(byte_stream);
}

void receive_axistream() {
  uint8_t i;
  uint8_t n_received_words = IOB_AXISTREAM_IN_GET_NWORDS();

  // Allocate memory for byte stream
  volatile uint32_t *byte_stream =
      (volatile uint32_t *)malloc((n_received_words) * sizeof(uint32_t));

  // Transfer bytes from AXI stream input via DMA
  uart16550_puts("Storing AXI words via DMA...\n");
  IOB_AXISTREAM_IN_SET_MODE(1);
  dma_start_transfer((uint32_t *)byte_stream, n_received_words, 1, 0);

  clear_cache();

  // Print byte stream received
  uart16550_puts("Received AXI stream bytes: ");
  for (i = 0; i < n_received_words * 4; i++)
    printf("0x%02x ", ((volatile uint8_t *)byte_stream)[i]);
  uart16550_puts("\n\n");

  free((uint32_t *)byte_stream);
}
#endif // IOB_SYSTEM_LINUX_DMA_DEMO
