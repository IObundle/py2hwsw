# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Constraints for Smart Zynq SL board
# Based on: http://www.hellofpga.com/wp-content/uploads/2023/05/SmartZynq_SL_Schematic_V1d3_20241005.pdf

# PL Input Clock (50MHz)
#set_property -dict {PACKAGE_PIN M19 IOSTANDARD LVCMOS33} [get_ports clk_50]
#create_clock -period 20.000 -name clk_50 [get_ports clk_50]

# UART (connected to PL pins)
set_property -dict {PACKAGE_PIN M17 IOSTANDARD LVCMOS33} [get_ports uart_rxd_i]
set_property -dict {PACKAGE_PIN L17 IOSTANDARD LVCMOS33} [get_ports uart_txd_o]

# LEDs
set_property -dict {PACKAGE_PIN P20 IOSTANDARD LVCMOS33} [get_ports {led_o[0]}]
set_property -dict {PACKAGE_PIN P21 IOSTANDARD LVCMOS33} [get_ports {led_o[1]}]

# Keys
set_property -dict {PACKAGE_PIN K21 IOSTANDARD LVCMOS33} [get_ports {key_i[0]}]
set_property -dict {PACKAGE_PIN J20 IOSTANDARD LVCMOS33} [get_ports {key_i[1]}]

# Reset signal if used from a button (e.g. KEY1)
# set_property -dict {PACKAGE_PIN K21 IOSTANDARD LVCMOS33} [get_ports reset_i]

# DDR and Fixed IO pins are handled by the PS and don't usually need explicit constraints in the XDC
# as they are defined by the PS7 IP block.
