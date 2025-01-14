// Verilator functions based on macros from 'iob-eth-defines.h'
// Similar functionality of 'iob_eth_defines_tasks.vs'

#ifndef H_IOB_ETH_DEFINES_VERILATOR_H
#define H_IOB_ETH_DEFINES_VERILATOR_H

#include "iob_eth_csrs_verilator.h"
#include "iob_eth_macros.h"

#define eth_tx_ready(idx, eth_if)                                              \
  !((IOB_ETH_GET_BD(idx << 1, eth_if) & TX_BD_READY) || 0)
#define eth_rx_ready(idx, eth_if) eth_tx_ready(idx, eth_if)

#define eth_bad_crc(idx, eth_if)                                               \
  ((IOB_ETH_GET_BD(idx << 1, eth_if) & RX_BD_CRC) || 0)

#define eth_send(enable, eth_if)                                               \
  ({                                                                           \
    IOB_ETH_SET_MODER(IOB_ETH_GET_MODER(eth_if) & ~MODER_TXEN |                \
                          (enable ? MODER_TXEN : 0),                           \
                      eth_if);                                                 \
  })

#define eth_receive(enable, eth_if)                                            \
  ({                                                                           \
    IOB_ETH_SET_MODER(IOB_ETH_GET_MODER(eth_if) & ~MODER_RXEN |                \
                          (enable ? MODER_RXEN : 0),                           \
                      eth_if);                                                 \
  })

#define eth_set_ready(idx, enable, eth_if)                                     \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1, eth_if) & ~TX_BD_READY |           \
                       (enable ? TX_BD_READY : 0),                             \
                   idx << 1, eth_if);                                          \
  })
#define eth_set_empty(idx, enable, eth_if) eth_set_ready(idx, enable, eth_if)

#define eth_set_interrupt(idx, enable, eth_if)                                 \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1, eth_if) & ~TX_BD_IRQ |             \
                       (enable ? TX_BD_IRQ : 0),                               \
                   idx << 1, eth_if);                                          \
  })

#define eth_set_wr(idx, enable, eth_if)                                        \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1, eth_if) & ~TX_BD_WRAP |            \
                       (enable ? TX_BD_WRAP : 0),                              \
                   idx << 1, eth_if);                                          \
  })

#define eth_set_crc(idx, enable, eth_if)                                       \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1, eth_if) & ~TX_BD_CRC |             \
                       (enable ? TX_BD_CRC : 0),                               \
                   idx << 1, eth_if);                                          \
  })

#define eth_set_pad(idx, enable, eth_if)                                       \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1, eth_if) & ~TX_BD_PAD |             \
                       (enable ? TX_BD_PAD : 0),                               \
                   idx << 1, eth_if);                                          \
  })

#define eth_set_ptr(idx, ptr, eth_if)                                          \
  ({ IOB_ETH_SET_BD((uint32_t)ptr, (idx << 1) + 1, eth_if); })

// Reset buffer descriptor memory
void eth_reset_bd_memory(iob_native_t *eth_if) {
  // Reset 128 buffer descriptors (64 bits each)
  for (int i = 0; i < 256; i++) {
    IOB_ETH_SET_BD(0x00000000, i, eth_if);
  }
}

void eth_set_payload_size(unsigned int idx, unsigned int size,
                          iob_native_t *eth_if) {
  IOB_ETH_SET_BD((IOB_ETH_GET_BD(idx << 1, eth_if) & 0x0000ffff) | size << 16,
                 idx << 1, eth_if);
}

void eth_wait_phy_rst(iob_native_t *eth_if) {
  while (IOB_ETH_GET_PHY_RST_VAL(eth_if))
    ;
}

#endif // H_IOB_ETH_DEFINES_VERILATOR_H
