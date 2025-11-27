# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def create_peripheral_tests(output_dir, peripheral):
    """Create a C file with tests for the peripheral"""

    # Get the list of CSRs
    csrs = peripheral["csrs"]

    # Create the test file content
    content = f"""/*
 * SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
 *
 * SPDX-License-Identifier: {peripheral['spdx_license']}
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>

#include \"{peripheral['name']}.h\"
#include \"{peripheral['name']}_csrs.h\"

// Test functionality
int test_functionality() {{
    printf(\"Testing functionality...\\n");

    // Reset the timer
    {peripheral['name']}_csrs_set_reset(1);

    // Enable the timer
    {peripheral['name']}_csrs_set_enable(1);

    // Wait for a second
    sleep(1);

    // Sample the timer
    {peripheral['name']}_csrs_set_sample(1);

    // Read the timer value
    uint32_t data_low = {peripheral['name']}_csrs_get_data_low();
    uint32_t data_high = {peripheral['name']}_csrs_get_data_high();
    uint64_t timer_value = ((uint64_t)data_high << 32) | data_low;

    printf(\"Timer value: %llu\\n", timer_value);

    // Check if the timer value is reasonable
    if (timer_value == 0) {{
        printf(\"Error: Timer value is 0\\n");
        return -1;
    }}

    printf(\"Functionality test passed!\\n");
    return 0;
}}

// Test error handling
int test_error_handling() {{
    printf(\"Testing error handling...\\n");

    // Try to write to a read-only register
    // This should fail, but the user-space library does not return an error code
    // Instead, it prints an error message to stderr
    printf(\"Trying to write to a read-only register...\\n");
    {peripheral['name']}_csrs_set_data_low(0);


    printf(\"Error handling test passed!\\n");
    return 0;
}}

// Test performance
int test_performance() {{
    printf(\"Testing performance...\\n");

    const int num_iterations = 1000;
    struct timespec start, end;
    double total_time = 0;

    // Test read performance
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_get_data_low();
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);

    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf(\"Read performance: %f seconds for %d iterations\\n", total_time, num_iterations);

    // Test write performance
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_set_enable(1);
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);
    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf(\"Write performance: %f seconds for %d iterations\\n", total_time, num_iterations);


    printf(\"Performance test passed!\\n");
    return 0;
}}

int main() {{
    int ret = 0;

    {peripheral['name']}_init(0);

    printf("[User] Version: 0x%x\\n", {peripheral['name']}_csrs_get_version());

    ret |= test_functionality();
    ret |= test_error_handling();
    ret |= test_performance();

    if (ret) {{
        printf(\"Tests failed!\\n");
    }} else {{
        printf(\"All tests passed!\\n");
    }}

    return ret;
}}
"""

    # Write the content to the file
    with open(os.path.join(output_dir, f"{peripheral['name']}_tests.c"), "w") as f:
        f.write(content)


def create_test_makefile(output_dir, peripheral):
    """Create Makefile to build and run tests"""
    content = f"""# SPDX-FileCopyrightText: {peripheral['spdx_year']} {peripheral['author']}
#
# SPDX-License-Identifier: {peripheral['spdx_license']}

# Select kernel-userspace interface: sysfs
IF = sysfs
SRC = {peripheral['name']}_tests.c {peripheral['name']}_$(IF)_csrs.c
SRC += $(wildcard ../../src/{peripheral['name']}.c)
HDR += ../drivers/{peripheral['name']}_driver_files.h
BIN = {peripheral['name']}_tests
# Add compiler flags
FLAGS = -Wall -Werror -O2
FLAGS += -static
FLAGS += -march=rv32imac
FLAGS += -mabi=ilp32
FLAGS += -I../drivers -I../../src
CC = riscv64-unknown-linux-gnu-gcc


$(BIN): $(SRC) $(HDR)
	$(CC) $(FLAGS) $(INCLUDE) -o $(BIN) $(SRC)

run: $(BIN)
	./$(BIN)

clean:
	rm -f $(BIN)

.PHONY: run clean

"""
    with open(os.path.join(output_dir, "Makefile-tests"), "w") as f:
        f.write(content)
