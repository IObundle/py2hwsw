# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#  UART 1 / rx / uart_rxd
set_property iostandard "LVCMOS33" [get_ports "rs232_rxd_i_0"]
set_property PACKAGE_PIN "V12" [get_ports "rs232_rxd_i_0"]

#  UART 1 / tx / uart_txd
set_property iostandard "LVCMOS33" [get_ports "rs232_txd_o_0"]
set_property PACKAGE_PIN "W16" [get_ports "rs232_txd_o_0"]


#set_property iostandard "LVCMOS33" [get_ports "led0_0"]
#set_property PACKAGE_PIN "D18" [get_ports "led0_0"]

#set_property iostandard "LVCMOS33" [get_ports "led3_0"]
#set_property PACKAGE_PIN "M14" [get_ports "led3_0"]
