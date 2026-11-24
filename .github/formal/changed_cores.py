#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

"""List the py2hwsw library cores changed between two commits.

A core is a directory under py2hwsw/lib that holds <name>/<name>.py. A changed
file belongs to the closest such directory above it. Only cores present at
both commits are listed, since the check compares the two versions.

Writes `cores=<JSON list>` to $GITHUB_OUTPUT (or stdout).

Usage: changed_cores.py <base> <head> [core ...]
  With explicit cores, those are checked instead of the changed ones.
"""

import json
import os
import subprocess
import sys
from pathlib import PurePosixPath

LIB = "py2hwsw/lib"
MAX_CORES = 8


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def tree_files(rev: str) -> set[str]:
    return set(git("ls-tree", "-r", "--name-only", rev, "--", LIB).splitlines())


def core_of(path: str, files: set[str]) -> str | None:
    for parent in PurePosixPath(path).parents:
        if str(parent) == LIB or LIB not in str(parent):
            return None
        if f"{parent}/{parent.name}.py" in files:
            return parent.name
    return None


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 64
    base, head, requested = sys.argv[1], sys.argv[2], sys.argv[3:]
    base_files, head_files = tree_files(base), tree_files(head)

    if requested:
        cores = sorted(set(requested))
    else:
        changed = git("diff", "--name-only", base, head, "--", LIB).splitlines()
        cores = sorted(
            {
                core
                for path in changed
                if (core := core_of(path, head_files))
                and core_of(path, base_files) == core
            }
        )

    if len(cores) > MAX_CORES:
        print(
            f"::notice::{len(cores)} cores changed; checking the first {MAX_CORES}: "
            + ", ".join(cores[:MAX_CORES])
        )
        cores = cores[:MAX_CORES]
    print("Cores to check: " + (", ".join(cores) or "none"))

    line = f"cores={json.dumps(cores)}\n"
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(line)
    else:
        sys.stdout.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
