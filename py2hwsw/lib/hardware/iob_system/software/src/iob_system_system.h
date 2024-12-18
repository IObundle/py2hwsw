/*
 * SPDX-FileCopyrightText: 2024 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#define B_BIT 31 // Bootrom selection bit
#define P_BIT 30 // Peripheral bus selection bit

// peripheral bus base
#define PBUS_BASE ((1 << 31) | (1 << P_BIT))

#define BOOTROM_BASE (1 << B_BIT)
