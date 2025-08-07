/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef NIST_KAT_RNG_H
#define NIST_KAT_RNG_H

void nist_kat_init(uint8_t *entropy_input,
                   const uint8_t *personalization_string,
                   int security_strength);

#endif
