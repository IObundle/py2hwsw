# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

UTARGETS=tb
TB_INCLUDES=-I./src -I./simulation/src
CSRS+=./simulation/src/iob_s_axi_m_sim_controller_csrs.c
CSRS+=./src/iob_s_axi_m.c
