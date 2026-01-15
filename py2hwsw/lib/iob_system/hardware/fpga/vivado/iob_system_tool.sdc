# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

## Synchronizers
set_property ASYNC_REG TRUE [get_cells -hier {*iob_sync_reg_data_o*[*]}]
