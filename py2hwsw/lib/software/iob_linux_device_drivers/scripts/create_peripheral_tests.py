# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os


def create_peripheral_tests(output_dir, peripheral):
    """Create a C file with tests for the peripheral"""

    # Get the list of CSRs
    csrs = peripheral["csrs"]

    # Find a writable CSR for the invalid write test
    writable_csr_name = None
    for csr in csrs:
        if "W" in csr["mode"]:
            writable_csr_name = csr["name"]
            break

    # Find a read-only CSR for the invalid write test
    readonly_csr_name = "version"  # Default to version CSR

    # Find a write-only CSR for the invalid read test
    writeonly_csr_name = None
    for csr in csrs:
        if "W" in csr["mode"] and "R" not in csr["mode"]:
            writeonly_csr_name = csr["name"]
            break

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
#include <sys/wait.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/ioctl.h>

#include "{peripheral['name']}.h"
#include "{peripheral['name']}_csrs.h"
#include "{peripheral['name']}_driver_files.h"

//
// Test macros
//
#define TEST_PASSED 0
#define TEST_FAILED 1

#define RUN_TEST(test_name) \
    printf("Running test: %s...\\n", #test_name); \
    if (test_name() != TEST_PASSED) {{ \
        printf("Test failed: %s\\n", #test_name); \
        return TEST_FAILED; \
    }} \
    printf("Test passed: %s\\n", #test_name);

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
        printf("Error: Read value (0x%x) does not match written value (0x%x)\\n", read_value, value);
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

    content += f"""
#if defined(DEV_IF)
int test_error_concurrent_open() {{
    /*
     * Test concurrent open calls to the device file.
     * This test is for the dev interface.
     */
    int fd1 = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd1 == -1) {{
        perror("open");
        return TEST_FAILED;
    }}

    int fd2 = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd2 != -1 || errno != EBUSY) {{
        printf("Error: Second open should fail with EBUSY\\n");
        if (fd2 != -1) {{
            close(fd2);
        }}
        close(fd1);
        return TEST_FAILED;
    }}

    close(fd1);
    return TEST_PASSED;
}}

int test_error_invalid_read() {{
    /*
     * Test invalid read calls to the device file.
     * This test is for the dev interface.
     */
    int fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd == -1) {{
        perror("open");
        return TEST_FAILED;
    }}

    char buf;
    #if defined({peripheral['upper_name']}_CSRS_{writeonly_csr_name.upper()}_ADDR)
    lseek(fd, {peripheral['upper_name']}_CSRS_{writeonly_csr_name.upper()}_ADDR, SEEK_SET); // Seek to a write-only CSR
    #else
    lseek(fd, 0xff, SEEK_SET); // Seek to an invalid address
    #endif
    if (read(fd, &buf, 1) != -1 || errno != EACCES) {{
        printf("Error: Invalid read should fail with EACCES\\n");
        close(fd);
        return TEST_FAILED;
    }}

    close(fd);
    return TEST_PASSED;
}}

int test_error_invalid_write() {{
    /*
     * Test invalid write calls to the device file.
     * This test is for the dev interface.
     */
    int fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd == -1) {{
        perror("open");
        return TEST_FAILED;
    }}

    char buf = 0;
    lseek(fd, {peripheral['upper_name']}_CSRS_{readonly_csr_name.upper()}_ADDR, SEEK_SET); // Seek to a read-only CSR
    if (write(fd, &buf, 1) != -1 || errno != EACCES) {{
        printf("Error: Invalid write should fail with EACCES\\n");
        close(fd);
        return TEST_FAILED;
    }}

    close(fd);
    return TEST_PASSED;
}}

int test_error_invalid_llseek() {{
    /*
     * Test invalid llseek calls to the device file.
     * This test is for the dev interface.
     */
    int fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd == -1) {{
        perror("open");
        return TEST_FAILED;
    }}

    if (lseek(fd, 0, -1) != -1 || errno != EINVAL) {{
        printf("Error: Invalid llseek should fail with EINVAL\\n");
        close(fd);
        return TEST_FAILED;
    }}

    close(fd);
    return TEST_PASSED;
}}

#elif defined(IOCTL_IF)
int test_error_invalid_ioctl() {{
    /*
     * Test invalid ioctl calls to the device file.
     * This test is for the ioctl interface.
     */
    int fd = open({peripheral['upper_name']}_DEVICE_FILE, O_RDWR);
    if (fd == -1) {{
        perror("open");
        return TEST_FAILED;
    }}

    if (ioctl(fd, -1, NULL) == 0 || errno != ENOTTY) {{
        printf("Error: Invalid ioctl should fail with ENOTTY. Errno: %d\\n", errno);
        close(fd);
        return TEST_FAILED;
    }}

    close(fd);
    return TEST_PASSED;
}}

#elif defined(SYSFS_IF)
int test_error_sysfs_write_to_readonly() {{
    /*
     * Test writing to a read-only sysfs file.
     * This test is for the sysfs interface.
     */
    char file_path[128];
    sprintf(file_path, "/sys/class/{peripheral['name']}/{peripheral['name']}/version");
    int fd = open(file_path, O_WRONLY);
    if (fd != -1 || errno != EACCES) {{
        printf("Error: Opening a read-only sysfs file for writing should fail with EACCES.\\n");
        if (fd != -1) {{
            close(fd);
        }}
        return TEST_FAILED;
    }}
    return TEST_PASSED;
}}

int test_error_sysfs_read_from_nonexistent() {{
    /*
     * Test reading from a non-existent sysfs file.
     * This test is for the sysfs interface.
     */
    char file_path[128];
    sprintf(file_path, "/sys/class/{peripheral['name']}/{peripheral['name']}/nonexistent");
    int fd = open(file_path, O_RDONLY);
    if (fd != -1 || errno != ENOENT) {{
        printf("Error: Opening a non-existent sysfs file for reading should fail with ENOENT.\\n");
        if (fd != -1) {{
            close(fd);
        }}
        return TEST_FAILED;
    }}
    return TEST_PASSED;
}}
"""

    # Only generate write test if there is a writable CSR
    if writable_csr_name:
        content += f"""
int test_error_sysfs_write_invalid_value() {{
    /*
     * Test writing an invalid value to a sysfs file.
     * This test is for the sysfs interface.
     */
    char file_path[128];
    sprintf(file_path, "/sys/class/{peripheral['name']}/{peripheral['name']}/{writable_csr_name}");
    int fd = open(file_path, O_WRONLY);
    if (fd == -1) {{
        perror("open");
        return TEST_FAILED;
    }}
    if (write(fd, "invalid", 7) != -1 || errno != EINVAL) {{
        printf("Error: Writing an invalid value to a sysfs file should fail with EINVAL.\\n");
        close(fd);
        return TEST_FAILED;
    }}
    close(fd);
    return TEST_PASSED;
}}
#endif  // SYSFS_IF
"""

    content += """
//
// Performance tests
//
"""

    # Generate performance tests for one write register and one read register
    for csr in csrs:
        if "R" in csr["mode"]:
            content += f"""
int test_performance_{csr['name']}_read() {{
    const int num_iterations = 100;
    struct timespec start, end;
    double total_time = 0;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_get_{csr['name']}();
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);

    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("Read performance for {csr['name']}: %f seconds for %d iterations\\n", total_time, num_iterations);

    return TEST_PASSED;
}}
"""
            break  # Only generate one read test

    for csr in csrs:
        if "W" in csr["mode"]:
            content += f"""
int test_performance_{csr['name']}_write() {{
    const int num_iterations = 100;
    struct timespec start, end;
    double total_time = 0;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < num_iterations; i++) {{
        {peripheral['name']}_csrs_set_{csr['name']}(i);
    }}
    clock_gettime(CLOCK_MONOTONIC, &end);

    total_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("Write performance for {csr['name']}: %f seconds for %d iterations\\n", total_time, num_iterations);

    return TEST_PASSED;
}}
"""
            break  # Only generate one write test

    content += f"""
int main() {{
    int ret = 0;

    printf("\\n[User] Version: 0x%x\\n", {peripheral['name']}_csrs_get_version());

    //
    // Run all tests
    //
"""
    for csr in csrs:
        if "W" in csr["mode"]:
            content += f"\n    RUN_TEST(test_functionality_{csr['name']}_write);"
        if "R" in csr["mode"]:
            content += f"\n    RUN_TEST(test_functionality_{csr['name']}_read);"

    content += """
#if defined(DEV_IF)
    RUN_TEST(test_error_concurrent_open);
    RUN_TEST(test_error_invalid_read);
    RUN_TEST(test_error_invalid_write);
    RUN_TEST(test_error_invalid_llseek);
#elif defined(IOCTL_IF)
    RUN_TEST(test_error_invalid_ioctl);
#elif defined(SYSFS_IF)
    RUN_TEST(test_error_sysfs_write_to_readonly);
    RUN_TEST(test_error_sysfs_read_from_nonexistent);
"""
    # Only generate write test if there is a writable CSR
    if writable_csr_name:
        content += """
    RUN_TEST(test_error_sysfs_write_invalid_value);
"""
    content += """
#endif
"""

    for csr in csrs:
        if "W" in csr["mode"]:
            content += f"\n    RUN_TEST(test_performance_{csr['name']}_write);"
            break  # Only call one write performance test
    for csr in csrs:
        if "R" in csr["mode"]:
            content += f"\n    RUN_TEST(test_performance_{csr['name']}_read);"
            break  # Only call one read performance test

    content += """
    if (ret) {
        printf("Tests failed!\\n");
    } else {
        printf("All tests passed!\\n");
    }

    return ret;
}
"""

    # Write the content to the file
    with open(os.path.join(output_dir, f"{peripheral['name']}_tests.c"), "w") as f:
        f.write(content)
