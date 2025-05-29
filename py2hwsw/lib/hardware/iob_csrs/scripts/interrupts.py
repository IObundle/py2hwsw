# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from copy import deepcopy

interrupt_csrs = [
    {
        "name": "status",
        "mode": "R",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
        "descr": "Interrupts status: active (1), inactive (0).",
    },
    {
        "name": "mask",
        "mode": "W",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
    },
    {
        "name": "clear",
        "mode": "W",
        "n_bits": 32,
        "rst_val": 0,
        "log2n_items": 0,
        "descr": "Interrupts clear: clear (1), do not clear (0) for each interrupt.",
    },
]


def find_and_update_interrupt_csrs(csrs_dict):
    """Given a dictionary of CSRs, find the interrupt CSRs group and update the dictionary
    accordingly.
    User should provide a CSR of type "INTERRUPT". This CSR will be replaced by interrupt_csrs.
    """
    csr_group_ref = None
    csr_ref = None
    for csr_group in csrs_dict:
        for csr in csr_group["regs"]:
            if csr.get("type", "") == "INTERRUPT":
                csr_group_ref = csr_group
                csr_ref = csr
                break
        if csr_ref:
            break

    if not csr_ref:
        return

    _interrupt_csrs = deepcopy(interrupt_csrs)
    for csr in _interrupt_csrs:
        # Update name of csrs to include original csr name as a prefix
        csr["name"] = f"{csr_ref['name']}_{csr['name']}"

    # Add interrupt_csrs to group
    csr_group_ref["regs"] += _interrupt_csrs

    # Remove original csr from csr_group
    csr_group_ref["regs"].remove(csr_ref)
