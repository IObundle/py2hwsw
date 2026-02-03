# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os
from linux_utils import csr_type

def escape(text):
    return text.replace("_", r"\_")

def create_driver_documentation(output_dir, peripheral):
    """Generate LaTeX documentation for the peripheral's driver."""

    print(f"output_dir: {output_dir}")
    file_path = os.path.join(output_dir, "linux.tex")
    print(f"Creating file: {file_path}")

    # Get the list of CSRs
    csrs = peripheral["csrs"]

    # Create the LaTeX file content

    # Intro
    content = f"""
This section provides a detailed description of the Linux user-space software interface for the {escape(peripheral["name"])} peripheral.
The software interface is designed to allow user-space applications to control and monitor the peripheral's Control and Status Registers (CSRs).

The driver for the {escape(peripheral["name"])} peripheral provides three distinct interfaces for user-space applications:
\\begin{{itemize}}
    \\item The \\texttt{{/dev}} interface, which allows direct read/write access to the peripheral's registers through a device file.
    \\item The \\texttt{{ioctl}} interface, which uses I/O control commands to interact with the peripheral.
    \\item The \\texttt{{sysfs}} interface, which exposes the peripheral's registers as files in the system's file system.
\\end{{itemize}}

The following sections describe each of these interfaces in detail.
"""

    content = f"""
\\subsection{{User-Space API}}

The user-space API provides a set of functions to interact with the {escape(peripheral["name"])} peripheral. These functions are available for each of the three interfaces.

The following header files must be included in your user-space application to use the API:
\\begin{{itemize}}
    \\item \\texttt{{{escape(peripheral["name"])}\\_driver\\_files.h}}
    \\item \\texttt{{{escape(peripheral["name"])}\\_csrs.h}}
\\end{{itemize}}

Before using any of the API functions, you must initialize the library by calling the following function:
\\begin{{verbatim}}
void {peripheral['name']}_csrs_init_baseaddr(uint32_t addr);
\\end{{verbatim}}
For the \\texttt{{/dev}} and \\texttt{{ioctl}} interfaces, this function opens the device file. For the \\texttt{{sysfs}} interface, this function does nothing.

\\subsubsection{{/dev Interface}}

The \\texttt{{/dev}} interface allows direct access to the peripheral's registers through the device file \\texttt{{/dev/{escape(peripheral["name"])}}}.
The following functions are provided to interact with the peripheral's CSRs:
"""

    for csr in csrs:
        csr_name = csr["name"]
        csr_mode = csr["mode"]
        data_type = csr_type(csr["n_bits"])

        if "W" in csr_mode:
            content += f"""

\\paragraph{{{escape(peripheral["name"])}\\_csrs\\_set\\_{escape(csr_name)}}}
\\begin{{verbatim}}
void {peripheral['name']}_csrs_set_{csr_name}({data_type} value);
\\end{{verbatim}}
This function writes the given value to the \\texttt{{{escape(csr_name)}}} CSR.

"""

        if "R" in csr_mode:
            content += f"""

\\paragraph{{{escape(peripheral["name"])}\\_csrs\\_get\\_{escape(csr_name)}}}
\\begin{{verbatim}}
{data_type} {peripheral['name']}_csrs_get_{csr_name}();
\\end{{verbatim}}
This function reads the current value of the \\texttt{{{escape(csr_name)}}} CSR and returns it.

"""

    content += r"""
\subsubsection{ioctl Interface}

The \texttt{ioctl} interface uses I/O control commands to interact with the peripheral.
The functions provided for this interface are identical to the \texttt{/dev} interface functions.

The following IOCTL commands are defined for each CSR:
\begin{itemize}"""
    for csr in csrs:
        csr_name = escape(csr["name"])
        CSR_NAME = escape(csr["name"].upper())
        csr_mode = csr["mode"]
        if "W" in csr_mode:
            content += f"    \\item \\texttt{{WR\\_{{{CSR_NAME}}}}}: Write to the {csr_name} CSR.\\\\ \n"
        if "R" in csr_mode:
            content += f"    \\item \\texttt{{RD\\_{{{CSR_NAME}}}}}: Read from the {csr_name} CSR.\\\\ \n"

    content += f"""\\end{{itemize}}

\\subsubsection{{sysfs Interface}}

The \\texttt{{sysfs}} interface exposes the peripheral's registers as files in the system's file system.
The functions provided for this interface are identical to the \\texttt{{/dev}} interface functions.

The CSRs are exposed as files in the following directory:
\\begin{{verbatim}}
/sys/class/{peripheral['name']}/{peripheral['name']}/
\\end{{verbatim}}

The following files are available for each CSR:
\\begin{{itemize}}"""
    for csr in csrs:
        csr_name = escape(csr["name"])
        csr_mode = csr["mode"]
        if "W" in csr_mode or "R" in csr_mode:
            content += f"    \\item \\texttt{{{csr_name}}}: Access the {csr_name} CSR. (Mode: {escape(csr_mode)})\\\\ \n"

    content += f"""
\\end{{itemize}}

\\subsection{{Tests}}

A test suite is provided to verify the functionality and performance of the driver interfaces.
The test source code is located in `user/{escape(peripheral["name"])}\\_tests.c`.

\\paragraph{{Building the tests}}
The tests can be built using the `Makefile` in the `user` directory by setting the `BIN` variable:
\\begin{{verbatim}}
make BIN={peripheral['name']}_tests IF=<interface>
\\end{{verbatim}}
The `IF` variable can be set to `sysfs`, `dev`, or `ioctl` to test the corresponding interface.

Alternatively, a dedicated makefile `user/Makefile-tests` is provided. You can edit this file to select the desired interface.

\\paragraph{{Running the tests}}
To run the tests, execute the compiled binary:
\\begin{{verbatim}}
./{peripheral['name']}_tests
\\end{{verbatim}}
If using `Makefile-tests`, you can simply run:
\\begin{{verbatim}}
make -f user/Makefile-tests run
\\end{{verbatim}}

The test suite includes:
\\begin{{itemize}}
    \\item \\textbf{{Functionality tests:}} Verify that writing to and reading from Control and Status Registers (CSRs) works correctly.
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
