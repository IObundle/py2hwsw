/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#pragma once
#include "iob_timer_csrs.h"

// Functions

/**
 * @brief Resets the timer peripheral.
 */
void timer_reset();

/**
 * @brief Initializes the timer peripheral.
 *
 * This function sets the base address, resets the timer, and enables it.
 *
 * @param base_address The base memory address of the timer.
 */
void timer_init(uint32_t base_address);

/**
 * @brief Reads the current 64-bit timer count.
 *
 * This function samples the timer and returns the current count value
 * as a 64-bit unsigned integer.
 *
 * @return uint64_t The current timer count in clock cycles.
 */
uint64_t timer_get_count();

/**
 * @brief Sets the timer interrupt threshold.
 *
 * This function sets a 64-bit threshold value across two 32-bit CSRs.
 * Interrupts are generated when the timer count reaches this threshold.
 * Setting both high and low parts to zero disables interrupts.
 *
 * @param threshold The 64-bit threshold value.
 */
void timer_set_interrupt(uint64_t threshold);
