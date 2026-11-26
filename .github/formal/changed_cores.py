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
(at most MAX_USERS of them, in a fixed order). A core that no library core
instantiates (for example iob_memwrapper, which py2hwsw adds around a core by
itself) cannot be checked this way; it is listed in `orphans`.

Writes to $GITHUB_OUTPUT (or stdout):
  cores=<JSON list>          cores to check
  via=<JSON object>          {checked core: changed core it stands for}
  orphans=<JSON list>        cores that need a parent but have no user in the library

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


def setup_files_matching(pattern: str, rev: str, files: set[str]) -> dict[str, str]:
    """{core: setup file} of the cores whose setup file matches `pattern` (ERE)."""
    try:
        hits = git("grep", "-lE", pattern, rev, "--", LIB).splitlines()
    except subprocess.CalledProcessError:  # no match
        return {}
    found = {}
    for hit in hits:
        path = hit.split(":", 1)[1]
        user = core_of(path, files)
        if user and path.endswith(f"/{user}/{user}.py"):
            found[user] = path
    return found


# py2hwsw wraps a top core in iob_memwrapper by itself when the core has a
# memory manager port: a port named <name>_m with a rom_*, ram_* or regfile_*
# interface (see __create_memwrapper in py2hwsw/scripts/iob_core.py). Checking
# such a core (iob_axi_m generates iob_axi_m_mwrap) checks iob_memwrapper.
MEM_MANAGER_PORT = re.compile(
    r'"name":\s*"\w+_m",(?:(?!"name").){0,300}?"type":\s*"(?:rom|ram|regfile)_\w+"',
    re.S,
)


def implicit_users(core: str, rev: str, files: set[str]) -> dict[str, str]:
    """Cores that py2hwsw makes use `core` without them naming it."""
    if core != "iob_memwrapper":
        return {}
    candidates = setup_files_matching(
        '"type":[[:space:]]*"(rom|ram|regfile)_', rev, files
    )
    return {
        user: path
        for user, path in candidates.items()
        if MEM_MANAGER_PORT.search(git("show", f"{rev}:{path}"))
    }


def users_of(core: str, rev: str, files: set[str]) -> list[str]:
    """Cores that instantiate `core`.

    A subblock names its core in a dict, with "core" ("core_name" before
    commit 7fdbc6d8e), or as the first word of a string that starts a line,
    followed by the instance name, such as `iob_csrs csrs -d ...` in an
    f-string (iob_uart, iob_macc). Some cores are also added by py2hwsw itself
    (implicit_users).

    The two forms and the implicit users go through different py2hwsw code,
    so the list takes one user of each kind in turn; within a kind, the cores
    under PREFERRED_USERS_DIR come first, then by name.
    """
    as_dict = f'"(core|core_name)":[[:space:]]*"{core}"'
    as_string = f'^[[:space:]]*[fFrR]{{0,2}}("""|"|\'){core}[[:space:]]+[A-Za-z_]'
    groups = [
        setup_files_matching(as_dict, rev, files),
        setup_files_matching(as_string, rev, files),
        implicit_users(core, rev, files),
    ]
    ranked = [
        sorted(g, key=lambda u, g=g: (not g[u].startswith(PREFERRED_USERS_DIR), u))
        for g in groups
    ]
    users: list[str] = []
    for i in range(max(map(len, ranked))):
        for group in ranked:
            if i < len(group) and group[i] != core and group[i] not in users:
                users.append(group[i])
    return users


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
    orphans: list[str] = []
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
            cores.append(core)  # reported as not checked
            orphans.append(core)
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
        orphans = [core for core in orphans if core in cores]
    print("Cores to check: " + (", ".join(cores) or "none"))

    lines = (
        f"cores={json.dumps(cores)}\nvia={json.dumps(via)}\n"
        f"orphans={json.dumps(orphans)}\n"
    )
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(lines)
    else:
        sys.stdout.write(lines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
