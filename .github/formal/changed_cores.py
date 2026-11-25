#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

"""List the py2hwsw library cores to check between two commits.

A core is a directory under py2hwsw/lib that holds <name>/<name>.py. A changed
file belongs to the closest such directory above it. Only cores present at
both commits are listed, since the check compares the two versions.

Some cores cannot be set up on their own: they are generated for the core
that instantiates them (for example iob_csrs, from the register list of a
peripheral), and their setup reads the `instantiator` or `issuer` parameter.
When such a core changes, the cores that instantiate it are checked instead
(at most MAX_USERS of them, in a fixed order).

Writes to $GITHUB_OUTPUT (or stdout):
  cores=<JSON list>          cores to check
  via=<JSON object>          {checked core: changed core it stands for}

Usage: changed_cores.py <base> <head> [core ...]
  With explicit cores, those are checked instead of the changed ones.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import PurePosixPath

LIB = "py2hwsw/lib"
MAX_CORES = 8
MAX_USERS = 4
# Cores under this directory are listed first among the users of a core.
PREFERRED_USERS_DIR = f"{LIB}/peripherals/"
NEEDS_PARENT = re.compile(
    r"""py_params_dict(?:\.get\(\s*|\[\s*)["'](?:instantiator|issuer)["']"""
)


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


def core_files(files: set[str]) -> dict[str, str]:
    """Map each core name to its setup file."""
    cores = {}
    for path in sorted(files):
        p = PurePosixPath(path)
        if p.suffix == ".py" and p.parent.name == p.stem:
            cores.setdefault(p.stem, path)
    return cores


def needs_parent(rev: str, path: str) -> bool:
    return bool(NEEDS_PARENT.search(git("show", f"{rev}:{path}")))


def users_of(core: str, rev: str, files: set[str]) -> list[str]:
    """Cores whose setup file instantiates `core`, preferred ones first.

    Subblocks name their core with "core" ("core_name" before commit 7fdbc6d8e).
    """
    pattern = f'"(core|core_name)":[[:space:]]*"{core}"'
    try:
        hits = git("grep", "-lE", pattern, rev, "--", LIB).splitlines()
    except subprocess.CalledProcessError:  # no match
        return []
    found = {}
    for hit in hits:
        path = hit.split(":", 1)[1]
        user = core_of(path, files)
        if user and user != core and path.endswith(f"/{user}/{user}.py"):
            found[user] = path
    return sorted(
        found, key=lambda u: (not found[u].startswith(PREFERRED_USERS_DIR), u)
    )


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 64
    base, head, requested = sys.argv[1], sys.argv[2], sys.argv[3:]
    base_files, head_files = tree_files(base), tree_files(head)
    base_cores, head_cores = core_files(base_files), core_files(head_files)

    if requested:
        changed = sorted(set(requested))
    else:
        paths = git("diff", "--name-only", base, head, "--", LIB).splitlines()
        changed = sorted(
            {
                core
                for path in paths
                if (core := core_of(path, head_files))
                and core_of(path, base_files) == core
            }
        )

    cores: list[str] = []
    via: dict[str, str] = {}
    for core in changed:
        path = head_cores.get(core)
        if not path or not needs_parent(head, path):
            if core not in cores:
                cores.append(core)
            continue
        users = [
            user
            for user in users_of(core, head, head_files)
            if user in base_cores and not needs_parent(head, head_cores[user])
        ][:MAX_USERS]
        print(
            f"{core} is set up by the core that instantiates it; checking "
            + (", ".join(users) if users else "no instantiating core found")
        )
        if not users:
            cores.append(core)  # reported as not generated
        for user in users:
            if user not in cores:
                cores.append(user)
                via[user] = core
    # A core changed directly is reported as such, not through another one.
    for core in changed:
        via.pop(core, None)

    if len(cores) > MAX_CORES:
        print(
            f"::notice::{len(cores)} cores to check; checking the first {MAX_CORES}: "
            + ", ".join(cores[:MAX_CORES])
        )
        cores = cores[:MAX_CORES]
        via = {core: via[core] for core in cores if core in via}
    print("Cores to check: " + (", ".join(cores) or "none"))

    lines = f"cores={json.dumps(cores)}\nvia={json.dumps(via)}\n"
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(lines)
    else:
        sys.stdout.write(lines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
