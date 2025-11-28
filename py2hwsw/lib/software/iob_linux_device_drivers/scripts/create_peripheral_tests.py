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

//
// Test macros
//
#define TEST_PASSED 0
#define TEST_FAILED 1

#define RUN_TEST(test_name) \
    printf(\"Running test: %s...\\n\", #test_name); \
    if (test_name() != TEST_PASSED) {{ \
        printf(\"Test failed: %s\\n\", #test_name); \
        return TEST_FAILED; \
    }} \
    printf(\"Test passed: %s\\n\", #test_name);

//
// Functionality tests
//
"""

    for csr in csrs:
        if "W" in csr["mode"]:
            content += f"""
int test_functionality_{csr['name']}_write() {{
    uint32_t value = 0x12345678;
    {peripheral['name']}_csrs_set_{csr['name']}(value);
"""
            if "R" in csr["mode"]:
                content += f"""
    uint32_t read_value = {peripheral['name']}_csrs_get_{csr['name']}();
    if (read_value != value) {{
        printf(\"Error: Read value (0x%x) does not match written value (0x%x)\\n\", read_value, value);
        return TEST_FAILED;
    }}
"""
            content += """
    return TEST_PASSED;
}
"""
        if "R" in csr["mode"]:
            content += f"""
int test_functionality_{csr['name']}_read() {{
    {peripheral['name']}_csrs_get_{csr['name']}();
    return TEST_PASSED;
}}
"""

    content += """
//
// Error handling tests
//
"""

    for csr in csrs:
        if "W" not in csr["mode"]:
            content += f"""
int test_error_handling_{csr['name']}_write() {{
    // This should fail, but the user-space library does not return an error code
    // Instead, it prints an error message to stderr
    {peripheral['name']}_csrs_set_{csr['name']}(0);
    return TEST_PASSED;
}}
"""
        if "R" not in csr["mode"]:
            content += f"""
int test_error_handling_{csr['name']}_read() {{
    // This should fail, but the user-space library does not return an error code
    // Instead, it prints an error message to stderr
    {peripheral['name']}_csrs_get_{csr['name']}();
    return TEST_PASSED;
}}
"""

    content += """
//
// Performance tests
//
"""

    for csr in csrs:
        if "R" in csr["mode"]:
            content += f"""
int test_performance_{csr['name']}_read() {{
    const int num_iterations = 1000;
    struct timespec start, end;
    double total_time = 0;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_get_{csr['name']}();
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);

    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf(\"Read performance for {csr['name']}: %f seconds for %d iterations\\n\", total_time, num_iterations);

    return TEST_PASSED;
}}
"""
        if "W" in csr["mode"]:
            content += f"""
int test_performance_{csr['name']}_write() {{
    const int num_iterations = 1000;
    struct timespec start, end;
    double total_time = 0;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_set_{csr['name']}(i);
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);

    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf(\"Write performance for {csr['name']}: %f seconds for %d iterations\\n\", total_time, num_iterations);

    return TEST_PASSED;
}}
"""

    content += """
int main() {
    int ret = 0;

    printf(\"[User] Version: 0x%x\\n\", iob_timer_csrs_get_version());

    //
    // Run all tests
    //
"""
    for csr in csrs:
        if "W" in csr["mode"]:
            content += f"\n    RUN_TEST(test_functionality_{csr['name']}_write);"
        if "R" in csr["mode"]:
            content += f"\n    RUN_TEST(test_functionality_{csr['name']}_read);"
        if "W" not in csr["mode"]:
            content += f"\n    RUN_TEST(test_error_handling_{csr['name']}_write);"
        if "R" not in csr["mode"]:
            content += f"\n    RUN_TEST(test_error_handling_{csr['name']}_read);"
        if "R" in csr["mode"]:
            content += f"\n    RUN_TEST(test_performance_{csr['name']}_read);"
        if "W" in csr["mode"]:
            content += f"\n    RUN_TEST(test_performance_{csr['name']}_write);"

    content += """
    if (ret) {
        printf(\"Tests failed!\\n");
    } else {
        printf(\"All tests passed!\\n");
    }

    return ret;
}
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