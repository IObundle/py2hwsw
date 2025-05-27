#  UART 1 / rx / uart_rxd
set_property iostandard "LVCMOS33" [get_ports "uart_rxd"]
set_property PACKAGE_PIN "V12" [get_ports "uart_rxd"]
set_property slew "slow" [get_ports "uart_rxd"]
set_property drive "8" [get_ports "uart_rxd"]
set_property pullup "TRUE" [get_ports "uart_rxd"]
set_property PIO_DIRECTION "INPUT" [get_ports "uart_rxd"]

#  UART 1 / tx / uart_txd
set_property iostandard "LVCMOS33" [get_ports "uart_txd"]
set_property PACKAGE_PIN "W16" [get_ports "uart_txd"]
set_property slew "slow" [get_ports "uart_txd"]
set_property drive "8" [get_ports "uart_txd"]
set_property pullup "TRUE" [get_ports "uart_txd"]
set_property PIO_DIRECTION "OUTPUT" [get_ports "uart_txd"]