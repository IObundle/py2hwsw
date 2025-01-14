// Tasks based on macros from iob-eth-defines.h

task static eth_tx_ready(input reg [ADDR_W-1:0] idx, output reg ready);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    ready = !((rvalue & `TX_BD_READY) || 0);
  end
endtask
task static eth_rx_ready(input reg [ADDR_W-1:0] idx, output reg ready);
  eth_tx_ready(idx, ready);
endtask

task static eth_bad_crc(input reg [ADDR_W-1:0] idx, output reg bad_crc);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    bad_crc = ((rvalue & `RX_BD_CRC) || 0);
  end
endtask

task static eth_send(input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_MODER(rvalue);
    IOB_ETH_SET_MODER(rvalue & ~`MODER_TXEN | (enable ? `MODER_TXEN : 0));
  end
endtask

task static eth_receive(input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_MODER(rvalue);
    IOB_ETH_SET_MODER(rvalue & ~`MODER_RXEN | (enable ? `MODER_RXEN : 0));
  end
endtask

task static eth_set_ready(input reg [ADDR_W-1:0] idx, input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD(rvalue & ~`TX_BD_READY | (enable ? `TX_BD_READY : 0), idx << 1);
  end
endtask
task static eth_set_empty(input reg [ADDR_W-1:0] idx, input reg enable);
  eth_set_ready(idx, enable);
endtask

task static eth_set_interrupt(input reg [ADDR_W-1:0] idx, input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD(rvalue & ~`TX_BD_IRQ | (enable ? `TX_BD_IRQ : 0), idx << 1);
  end
endtask

task static eth_set_wr(input reg [ADDR_W-1:0] idx, input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD(rvalue & ~`TX_BD_WRAP | (enable ? `TX_BD_WRAP : 0), idx << 1);
  end
endtask

task static eth_set_crc(input reg [ADDR_W-1:0] idx, input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD(rvalue & ~`TX_BD_CRC | (enable ? `TX_BD_CRC : 0), idx << 1);
  end
endtask

task static eth_set_pad(input reg [ADDR_W-1:0] idx, input reg enable);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD(rvalue & ~`TX_BD_PAD | (enable ? `TX_BD_PAD : 0), idx << 1);
  end
endtask

task static eth_set_ptr(input reg [ADDR_W-1:0] idx, input reg [ADDR_W-1:0] ptr);
  IOB_ETH_SET_BD(ptr, (idx << 1) + 1);
endtask

task static eth_reset_bd_memory;
  begin
    integer i;
    for (i = 0; i < 256; i = i + 1) begin
      IOB_ETH_SET_BD(32'h00000000, i);
    end
  end
endtask

task static eth_set_payload_size(input reg [ADDR_W-1:0] idx, input reg [ADDR_W-1:0] size);
  begin
    reg [DATA_W-1:0] rvalue;
    IOB_ETH_GET_BD(idx << 1, rvalue);
    IOB_ETH_SET_BD((rvalue & 32'h0000ffff) | size << 16, idx << 1);
  end
endtask

task static wait_phy_rst;
  reg [DATA_W-1:0] rvalue=1;
  while(rvalue)
    IOB_ETH_GET_PHY_RST_VAL(rvalue);
endtask
