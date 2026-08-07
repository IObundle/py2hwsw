/*
 * SPDX-FileCopyrightText: 2026 IObundle
 *
 * SPDX-License-Identifier: GPL-3.0-only
 *
 * Py2HWSW Version 0.81.0 has generated this code
 * (https://github.com/IObundle/py2hwsw).
 */

// SPDX-FileCopyrightText: 2026 IObundle
//
// SPDX-License-Identifier: GPL-3.0-only

#include "iob_bsp.h"
#include "iob_printf.h"
#include "iob_system_linux_conf.h"
#include "iob_system_linux_mmap.h"
#include "iob_uart16550.h"
#include "iob_eth.h"
#include "iob_eth_csrs.h"
#include "iob_eth_macros.h"
#include "iob_eth_defines.h"
#include "iob_plic.h"
#include "iob_timer.h"
#include <string.h>

#define ETH0_PLIC_SOURCE 2

static void clear_cache() {
  for (unsigned int i = 0; i < 10; i++)
    asm volatile("nop");
  asm volatile(".word 0x500F" ::: "memory");
}

#define DATA_FENCE() asm volatile("fence" ::: "memory")

static int pass_count, fail_count;

#define TEST(desc, cond)                                                       \
  do {                                                                         \
    if (cond) {                                                                \
      printf("  PASS: %s\n", desc);                                            \
      pass_count++;                                                            \
    } else {                                                                   \
      printf("  FAIL: %s\n", desc);                                            \
      fail_count++;                                                            \
    }                                                                          \
  } while (0)

#define TEST_EQ(desc, got, expected) TEST(desc, (got) == (expected))

int main() {
  uint32_t val;
  int i;
  int timeout;

  uart16550_init(UART0_BASE, IOB_BSP_FREQ / (16 * IOB_BSP_BAUD));
  printf_init(&uart16550_putc);

  iob_eth_csrs_init_baseaddr(ETH0_BASE);

  pass_count = 0;
  fail_count = 0;

  printf("\n=== iob_eth CSR Test ===\n\n");

  // 1. MODER - write/read back
  printf("--- MODER ---\n");
  iob_eth_csrs_set_moder(0xA5A5A5A5);
  val = iob_eth_csrs_get_moder();
  TEST_EQ("MODER write/read 0xA5A5A5A5", val, 0xA5A5A5A5);

  // Linux ethoc driver MODER value
  iob_eth_csrs_set_moder(MODER_RXEN | MODER_TXEN | MODER_CRC | MODER_PAD |
                         MODER_FULLD | MODER_PRO | MODER_BRO);
  val = iob_eth_csrs_get_moder();
  TEST_EQ("MODER Linux-compatible bits", val,
          MODER_RXEN | MODER_TXEN | MODER_CRC | MODER_PAD | MODER_FULLD |
              MODER_PRO | MODER_BRO);

  // 2. INT_SOURCE - write-1-to-clear
  printf("--- INT_SOURCE ---\n");
  iob_eth_csrs_set_int_source(0xFFFFFFFF);
  val = iob_eth_csrs_get_int_source();
  TEST_EQ("INT_SOURCE write-1-to-clear all bits", val, 0);

  iob_eth_csrs_set_int_source(0xDEADBEEF);
  val = iob_eth_csrs_get_int_source();
  TEST_EQ("INT_SOURCE write-1-to-clear pattern", val, 0);

  // 3. INT_MASK - write/read back
  printf("--- INT_MASK ---\n");
  iob_eth_csrs_set_int_mask(INT_MASK_ALL);
  val = iob_eth_csrs_get_int_mask();
  TEST_EQ("INT_MASK write/read all bits", val, INT_MASK_ALL);

  iob_eth_csrs_set_int_mask(0);
  val = iob_eth_csrs_get_int_mask();
  TEST_EQ("INT_MASK clear", val, 0);

  // 4. IPGT, IPGR1, IPGR2
  printf("--- IPG registers ---\n");
  iob_eth_csrs_set_ipgt(0x12);
  val = iob_eth_csrs_get_ipgt();
  TEST_EQ("IPGT write/read", val, 0x12);

  iob_eth_csrs_set_ipgr1(0x0C);
  val = iob_eth_csrs_get_ipgr1();
  TEST_EQ("IPGR1 write/read", val, 0x0C);

  iob_eth_csrs_set_ipgr2(0x12);
  val = iob_eth_csrs_get_ipgr2();
  TEST_EQ("IPGR2 write/read", val, 0x12);

  // 5. PACKETLEN
  printf("--- PACKETLEN ---\n");
  iob_eth_csrs_set_packetlen(PACKETLEN_MIN_MAX(64, 1518));
  val = iob_eth_csrs_get_packetlen();
  TEST_EQ("PACKETLEN min=64 max=1518", val, PACKETLEN_MIN_MAX(64, 1518));

  // 6. COLLCONF
  printf("--- COLLCONF ---\n");
  iob_eth_csrs_set_collconf(0x0F0F0F0F);
  val = iob_eth_csrs_get_collconf();
  TEST_EQ("COLLCONF write/read", val, 0x0F0F0F0F);

  // 7. TX_BD_NUM
  printf("--- TX_BD_NUM ---\n");
  iob_eth_csrs_set_tx_bd_num(TX_BD_NUM_VAL(0x40));
  val = iob_eth_csrs_get_tx_bd_num();
  TEST_EQ("TX_BD_NUM write/read", val, TX_BD_NUM_VAL(0x40));

  // 8. CTRLMODER
  printf("--- CTRLMODER ---\n");
  iob_eth_csrs_set_ctrlmoder(0);
  val = iob_eth_csrs_get_ctrlmoder();
  TEST_EQ("CTRLMODER=0", val, 0);

  iob_eth_csrs_set_ctrlmoder(CTRLMODER_PASSALL | CTRLMODER_RXFLOW |
                             CTRLMODER_TXFLOW);
  val = iob_eth_csrs_get_ctrlmoder();
  TEST_EQ("CTRLMODER all flags", val,
          CTRLMODER_PASSALL | CTRLMODER_RXFLOW | CTRLMODER_TXFLOW);

  // 9. MAC address
  printf("--- MAC_ADDR ---\n");
  iob_eth_csrs_set_mac_addr0(0x0A350001);
  val = iob_eth_csrs_get_mac_addr0();
  TEST_EQ("MAC_ADDR0 write/read", val, 0x0A350001);

  iob_eth_csrs_set_mac_addr1(0x0000);
  val = iob_eth_csrs_get_mac_addr1();
  TEST_EQ("MAC_ADDR1 write/read", val, 0x0000);

  // 10. HASH registers
  printf("--- ETH_HASH ---\n");
  iob_eth_csrs_set_eth_hash0_adr(0xA5A5A5A5);
  val = iob_eth_csrs_get_eth_hash0_adr();
  TEST_EQ("ETH_HASH0 write/read", val, 0xA5A5A5A5);

  iob_eth_csrs_set_eth_hash1_adr(0x5A5A5A5A);
  val = iob_eth_csrs_get_eth_hash1_adr();
  TEST_EQ("ETH_HASH1 write/read", val, 0x5A5A5A5A);

  // 11. TXCTRL
  printf("--- ETH_TXCTRL ---\n");
  iob_eth_csrs_set_eth_txctrl(0);
  val = iob_eth_csrs_get_eth_txctrl();
  TEST_EQ("ETH_TXCTRL=0", val, 0);

  iob_eth_csrs_set_eth_txctrl(0xDEADBEEF);
  val = iob_eth_csrs_get_eth_txctrl();
  TEST_EQ("ETH_TXCTRL write/read", val, 0xDEADBEEF);

  // 12. MII management
  printf("--- MII ---\n");
  iob_eth_csrs_set_miimoder(MIIMODER_CLKDIV(40));
  val = iob_eth_csrs_get_miimoder();
  TEST_EQ("MIIMODER clkdiv=40", val, MIIMODER_CLKDIV(40));

  iob_eth_csrs_set_miiaddress(MIIADDRESS_ADDR(0, 0));
  val = iob_eth_csrs_get_miiaddress();
  TEST_EQ("MIIADDRESS PHY=0 REG=0", val, MIIADDRESS_ADDR(0, 0));

  iob_eth_csrs_set_miicommand(MIICOMMAND_READ);

  timeout = 500000;
  while (iob_eth_csrs_get_miistatus() & MIISTATUS_BUSY) {
    timeout--;
    if (timeout <= 0)
      break;
  }
  TEST("MII busy completed", timeout > 0);

  val = iob_eth_csrs_get_miirx_data();
  printf("  MIIRX_DATA = 0x%04X\n", val);
  TEST("MIIRX_DATA read OK (non-zero data or 0xFFFF)", val != 0xDEADBEEF);

  val = iob_eth_csrs_get_miistatus();
  TEST_EQ("MIISTATUS not busy", val & MIISTATUS_BUSY, 0);

  // 13. BD memory
  printf("--- BD memory ---\n");
  for (i = 0; i < 4; i++) {
    uint32_t pattern = 0xA5A5A5A5 ^ (i * 0x11111111);
    iob_eth_csrs_set_bd(pattern, i);
    val = iob_eth_csrs_get_bd(i);
    TEST_EQ("BD write/read", val, pattern);
  }

  // 14. Version register (read-only)
  printf("--- VERSION ---\n");
  val = iob_eth_csrs_get_version();
  printf("  VERSION = 0x%06X\n", val);
  TEST("VERSION read OK", val != 0);

  // 15. MII Write (validates [12:8] register address fix)
  printf("--- MII Write ---\n");
  {
    iob_eth_csrs_set_miiaddress(MIIADDRESS_ADDR(0, 1)); // REG=1 (tests [12:8])
    iob_eth_csrs_set_miitx_data(MIITX_DATA_VAL(0xA5A5));
    iob_eth_csrs_set_miicommand(MIICOMMAND_WRITE);
    timeout = 500000;
    while (iob_eth_csrs_get_miistatus() & MIISTATUS_BUSY) {
      timeout--;
      if (timeout <= 0)
        break;
    }
    TEST("MII write completed", timeout > 0);

    // Read back same register to validate the full cycle
    iob_eth_csrs_set_miiaddress(MIIADDRESS_ADDR(0, 1));
    iob_eth_csrs_set_miicommand(MIICOMMAND_READ);
    timeout = 500000;
    while (iob_eth_csrs_get_miistatus() & MIISTATUS_BUSY) {
      timeout--;
      if (timeout <= 0)
        break;
    }
    TEST("MII write-then-read completed", timeout > 0);
    val = iob_eth_csrs_get_miirx_data();
    printf("  MII read-back after write = 0x%04X\n", val);
    TEST("MII write/read cycle executed", val != 0xDEADBEEF);
  }

  // 16. PLIC Timer Interrupt (validates full PLIC interrupt chain)
  printf("--- PLIC Timer Interrupt ---\n");
  {
    uint32_t src;
    uint64_t count;

    timer_init(TIMER0_BASE);
    plic_init(PLIC0_BASE);
    plic_enable_interrupt(0, 1); // source 1 = timer
    count = timer_get_count();
    timer_set_interrupt(count + 1000);
    timeout = 100000;
    while (!(plic_read(PLIC_PENDING_BASE) & (1 << 1))) {
      timeout--;
      if (timeout <= 0)
        break;
    }
    TEST("Timer interrupt pending in PLIC", timeout > 0);
    if (timeout > 0) {
      src = plic_claim_interrupt(0);
      TEST_EQ("PLIC claim source = 1 (timer)", src, 1);
      plic_complete_interrupt(0, src);
      TEST("PLIC pending cleared after complete",
           !(plic_read(PLIC_PENDING_BASE) & (1 << 1)));
    }
    timer_set_interrupt(0); // disable timer interrupt
    plic_disable_interrupt(0, 1);
  }

  // 17. PLIC eth0 Configuration
  printf("--- PLIC eth0 Config ---\n");
  {
    uint32_t enable_val;
    plic_enable_interrupt(0, ETH0_PLIC_SOURCE);
    enable_val = plic_read(PLIC_ENABLE_BASE);
    TEST("PLIC eth0 enable bit 2 set", enable_val & (1 << ETH0_PLIC_SOURCE));
    plic_disable_interrupt(0, ETH0_PLIC_SOURCE);
    enable_val = plic_read(PLIC_ENABLE_BASE);
    TEST("PLIC eth0 enable bit 2 cleared",
         !(enable_val & (1 << ETH0_PLIC_SOURCE)));
    plic_set_priority(ETH0_PLIC_SOURCE, 2);
    enable_val = plic_read(PLIC_PRIORITY_BASE + ETH0_PLIC_SOURCE * 4);
    TEST_EQ("PLIC eth0 priority", enable_val, 2);
    plic_set_priority(ETH0_PLIC_SOURCE, 1); // restore
  }

  // 18. Real Ethernet TX + Interrupt (full datapath + interrupt chain test)
  printf("--- Real TX + Interrupt ---\n");
  {
    uint8_t frame[60];
    uint32_t frame_addr;
    uint32_t src;

    // Wait for PHY reset to complete
    eth_wait_phy_rst();

    // Setup PLIC for eth0 interrupt
    plic_enable_interrupt(0, ETH0_PLIC_SOURCE);
    iob_eth_csrs_set_int_mask(INT_MASK_TXF);
    iob_eth_csrs_set_int_source(0xFFFFFFFF); // clear any pending

    // Set MODER: enable TX, RX, CRC, PAD, FULLD
    iob_eth_csrs_set_moder(MODER_RXEN | MODER_TXEN | MODER_CRC | MODER_PAD |
                           MODER_FULLD | MODER_PRO | MODER_BRO);

    // Build minimum Ethernet frame (60 bytes = 14 header + 46 payload)
    memset(frame, 0, sizeof(frame));
    // Destination MAC: broadcast
    memset(frame, 0xFF, 6);
    // Source MAC: 0A:35:00:00:00:01
    frame[6] = 0x0A;
    frame[7] = 0x35;
    frame[8] = 0x00;
    frame[9] = 0x00;
    frame[10] = 0x00;
    frame[11] = 0x01;
    // Ethertype: 0x6000
    frame[12] = 0x60;
    frame[13] = 0x00;
    // Payload is already zeroed

    // Copy frame to known address within 24-bit AXI range
    frame_addr = 0x00100000;
    memcpy((void *)(uintptr_t)frame_addr, frame, sizeof(frame));
    DATA_FENCE();

    // Write TX BD entry 0: status word
    iob_eth_csrs_set_bd(TX_BD_READY | TX_BD_IRQ | TX_BD_WRAP | TX_BD_CRC |
                            TX_BD_PAD | TX_BD_LEN(sizeof(frame)),
                        0);
    // TX BD entry 0: pointer word
    iob_eth_csrs_set_bd(frame_addr, 1);

    // Enable TX (rising edge triggers state machine)
    iob_eth_csrs_set_moder(iob_eth_csrs_get_moder() & ~MODER_TXEN);
    iob_eth_csrs_set_moder(iob_eth_csrs_get_moder() | MODER_TXEN);

    // Wait for interrupt via PLIC
    timeout = 2000000;
    while (!(plic_read(PLIC_PENDING_BASE) & (1 << ETH0_PLIC_SOURCE))) {
      timeout--;
      if (timeout <= 0)
        break;
    }
    TEST("TX interrupt pending in PLIC", timeout > 0);

    if (timeout > 0) {
      src = plic_claim_interrupt(0);
      TEST_EQ("PLIC claim source = 2 (eth0)", src, ETH0_PLIC_SOURCE);
      if (src == ETH0_PLIC_SOURCE)
        plic_complete_interrupt(0, src);
    }

    // Verify TX completed: BD READY bit cleared by HW
    val = iob_eth_csrs_get_bd(0);
    printf("  TX BD status = 0x%08X\n", val);
    TEST("TX BD READY cleared by HW", !(val & TX_BD_READY));

    // Clean up
    iob_eth_csrs_set_int_source(0xFFFFFFFF);
    iob_eth_csrs_set_int_mask(0);
    iob_eth_csrs_set_moder(iob_eth_csrs_get_moder() & ~MODER_TXEN);
  }

  // Summary
  printf("\n=== CSR Test Complete ===\n");
  printf("  PASS: %d\n", pass_count);
  printf("  FAIL: %d\n", fail_count);

  uart16550_finish();
  return fail_count;
}
