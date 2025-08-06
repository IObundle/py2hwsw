# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

UTARGETS=tb
TB_INCLUDES=-I./src -I./simulation/src
TB_SRC+=./simulation/src/iob_s_axi_m_sim_controller_csrs.c
TB_SRC+=./src/iob_s_axi_m.c
