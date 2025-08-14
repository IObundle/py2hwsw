# SPDX-FileCopyrightText: 2025 IObundle, Lda
#
# SPDX-License-Identifier: MIT

# ### Set Ethernet environment variables
# #Eth interface address of pc connected to ethernet peripheral (based on board name)
# $(if $(findstring sim,$(MAKECMDGOALS))$(SIMULATOR),$(eval BOARD=))
# ifeq ($(BOARD),AES-KU040-DB-G)
# ETH_IF ?=eno1
# endif
# ifeq ($(BOARD),CYCLONEV-GT-DK)
# ETH_IF ?= enp0s31f6
# endif
# # Set a MAC address for console (randomly generated)
# RMAC_ADDR ?=88431eafa897
# export RMAC_ADDR
# #Set correct environment if running on IObundle machines
# ifneq ($(filter feynman pudim-flan sericaia,$(shell hostname)),)
# IOB_CONSOLE_PYTHON_ENV ?= /opt/pyeth3/bin/python
# else
# IOB_CONSOLE_PYTHON_ENV ?= {__class__.setup_dir}/submodules/ETHERNET/scripts/pyRawWrapper/pyRawWrapper
# endif


# If running simulation, set eth interface
# ETH_IF ?= eth-$(SIMULATOR)
