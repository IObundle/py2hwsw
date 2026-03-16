# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Constraints for Smart Zynq SL board, based on: http://www.hellofpga.com/wp-content/uploads/2023/05/SmartZynq_SL_Schematic_V1d3_20241005.pdf
# Demo vivado project for this board: http://www.hellofpga.com/index.php/2023/04/27/smart-zynq_sp_sl_01_led/

create_clock -period 20 -name clk_50 [get_ports clk_50]
set_property -dict {PACKAGE_PIN M19 IOSTANDARD LVCMOS33} [get_ports clk_50]

set_property -dict {PACKAGE_PIN M17 IOSTANDARD LVCMOS33} [get_ports uart_rxd]
set_property -dict {PACKAGE_PIN L17 IOSTANDARD LVCMOS33} [get_ports uart_txd]

set_property -dict {PACKAGE_PIN P20 IOSTANDARD LVCMOS33} [get_ports LED1]
set_property -dict {PACKAGE_PIN P21 IOSTANDARD LVCMOS33} [get_ports LED2]
set_property -dict {PACKAGE_PIN K21 IOSTANDARD LVCMOS33} [get_ports KEY1]
set_property -dict {PACKAGE_PIN J20 IOSTANDARD LVCMOS33} [get_ports KEY2]

set_property -dict {PACKAGE_PIN R20 IOSTANDARD LVCMOS33} [get_ports EEPROM_SCL]
set_property -dict {PACKAGE_PIN R21 IOSTANDARD LVCMOS33} [get_ports EEPROM_SDA]

# RGMII PHY
create_clock -period 8 -name RGMII_rxc [get_ports RGMII_rxc]
set_property -dict {PACKAGE_PIN G21 IOSTANDARD LVCMOS33} [get_ports MDIO_PHY_mdc]
set_property -dict {PACKAGE_PIN H22 IOSTANDARD LVCMOS33} [get_ports MDIO_PHY_mdio_io]
set_property -dict {PACKAGE_PIN A22 IOSTANDARD LVCMOS33} [get_ports {RGMII_rd[0]}]
set_property -dict {PACKAGE_PIN A18 IOSTANDARD LVCMOS33} [get_ports {RGMII_rd[1]}]
set_property -dict {PACKAGE_PIN A19 IOSTANDARD LVCMOS33} [get_ports {RGMII_rd[2]}]
set_property -dict {PACKAGE_PIN B20 IOSTANDARD LVCMOS33} [get_ports {RGMII_rd[3]}]
set_property -dict {PACKAGE_PIN A21 IOSTANDARD LVCMOS33} [get_ports RGMII_rx_ctl]
set_property -dict {PACKAGE_PIN B19 IOSTANDARD LVCMOS33} [get_ports RGMII_rxc]
set_property -dict {PACKAGE_PIN E21 IOSTANDARD LVCMOS33} [get_ports {RGMII_td[0]}]
set_property -dict {PACKAGE_PIN F21 IOSTANDARD LVCMOS33} [get_ports {RGMII_td[1]}]
set_property -dict {PACKAGE_PIN F22 IOSTANDARD LVCMOS33} [get_ports {RGMII_td[2]}]
set_property -dict {PACKAGE_PIN G20 IOSTANDARD LVCMOS33} [get_ports {RGMII_td[3]}]
set_property -dict {PACKAGE_PIN G22 IOSTANDARD LVCMOS33} [get_ports RGMII_tx_ctl]
set_property -dict {PACKAGE_PIN D21 IOSTANDARD LVCMOS33} [get_ports RGMII_txc]
set_property SLEW FAST [get_ports {RGMII_td[0]}]
set_property SLEW FAST [get_ports {RGMII_td[1]}]
set_property SLEW FAST [get_ports {RGMII_td[2]}]
set_property SLEW FAST [get_ports {RGMII_td[3]}]
set_property SLEW FAST [get_ports RGMII_tx_ctl]
set_property SLEW FAST [get_ports RGMII_txc]

## J5 on board (BANK35 V3V3)
# Set voltage level for banks35 (match with jumper setting on board)
set_property IOSTANDARD LVCMOS33 [get_ports {J5[*]}]
set_property PACKAGE_PIN H19 [get_ports {J5[0]}]; #IO_B35_LP19
set_property PACKAGE_PIN H20 [get_ports {J5[1]}]; #IO_B35_LN19
set_property PACKAGE_PIN E18 [get_ports {J5[2]}]; #IO_B35_LN5
set_property PACKAGE_PIN F18 [get_ports {J5[3]}]; #IO_B35_LP5
set_property PACKAGE_PIN F17 [get_ports {J5[4]}]; #IO_B35_LN6
set_property PACKAGE_PIN G17 [get_ports {J5[5]}]; #IO_B35_LP6
set_property PACKAGE_PIN C17 [get_ports {J5[6]}]; #IO_B35_LP11
set_property PACKAGE_PIN C18 [get_ports {J5[7]}]; #IO_B35_LN11
set_property PACKAGE_PIN G19 [get_ports {J5[8]}]; #IO_B35_LP20
set_property PACKAGE_PIN F19 [get_ports {J5[9]}]; #JIO_B35_LN20
set_property PACKAGE_PIN E20 [get_ports {J5[10]}]; #IO_B35_LN21
set_property PACKAGE_PIN E19 [get_ports {J5[11]}]; #IO_B35_LP21
set_property PACKAGE_PIN D22 [get_ports {J5[12]}]; #IO_B35_LP16
set_property PACKAGE_PIN C22 [get_ports {J5[13]}]; #IO_B35_LN16
set_property PACKAGE_PIN B22 [get_ports {J5[14]}]; #IO_B35_LN18
set_property PACKAGE_PIN B21 [get_ports {J5[15]}]; #IO_B35_LP18
set_property PACKAGE_PIN B17 [get_ports {J5[16]}]; #IO_B35_LN8
set_property PACKAGE_PIN B16 [get_ports {J5[17]}]; #IO_B35_LP8
set_property PACKAGE_PIN A17 [get_ports {J5[18]}]; #IO_B35_LN9
set_property PACKAGE_PIN A16 [get_ports {J5[19]}]; #IO_B35_LP9
set_property PACKAGE_PIN D20 [get_ports {J5[20]}]; #IO_B35_LP14
set_property PACKAGE_PIN C20 [get_ports {J5[21]}]; #IO_B35_LN14
set_property PACKAGE_PIN B15 [get_ports {J5[22]}]; #IO_B35_LN7
set_property PACKAGE_PIN C15 [get_ports {J5[23]}]; #IO_B35_LP7
set_property PACKAGE_PIN D17 [get_ports {J5[24]}]; #IO_B35_LN2
set_property PACKAGE_PIN D16 [get_ports {J5[25]}]; #IO_B35_LP2
set_property PACKAGE_PIN D15 [get_ports {J5[26]}]; #IO_B35_LN3
set_property PACKAGE_PIN E15 [get_ports {J5[27]}]; #IO_B35_LP3
set_property PACKAGE_PIN D18 [get_ports {J5[28]}]; #IO_B35_LP12
set_property PACKAGE_PIN C19 [get_ports {J5[29]}]; #IO_B35_LN12
set_property PACKAGE_PIN E16 [get_ports {J5[30]}]; #IO_B35_LN1
set_property PACKAGE_PIN F16 [get_ports {J5[31]}]; #IO_B35_LP1
set_property PACKAGE_PIN G15 [get_ports {J5[32]}]; #IO_B35_LP4
set_property PACKAGE_PIN G16 [get_ports {J5[33]}]; #IO_B35_LN4

## J6 on board (BANK33 VADJ)
# Set voltage level for banks 33 (match with jumper setting on board)
set_property IOSTANDARD LVCMOS33 [get_ports {J6[*]}]
set_property PACKAGE_PIN U22 [get_ports {J6[0]}]; #J6/1 = IO_B33_LN2
set_property PACKAGE_PIN T22 [get_ports {J6[1]}]; #J6/2 = IO_B33_LP2
set_property PACKAGE_PIN W22 [get_ports {J6[2]}]; #J6/3 = IO_B33_LN3
set_property PACKAGE_PIN V22 [get_ports {J6[3]}]; #J6/4 = IO_B33_LP3
set_property PACKAGE_PIN Y21 [get_ports {J6[4]}]; #J6/5 = IO_B33_LN9
set_property PACKAGE_PIN Y20 [get_ports {J6[5]}]; #J6/6 = IO_B33_LP9
set_property PACKAGE_PIN AB22 [get_ports {J6[6]}]; #J6/7 = IO_B33_LN7
set_property PACKAGE_PIN AA22 [get_ports {J6[7]}]; #J6/8 = IO_B33_LP7
set_property PACKAGE_PIN AB21 [get_ports {J6[8]}]; #J6/9 = IO_B33_LN8
set_property PACKAGE_PIN AA21 [get_ports {J6[9]}]; #J6/10 = IO_B33_LP8
set_property PACKAGE_PIN AB19 [get_ports {J6[10]}]; #J6/11 = IO_B33_LP10
set_property PACKAGE_PIN AB20 [get_ports {J6[11]}]; #J6/12 = IO_B33_LN10
set_property PACKAGE_PIN AA19 [get_ports {J6[12]}]; #J6/13 = IO_B33_LN11
set_property PACKAGE_PIN Y19 [get_ports {J6[13]}]; #J6/14 = IO_B33_LP11
set_property PACKAGE_PIN AB16 [get_ports {J6[14]}]; #J6/15 = IO_B33_LN18
set_property PACKAGE_PIN AA16 [get_ports {J6[15]}]; #J6/16 = IO_B33_LP18
set_property PACKAGE_PIN Y18 [get_ports {J6[16]}]; #J6/17 = IO_B33_LP12
set_property PACKAGE_PIN AA18 [get_ports {J6[17]}]; #J6/18 = IO_B33_LN12
set_property PACKAGE_PIN AB14 [get_ports {J6[18]}]; #J6/19 = IO_B33_LP24
set_property PACKAGE_PIN AB15 [get_ports {J6[19]}]; #J6/20 = IO_B33_LN24
set_property PACKAGE_PIN Y13 [get_ports {J6[20]}]; #J6/21 = IO_B33_LP23
set_property PACKAGE_PIN AA13 [get_ports {J6[21]}]; #J6/22 = IO_B33_LN23
set_property PACKAGE_PIN V13 [get_ports {J6[22]}]; #J6/23 = IO_B33_LP20
set_property PACKAGE_PIN W13 [get_ports {J6[23]}]; #J6/24 = IO_B33_LN20
set_property PACKAGE_PIN W18 [get_ports {J6[24]}]; #J6/25 = IO_B33_LN13
set_property PACKAGE_PIN W17 [get_ports {J6[25]}]; #J6/26 = IO_B33_LP13
set_property PACKAGE_PIN AA17 [get_ports {J6[26]}]; #J6/27 = IO_B33_LP17
set_property PACKAGE_PIN AB17 [get_ports {J6[27]}]; #J6/28 = IO_B33_LN17
set_property PACKAGE_PIN W16 [get_ports {J6[28]}]; #J6/29 = IO_B33_LP14
set_property PACKAGE_PIN Y16 [get_ports {J6[29]}]; #J6/30 = IO_B33_LN14
set_property PACKAGE_PIN Y14 [get_ports {J6[30]}]; #J6/31 = IO_B33_LP22
set_property PACKAGE_PIN AA14 [get_ports {J6[31]}]; #J6/32 = IO_B33_LN22
set_property PACKAGE_PIN V15 [get_ports {J6[32]}]; #J6/33 = IO_B33_LN19
set_property PACKAGE_PIN V14 [get_ports {J6[33]}]; #J6/34 = IO_B33_LP19

# Only for board versions V1.0 / V1.1 / V1.2
# HDMI (DVI) outputs
set_property PACKAGE_PIN J21 [get_ports {hdmi_d_p[2]}]
set_property PACKAGE_PIN L21 [get_ports {hdmi_d_p[1]}]
set_property PACKAGE_PIN M21 [get_ports {hdmi_d_p[0]}]
set_property PACKAGE_PIN N22 [get_ports hdmi_clk_p]

# Only for board version V1.3
# # HDMI (DVI) outputs
# set_property PACKAGE_PIN J21 [get_ports {hdmi_d_p[2]}]
# set_property PACKAGE_PIN L21 [get_ports {hdmi_d_p[1]}]
# set_property PACKAGE_PIN M21 [get_ports {hdmi_d_p[0]}]
# set_property PACKAGE_PIN N19 [get_ports hdmi_clk_p]
# set_property -dict {PACKAGE_PIN K20 IOSTANDARD LVCMOS33} [get_ports HDMI_SDA]
# set_property -dict {PACKAGE_PIN K19 IOSTANDARD LVCMOS33} [get_ports HDMI_SCL]
# set_property -dict {PACKAGE_PIN L19 IOSTANDARD LVCMOS33} [get_ports HDMI_RX_HPD]
