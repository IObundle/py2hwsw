#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

"""Collect the formal equivalence results of the checked cores in one table.

Usage:
  report.py row <core> <generation-status> <message> <result.json> <row.json>
      Write the result of one core (run by each SEC job).
  report.py table <rows-dir>
      Append the table of all rows to $GITHUB_STEP_SUMMARY (or stdout).
      The cores expected are read from $CORES (JSON list) so that a job
      without a result still shows up; $BASE and $HEAD name the commits.
"""

import json
import os
import sys
from pathlib import Path

ICONS = {
    "equivalent": "✅",
    "identical": "➖",
    "different": "⚠️",
    "partially_proved": "🟡",
    "setup-broken": "⚠️",
    "not-generated": "🚫",
}


def write_row(core: str, generation: str, message: str, result: str, out: str) -> None:
    row = {"core": core, "generation": generation, "message": message}
    result_path = Path(result)
    if result_path.is_file():
        data = json.loads(result_path.read_text())
        for key in ("verdict", "covered_outputs", "total_outputs", "elapsed_seconds"):
            row[key] = data.get(key)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(row))


def outcome(row: dict) -> str:
    if row["generation"] == "identical":
        return "identical"
    if row["generation"] in ("setup-broken", "not-generated"):
        return row["generation"]
    if row["generation"] != "changed":
        return "not-generated"
    return row.get("verdict") or "no verdict"


def write_table(rows_dir: str) -> None:
    rows = {}
    for path in Path(rows_dir).glob("*.json"):
        row = json.loads(path.read_text())
        rows[row["core"]] = row
    cores = json.loads(os.environ.get("CORES") or "[]") or sorted(rows)
    base, head = os.environ.get("BASE", "")[:9], os.environ.get("HEAD", "")[:9]

    lines = [
        "### Formal equivalence of the changed cores",
        "",
        f"`{base}` → `{head}`" if base and head else "",
        "",
        "| Core | Result | Outputs covered | Time | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for core in cores:
        row = rows.get(core)
        if row is None:
            lines.append(f"| `{core}` | ❔ no result | | | job did not complete |")
            continue
        result = outcome(row)
        icon = ICONS.get(result, "❔")
        outputs = ""
        if row.get("total_outputs"):
            outputs = f"{row.get('covered_outputs')}/{row['total_outputs']}"
        seconds = row.get("elapsed_seconds")
        time = "" if seconds is None else f"{seconds:.0f} s" if seconds >= 1 else "< 1 s"
        notes = row["message"].replace("|", "\\|")
        lines.append(f"| `{core}` | {icon} {result} | {outputs} | {time} | {notes} |")
    lines += [
        "",
        "Details per core: the job summaries below (counterexample traces) and the "
        "`formal-<core>` artifacts (logs, py2hwsw setup output).",
    ]

    text = "\n".join(lines) + "\n"
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(text)
    sys.stdout.write(text)


def main() -> int:
    if len(sys.argv) == 7 and sys.argv[1] == "row":
        write_row(*sys.argv[2:])
        return 0
    if len(sys.argv) == 3 and sys.argv[1] == "table":
        write_table(sys.argv[2])
        return 0
    print(__doc__, file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main())
