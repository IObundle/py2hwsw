# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

## System Clock 
# System clock already created in aes_ku040_db_g.tcl
#create_clock -name "clk" -period 4.0 [get_ports {c0_sys_clk_clk_p_i}]

# LVDS Programmable Clock Generator (CDCM61002)
#set_property  PACKAGE_PIN M5   [get_ports LVDS_CLK0_N]
#set_property  PACKAGE_PIN M6   [get_ports LVDS_CLK0_P]
#set_property  PACKAGE_PIN P5   [get_ports LVDS_CLK1_N]
#set_property  PACKAGE_PIN P6   [get_ports LVDS_CLK1_P]

#set_property  IOSTANDARD LVDS [get_ports LVDS_CLK0_N]
#set_property  IOSTANDARD LVDS [get_ports LVDS_CLK0_P]
#set_property  IOSTANDARD LVDS [get_ports LVDS_CLK1_N]
#set_property  IOSTANDARD LVDS [get_ports LVDS_CLK1_P]

##DDR clocks
set_property PACKAGE_PIN H22 [get_ports {c0_sys_clk_clk_p_i}]
set_property PACKAGE_PIN H23 [get_ports {c0_sys_clk_clk_n_i}]
set_property IOSTANDARD DIFF_SSTL12 [get_ports {c0_sys_clk_clk_p_i}]
set_property IOSTANDARD DIFF_SSTL12 [get_ports {c0_sys_clk_clk_n_i}]

set_property CONFIG_VOLTAGE 2.5 [current_design]

#derive_pll_clocks
#derive_clock_uncertainty

set_property CFGBVS VCCO [current_design]

## USB-UART Interface
set_property PACKAGE_PIN D20 [get_ports {txd_o}]
set_property IOSTANDARD LVCMOS18 [get_ports {txd_o}]
set_property PACKAGE_PIN C19 [get_ports {rxd_i}]
set_property IOSTANDARD LVCMOS18 [get_ports {rxd_i}]

###### User LEDs
#set_property PACKAGE_PIN D16 [get_ports {led[6]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[6]}]

#set_property PACKAGE_PIN G16 [get_ports {led[5]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[5]}]

#set_property PACKAGE_PIN H16 [get_ports {led[4]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[4]}]

#set_property PACKAGE_PIN E18 [get_ports {led[3]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[3]}]

#set_property PACKAGE_PIN E17 [get_ports {led[2]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[2]}]

#set_property PACKAGE_PIN E16 [get_ports {led[1]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[1]}]

#set_property PACKAGE_PIN H18 [get_ports {led[0]}]
#set_property IOSTANDARD LVCMOS18 [get_ports {led[0]}]

#set_property PACKAGE_PIN H17 [get_ports {trap}]
#set_property IOSTANDARD LVCMOS18 [get_ports {trap}]

####### User PUSH Switches
#set_property PACKAGE_PIN N24 [get_ports {areset_i}]
#set_property IOSTANDARD LVCMOS12 [get_ports {areset_i}]
set_property PACKAGE_PIN K20 [get_ports {areset_i}]
set_property IOSTANDARD LVCMOS12 [get_ports {areset_i}]

#set_property PACKAGE_PIN K18 [get_ports {gpio_push_sw_tri_i[0]}]
#set_property IOSTANDARD LVCMOS12 [get_ports {gpio_push_sw_tri_i[0]}]

#set_property PACKAGE_PIN L18 [get_ports {gpio_push_sw_tri_i[1]}]
#set_property IOSTANDARD LVCMOS12 [get_ports {gpio_push_sw_tri_i[1]}]

#set_property PACKAGE_PIN K21 [get_ports {gpio_push_sw_tri_i[2]}]
#set_property IOSTANDARD LVCMOS12 [get_ports {gpio_push_sw_tri_i[2]}]

#set_property PACKAGE_PIN K20 [get_ports {gpio_push_sw_tri_i[3]}]
#set_property IOSTANDARD LVCMOS12 [get_ports {gpio_push_sw_tri_i[3]}]
