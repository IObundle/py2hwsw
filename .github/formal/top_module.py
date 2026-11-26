#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

"""Print the top module of a generated RTL tree.

The top is the one module that no other module of the tree instantiates: the
rule kepler-formal-action applies when it is given no `top`. The workflow uses
this to pass a reset port only when the top really has it, because the action
rejects a reset port that is not a top-level input (verdict `unsupported`).

Usage: top_module.py <src-dir> [--has-input <port>]
  Prints the top module name. Exits 0 when there is exactly one top (and, with
  --has-input, when that top declares <port> as an input), 1 otherwise.

This is a light text scan of the *.v files (comments removed), enough for the
Verilog that py2hwsw generates; it is not a Verilog parser.
"""

import re
import sys
from pathlib import Path

MODULE = re.compile(r"\bmodule\s+([A-Za-z_]\w*)(.*?)\bendmodule\b", re.S)
COMMENTS = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)


def modules(src: Path) -> dict[str, str]:
    """Map each module defined under `src` to its text."""
    found = {}
    for path in sorted(src.glob("*.v")):
        text = COMMENTS.sub(" ", path.read_text(errors="replace"))
        for match in MODULE.finditer(text):
            found[match.group(1)] = match.group(2)
    return found


def instantiated(name: str, body: str) -> bool:
    # <module> [#(...)] <instance> (   -- the instance name or the "#(" follows
    return re.search(rf"\b{name}\s*(?:#|[A-Za-z_]\w*\s*\()", body) is not None


def main() -> int:
    args = sys.argv[1:]
    port = None
    if len(args) == 3 and args[1] == "--has-input":
        port = args[2]
    elif len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 64
    mods = modules(Path(args[0]))
    tops = [
        name
        for name in mods
        if not any(
            instantiated(name, body) for other, body in mods.items() if other != name
        )
    ]
    if len(tops) != 1:
        print(f"no single top module: {', '.join(tops) or 'none'}", file=sys.stderr)
        return 1
    top = tops[0]
    print(top)
    if port and not re.search(rf"\binput\b[^;,]*?\b{re.escape(port)}\b", mods[top]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
