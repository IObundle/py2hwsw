`include "iob_eth_conf.vh"
`include "iob_eth_csrs_def.vh"

/**********************
 * eth_frame_struct.h  
 **********************/
`define ETH_TYPE_H 8'h60
`define ETH_TYPE_L 8'h00

`define ETH_NBYTES 1500
`define ETH_MINIMUM_NBYTES (64-18)

`define HDR_LEN      (2*`IOB_ETH_MAC_ADDR_LEN + 2)

/**********************
 * iob-eth-defines.h  
 **********************/
/* mode register */
`define	MODER_RXEN	(1 <<  0) /* receive enable */
`define	MODER_TXEN	(1 <<  1) /* transmit enable */
`define	MODER_NOPRE	(1 <<  2) /* no preamble */
`define	MODER_BRO	(1 <<  3) /* broadcast address */
`define	MODER_IAM	(1 <<  4) /* individual address mode */
`define	MODER_PRO	(1 <<  5) /* promiscuous mode */
`define	MODER_IFG	(1 <<  6) /* interframe gap for incoming frames */
`define	MODER_LOOP	(1 <<  7) /* loopback */
`define	MODER_NBO	(1 <<  8) /* no back-off */
`define	MODER_EDE	(1 <<  9) /* excess defer enable */
`define	MODER_FULLD	(1 << 10) /* full duplex */
`define	MODER_RESET	(1 << 11) /* FIXME: reset (undocumented) */
`define	MODER_DCRC	(1 << 12) /* delayed CRC enable */
`define	MODER_CRC	(1 << 13) /* CRC enable */
`define	MODER_HUGE	(1 << 14) /* huge packets enable */
`define	MODER_PAD	(1 << 15) /* padding enabled */
`define	MODER_RSM	(1 << 16) /* receive small packets */

/* interrupt source and mask registers */
`define	INT_MASK_TXF	(1 << 0) /* transmit frame */
`define	INT_MASK_TXE	(1 << 1) /* transmit error */
`define	INT_MASK_RXF	(1 << 2) /* receive frame */
`define	INT_MASK_RXE	(1 << 3) /* receive error */
`define	INT_MASK_BUSY	(1 << 4)
`define	INT_MASK_TXC	(1 << 5) /* transmit control frame */
`define	INT_MASK_RXC	(1 << 6) /* receive control frame */

`define	INT_MASK_TX	(`INT_MASK_TXF | `INT_MASK_TXE)
`define	INT_MASK_RX	(`INT_MASK_RXF | `INT_MASK_RXE)

`define	INT_MASK_ALL ( \
		`INT_MASK_TXF | `INT_MASK_TXE | \
		`INT_MASK_RXF | `INT_MASK_RXE | \
		`INT_MASK_TXC | `INT_MASK_RXC | \
		`INT_MASK_BUSY \
	)

/* packet length register */
`define	PACKETLEN_MIN(min)		(((min) & 16'hffff) << 16)
`define	PACKETLEN_MAX(max)		(((max) & 16'hffff) <<  0)
`define	PACKETLEN_MIN_MAX(min, max)	(`PACKETLEN_MIN(min) | \
					`PACKETLEN_MAX(max))

/* transmit buffer number register */
`define	TX_BD_NUM_VAL(x)	(((x) <= 8'h80) ? (x) : 8'h80)

/* control module mode register */
`define	CTRLMODER_PASSALL	(1 << 0) /* pass all receive frames */
`define	CTRLMODER_RXFLOW	(1 << 1) /* receive control flow */
`define	CTRLMODER_TXFLOW	(1 << 2) /* transmit control flow */

/* MII mode register */
`define	MIIMODER_CLKDIV(x)	((x) & 8'hfe) /* needs to be an even number */
`define	MIIMODER_NOPRE		(1 << 8) /* no preamble */

/* MII command register */
`define	MIICOMMAND_SCAN		(1 << 0) /* scan status */
`define	MIICOMMAND_READ		(1 << 1) /* read status */
`define	MIICOMMAND_WRITE	(1 << 2) /* write control data */

/* MII address register */
`define	MIIADDRESS_FIAD(x)		(((x) & 8'h1f) << 0)
`define	MIIADDRESS_RGAD(x)		(((x) & 8'h1f) << 8)
`define	MIIADDRESS_ADDR(phy, reg)	(`MIIADDRESS_FIAD(phy) | \
					`MIIADDRESS_RGAD(reg))

/* MII transmit data register */
`define	MIITX_DATA_VAL(x)	((x) & 16'hffff)

/* MII receive data register */
`define	MIIRX_DATA_VAL(x)	((x) & 16'hffff)

/* MII status register */
`define	MIISTATUS_LINKFAIL	(1 << 0)
`define	MIISTATUS_BUSY		(1 << 1)
`define	MIISTATUS_INVALID	(1 << 2)

/* TX buffer descriptor */
`define	TX_BD_CS		(1 <<  0) /* carrier sense lost */
`define	TX_BD_DF		(1 <<  1) /* defer indication */
`define	TX_BD_LC		(1 <<  2) /* late collision */
`define	TX_BD_RL		(1 <<  3) /* retransmission limit */
`define	TX_BD_RETRY_MASK	(16'h00f0)
`define	TX_BD_RETRY(x)		(((x) & 16'h00f0) >>  4)
`define	TX_BD_UR		(1 <<  8) /* transmitter underrun */
`define	TX_BD_CRC		(1 << 11) /* TX CRC enable */
`define	TX_BD_PAD		(1 << 12) /* pad enable for short packets */
`define	TX_BD_WRAP		(1 << 13)
`define	TX_BD_IRQ		(1 << 14) /* interrupt request enable */
`define	TX_BD_READY		(1 << 15) /* TX buffer ready */
`define	TX_BD_LEN(x)		(((x) & 16'hffff) << 16)
`define	TX_BD_LEN_MASK		(16'hffff << 16)

`define	TX_BD_STATS		(`TX_BD_CS | `TX_BD_DF | `TX_BD_LC | \
				`TX_BD_RL | `TX_BD_RETRY_MASK | `TX_BD_UR)

/* RX buffer descriptor */
`define	RX_BD_LC	(1 <<  0) /* late collision */
`define	RX_BD_CRC	(1 <<  1) /* RX CRC error */
`define	RX_BD_SF	(1 <<  2) /* short frame */
`define	RX_BD_TL	(1 <<  3) /* too long */
`define	RX_BD_DN	(1 <<  4) /* dribble nibble */
`define	RX_BD_IS	(1 <<  5) /* invalid symbol */
`define	RX_BD_OR	(1 <<  6) /* receiver overrun */
`define	RX_BD_MISS	(1 <<  7)
`define	RX_BD_CF	(1 <<  8) /* control frame */
`define	RX_BD_WRAP	(1 << 13)
`define	RX_BD_IRQ	(1 << 14) /* interrupt request enable */
`define	RX_BD_EMPTY	(1 << 15)
`define	RX_BD_LEN(x)	(((x) & 16'hffff) << 16)

`define	RX_BD_STATS	(`RX_BD_LC | `RX_BD_CRC | `RX_BD_SF | `RX_BD_TL | \
			`RX_BD_DN | `RX_BD_IS | `RX_BD_OR | `RX_BD_MISS)

// fields
`define ETH_MAC_ADDR 48'h01606e11020f

// Rx return codes
`define ETH_INVALID_CRC -2
`define ETH_NO_DATA -1
`define ETH_DATA_RCV 0

// Pointers for fields of frame template
`define MAC_DEST_PTR     0
`define MAC_SRC_PTR      (`MAC_DEST_PTR + `IOB_ETH_MAC_ADDR_LEN)
//`define TAG_PTR          (`MAC_SRC_PTR + `IOB_ETH_MAC_ADDR_LEN) // Optional - not supported
`define ETH_TYPE_PTR     (`MAC_SRC_PTR + `IOB_ETH_MAC_ADDR_LEN)
`define PAYLOAD_PTR      (`ETH_TYPE_PTR + 2)

`define TEMPLATE_LEN     (`PAYLOAD_PTR)

`define DWORD_ALIGN(val) ((val + 4'h3) & ~4'h3)

`define ETH_DEBUG_PRINT 1

`ifndef ETH_RMAC_ADDR
`define ETH_RMAC_ADDR `ETH_MAC_ADDR
`endif

`define eth_tx_ready(idx) !((IOB_ETH_GET_BD(idx<<1) & `TX_BD_READY) || 0)
`define eth_rx_ready(idx) eth_tx_ready(idx)

`define eth_bad_crc(idx) ((IOB_ETH_GET_BD(idx<<1) & `RX_BD_CRC) || 0)

`define eth_send(enable) ({\
        IOB_ETH_SET_MODER(IOB_ETH_GET_MODER() & ~`MODER_TXEN | (enable ? `MODER_TXEN : 0));\
        })

`define eth_receive(enable) ({\
        IOB_ETH_SET_MODER(IOB_ETH_GET_MODER() & ~`MODER_RXEN | (enable ? `MODER_RXEN : 0));\
        })

`define eth_set_ready(idx, enable) ({\
        IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx<<1) & ~`TX_BD_READY | (enable ? `TX_BD_READY : 0), idx<<1);\
        })
`define eth_set_empty(idx, enable) eth_set_ready(idx, enable)

`define eth_set_interrupt(idx, enable) ({\
        IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx<<1) & ~`TX_BD_IRQ | (enable ? `TX_BD_IRQ : 0), idx<<1);\
        })

`define eth_set_wr(idx, enable) ({\
        IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx<<1) & ~`TX_BD_WRAP | (enable ? `TX_BD_WRAP : 0), idx<<1);\
        })

`define eth_set_crc(idx, enable) ({\
        IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx<<1) & ~`TX_BD_CRC | (enable ? `TX_BD_CRC : 0), idx<<1);\
        })

`define eth_set_pad(idx, enable) ({\
        IOB_ETH_SET_BD(IOB_ETH_GET_BD(idx<<1) & ~`TX_BD_PAD | (enable ? `TX_BD_PAD : 0), idx<<1);\
        })

`define eth_set_ptr(idx, ptr) ({\
        IOB_ETH_SET_BD((uint32_t)ptr, (idx<<1)+1);\
        })
