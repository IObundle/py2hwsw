# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
from linux_utils import csr_type


def escape(text):
    return text.replace("_", r"\_")


def create_driver_documentation(output_dir, peripheral):
    """Generate LaTeX documentation for the peripheral's driver."""

    file_path = os.path.join(output_dir, "linux.tex")

    # Get the list of CSRs
    csrs = peripheral["csrs"]

    # Create the LaTeX file content

    # Intro
    content = f"""
This section describes the Linux driver for the {escape(peripheral["name"])} peripheral.
It includes details about the main kernel module, the kernel-user space interfaces it provides for interacting with the peripheral's Control and Status Registers (CSRs), and the available tests to verify the driver's functionality.

The driver consists of:
\\begin{{itemize}}
    \\item A kernel module, implemented in \\texttt{{{escape(peripheral["name"])}\\_main.c}}, which is the core of the driver.
    \\item Three distinct kernel-user space interfaces: \\texttt{{/dev}}, \\texttt{{ioctl}}, and \\texttt{{sysfs}}.
    \\item A set of user space functions with a common API to access the CSRs through any of the interfaces.
    \\item A test suite to validate the driver and the interfaces.
\\end{{itemize}}
"""

    content += f"""
\\subsection{{Kernel Module}}
\\label{{sec:linux_kernel_module}}

The main source code for the kernel module is located in the \\texttt{{{escape(peripheral["name"])}\\_main.c}} file.
This module is implemented as a platform driver, which is responsible for probing and initializing the peripheral device based on information from the device tree.
When the device is detected, the driver maps the peripheral's memory-mapped registers and creates the necessary user space interfaces (\\texttt{{/dev}}, \\texttt{{ioctl}}, and \\texttt{{sysfs}}).
It also implements the file operations (e.g., \\texttt{{read}}, \\texttt{{write}}, \\texttt{{ioctl}}) for the \\texttt{{/dev}} and \\texttt{{ioctl}} interfaces.
"""

    content += f"""
\\subsection{{User Space Interfaces}}
\\label{{sec:linux_user_space_interfaces}}

The driver provides three distinct interfaces for user space applications to interact with the {escape(peripheral["name"])} peripheral: \\texttt{{/dev}}, \\texttt{{ioctl}}, and \\texttt{{sysfs}}.
All three interfaces use a common set of user space functions to access the CSRs, with function prototypes that are similar to those of the bare-metal drivers, providing a consistent API.
\\ifdefined\\DOXYGEN
The baremetal function prototypes are documented in Section~\\ref{{sec:baremetal}}.
\\fi

The following header files must be included in your user space application to use the API:
\\begin{{itemize}}
    \\item \\texttt{{{escape(peripheral["name"])}\\_driver\\_files.h}}
    \\item \\texttt{{{escape(peripheral["name"])}\\_csrs.h}}
\\end{{itemize}}

Before using any of the API functions, you must initialize the library by calling the following function:
\\begin{{verbatim}}
void {peripheral['name']}_csrs_init_baseaddr(uint32_t addr);
\\end{{verbatim}}
For the \\texttt{{/dev}} and \\texttt{{ioctl}} interfaces, this function opens the device file. For the \\texttt{{sysfs}} interface, this function does nothing.

The following sections describe each of these interfaces in detail.
"""

    content += f"""
\\subsubsection{{/dev Interface}}
\\label{{sec:linux_dev_interface}}

The \\texttt{{/dev}} interface allows direct access to the peripheral's registers through the device file \\texttt{{/dev/{escape(peripheral["name"])}}}.
Access to the CSRs is performed by seeking to the appropriate address offset using \\texttt{{lseek()}} and then using \\texttt{{read()}} or \\texttt{{write()}} to access the register.

The following CSRs are available through this interface:
\\begin{{itemize}}
"""
    for csr in csrs:
        csr_name = escape(csr["name"])
        upper_csr_name = escape(csr["name"].upper())
        addr_macro = (
            f"{escape(peripheral['upper_name'])}\\_CSRS\\_{upper_csr_name}\\_ADDR"
        )
        csr_mode = escape(csr["mode"])
        content += f"    \\item \\texttt{{{csr_name}}}: Address: \\texttt{{{addr_macro}}}, Access: {csr_mode}\n"

    content += "\\end{itemize}"

    content += r"""
\subsubsection{ioctl Interface}
\label{sec:linux_ioctl_interface}

The \texttt{ioctl} interface uses I/O control commands to interact with the peripheral.
The function prototypes provided for this interface are identical to the \texttt{/dev} interface functions.

The following IOCTL commands are defined for each CSR:
\begin{itemize}"""
    for csr in csrs:
        csr_name = escape(csr["name"])
        CSR_NAME = escape(csr["name"].upper())
        csr_mode = csr["mode"]
        if "W" in csr_mode:
            content += f"    \\item \\texttt{{WR\\_{{{CSR_NAME}}}}}: Write to the {csr_name} CSR.\n"
        if "R" in csr_mode:
            content += f"    \\item \\texttt{{RD\\_{{{CSR_NAME}}}}}: Read from the {csr_name} CSR.\n"

    content += f"""\\end{{itemize}}

\\subsubsection{{sysfs Interface}}
\\label{{sec:linux_sysfs_interface}}

The \\texttt{{sysfs}} interface exposes the peripheral's registers as files in the system's file system.
The functions prototypes provided for this interface are identical to the \\texttt{{/dev}} interface functions.

The CSRs are exposed as files in the following directory:
\\begin{{verbatim}}
/sys/class/{peripheral['name']}/{peripheral['name']}/
\\end{{verbatim}}

The following files are available for each CSR:
\\begin{{itemize}}"""
    for csr in csrs:
        csr_name = escape(csr["name"])
        csr_mode = escape(csr["mode"])
        if "W" in csr_mode or "R" in csr_mode:
            content += f"    \\item \\texttt{{{csr_name}}}: Access the {csr_name} CSR. (Mode: {escape(csr_mode)})\n"

    content += f"""
\\end{{itemize}}

\\subsection{{User Space Application}}
\\label{{sec:linux_user_space_application}}

User space applications can be developed to interact with the peripheral's driver interfaces. An example application, \\texttt{{user/{escape(peripheral["name"])}\\_user.c}}, is provided for some cores.
Otherwise, the auto-generated test application, \\texttt{{user/{escape(peripheral["name"])}\\_tests.c}}, can serve as a reference for creating custom user space applications.

\\paragraph{{Building an application}}
User space applications can be built using the \\texttt{{Makefile}} located in the \\texttt{{user}} directory. You need to specify the name of your application's source file (without the \\texttt{{.c}} extension) and the desired interface.
\\begin{{verbatim}}
make BIN=<your_app_name> IF=<interface>
\\end{{verbatim}}
The \\texttt{{IF}} variable can be set to \\texttt{{sysfs}}, \\texttt{{dev}}, or \\texttt{{ioctl}} to build the application for the corresponding interface. For example, to build an application from a source file named \\texttt{{my\\_app.c}}, you would run \\texttt{{make BIN=my\\_app IF=sysfs}}.

\\paragraph{{Running the application}}
To run the application, execute the compiled binary in the target Linux system, replacing \\texttt{{<your\\_app\\_name>}} and \\texttt{{<interface>}} with the ones you selected during the build:
\\begin{{verbatim}}
./<your_app_name>_<interface>
\\end{{verbatim}}

\\subsection{{Tests}}
\\label{{sec:linux_tests}}

A test suite is provided to verify the functionality and performance of the driver interfaces.
The test source code is located in \\texttt{{user/{escape(peripheral["name"])}\\_tests.c}}.

\\paragraph{{Building the tests}}
The tests can be built using the \\texttt{{Makefile}} in the \\texttt{{user}} directory by setting the \\texttt{{BIN}} variable to \\texttt{{{escape(peripheral["name"])}\\_tests}}:
\\begin{{verbatim}}
make BIN={peripheral['name']}_tests IF=<interface>
\\end{{verbatim}}
The \\texttt{{IF}} variable can be set to \\texttt{{sysfs}}, \\textt{{dev}}, or \\texttt{{ioctl}} to test the corresponding interface.

\\paragraph{{Running the tests}}
To run the tests, execute the compiled binary in the target Linux system, replacing \\texttt{{<interface>}} with the one you selected during build:
\\begin{{verbatim}}
./{peripheral['name']}_tests_<interface>
\\end{{verbatim}}

The test suite includes:
\\begin{{itemize}}
    \\item \\textbf{{Functionality tests:}} Verify that writing to and reading from Control and Status Registers (CSRs) works correctly.
    \\item \\textbf{{Error Handling tests:}} Simulate faults and verify that appropriate error messages are generated.
    \\item \\textbf{{Performance tests:}} Measure the time taken for a large number of read and write operations to evaluate the interface performance.
\\end{{itemize}}
"""

    # Write the content to the file
    with open(file_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    # Example peripheral dictionary
    peripheral = {
        "name": "iob_timer",
        "instance_name": "timer0",
        "upper_name": "IOB_TIMER",
        "version": "0.1",
        "description": "IOb-Timer, a timer peripheral",
        "author": "IObundle",
        "spdx_year": "2025",
        "spdx_license": "MIT",
        "license": "Dual MIT/GPL",
        "csrs": [
            {"name": "reset", "mode": "W", "n_bits": "1"},
            {"name": "enable", "mode": "W", "n_bits": "1"},
            {"name": "sample", "mode": "W", "n_bits": "1"},
            {"name": "value", "mode": "R", "n_bits": "32"},
            {"name": "version", "mode": "R", "n_bits": "16"},
        ],
        "compatible_str": "iobundle,timer0",
    }

    output_dir = "."
    create_driver_documentation(output_dir, peripheral)

    print(f"Generated LaTeX documentation for {peripheral['name']} in {output_dir}")
