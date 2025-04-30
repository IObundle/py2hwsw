# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

interrupt_csrs = [
    {
        "name": "status",
        "mode": "R",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
        "autoreg": True,
        "descr": "Interrupts status: active (1), inactive (0).",
    },
    {
        "name": "mask",
        "mode": "W",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
        "autoreg": True,
        "descr": "Interrupts mask: enable (0), disable (1) for each interrupt.",
    },
    {
        "name": "clear",
        "mode": "W",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
        "autoreg": True,
        "descr": "Interrupts clear: clear (1), do not clear (0) for each interrupt.",
    },
]


def find_and_update_interrupt_csrs(csrs_dict):
    """Given a dictionary of CSRs, find the interrupt CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of mode "INTERRUPT". This CSR will be replaced by interrupt_csrs.
    """
    csr_group_ref = None
    csr_ref = None
    for csr_group in csrs_dict:
        for csr in csr_group["regs"]:
            if csr["mode"] == "INTERRUPT":
                csr_group_ref = csr_group
                csr_ref = csr
                break
        if csr_ref:
            break

    if not csr_ref:
        return

    # Add interrupt_csrs to group
    csr_group_ref["regs"] += interrupt_csrs

    # Remove original csr from csr_group
    csr_group_ref["regs"].remove(csr_ref)
