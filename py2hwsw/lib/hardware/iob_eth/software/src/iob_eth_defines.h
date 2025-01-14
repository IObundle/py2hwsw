#ifndef H_IOB_ETH_DEFINES_H
#define H_IOB_ETH_DEFINES_H

#include "eth_frame_struct.h"

#include "iob_eth_conf.h"
#include "iob_eth_csrs.h"
#include "iob_eth_macros.h"

#define eth_tx_ready(idx) !((IOB_ETH_GET_BD(idx << 1) & TX_BD_READY) || 0)
#define eth_rx_ready(idx) eth_tx_ready(idx)

#define eth_bad_crc(idx) ((IOB_ETH_GET_BD(idx << 1) & RX_BD_CRC) || 0)

#define eth_send(enable)                                                       \
  ({                                                                           \
    IOB_ETH_SET_MODER(IOB_ETH_GET_MODER() & ~MODER_TXEN |                      \
                      (enable ? MODER_TXEN : 0));                              \
  })

#define eth_receive(enable)                                                    \
  ({                                                                           \
    IOB_ETH_SET_MODER(IOB_ETH_GET_MODER() & ~MODER_RXEN |                      \
                      (enable ? MODER_RXEN : 0));                              \
  })

#define eth_set_ready(idx, enable)                                             \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1) & ~TX_BD_READY |                   \
                       (enable ? TX_BD_READY : 0),                             \
                   idx << 1);                                                  \
  })
#define eth_set_empty(idx, enable) eth_set_ready(idx, enable)

#define eth_set_interrupt(idx, enable)                                         \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1) & ~TX_BD_IRQ |                     \
                       (enable ? TX_BD_IRQ : 0),                               \
                   idx << 1);                                                  \
  })

#define eth_set_wr(idx, enable)                                                \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1) & ~TX_BD_WRAP |                    \
                       (enable ? TX_BD_WRAP : 0),                              \
                   idx << 1);                                                  \
  })

#define eth_set_crc(idx, enable)                                               \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1) & ~TX_BD_CRC |                     \
                       (enable ? TX_BD_CRC : 0),                               \
                   idx << 1);                                                  \
  })

#define eth_set_pad(idx, enable)                                               \
  ({                                                                           \
    IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx << 1) & ~TX_BD_PAD |                     \
                       (enable ? TX_BD_PAD : 0),                               \
                   idx << 1);                                                  \
  })

#define eth_set_ptr(idx, ptr)                                                  \
  ({ IOB_ETH_SET_BD((uint32_t)ptr, (idx << 1) + 1); })

#endif // H_IOB_ETH_DEFINES_H
