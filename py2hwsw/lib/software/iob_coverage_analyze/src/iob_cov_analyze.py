#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="coverage_analyze.py",
        description="""Verilator Coverage Analysis Script.
        Run this tool to analyze verilator coverage annotations.
        """,
    )
    parser.add_argument(
        "annotations",
        default=".",
        help="Path to verilator coverage annotations.",
    )
    parser.add_argument(
        "-E",
        "--exclude",
        default=[],
        action="append",
        help="List of files to exclude from coverage.",
    )
    parser.add_argument(
        "-W",
        "--waive",
        default=[],
        action="append",
        help="List of waive files.",
    )
    parser.add_argument(
        "-T",
        "--waived-tag",
        action="store_true",
        help="Tag waived lines in verilog coverage annotations. Replaces annotation with `%waived`",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="coverage.rpt",
        help="Output report file.",
    )
    args = parser.parse_args()
    return args


@dataclass
class WaiveRule:
    """Represent a Verilator coverage waive rule"""

    file: str = ""
    line_start: int = 0
    line_end: int = 0
    reason: str = ""


def create_waive_rule(line: str) -> WaiveRule:
    """Create a waive rule from a line in a waive file.
    waive rules format:
        waive filename:line_start[:line_end]] "reason"
    Example:
        waive reg.v:10 "Clock is always enabled"
        waive prio_enc.v:30:34 "Unused Generate Block Configuration"

    Args:
        line str: Line from waive file.
    Returns:
        WaiveRule: Waive rule object.
    """
    tokens = line.split()
    if len(tokens) < 3:
        raise ValueError(f"Invalid waive rule: {line}")
    parts = tokens[1].split(":")
    file = parts[0]
    line_start = int(parts[1])
    line_end = int(parts[2]) if len(parts) > 2 else line_start
    reason = " ".join(tokens[2:]).strip('"').strip("'")
    return WaiveRule(file, line_start, line_end, reason)


@dataclass
class CovFile:
    """Represent a Verilator coverage annotation file"""

    path: str = ""
    covered_lines: int = 0
    waived_lines: int = 0
    uncovered_lines: int = 0
    mixed_lines: int = 0
    waive_rules: list[WaiveRule] = field(default_factory=list)

    @property
    def total_lines(self) -> int:
        return (
            self.covered_lines
            + self.uncovered_lines
            + self.mixed_lines
            + self.waived_lines
        )

    def is_covered(self) -> bool:
        return self.total_lines == (self.covered_lines + self.waived_lines)

    @property
    def coverage_level(self) -> float:
        if self.total_lines == 0:
            return 100
        else:
            return ((self.covered_lines + self.waived_lines) / self.total_lines) * 100

    @property
    def filename(self) -> str:
        return self.path.split("/")[-1]

    @property
    def waived_line_numbers(self) -> list[int]:
        """
        Returns:
            list[str]: List of line number to waive.
        """
        excluded_lines = []
        # get all waived lines
        for rule in self.waive_rules:
            excluded_lines += list(range(rule.line_start, rule.line_end + 1))
        # remove repeated lines
        return list(set(excluded_lines))

    def process(self) -> None:
        """Read and process coverage annotation file.
        Update the coverage data structures with information about coverage.
        Check: https://verilator.org/guide/latest/exe_verilator_coverage.html for
        more details.
        """
        # read file lines
        with open(self.path, "r") as file:
            lines = self.exclude_waives(file.readlines())
            for line in lines:
                tokens = line.split()
                if not tokens:
                    continue  # skip empty lines
                annotation = tokens[0]
                if annotation.isdigit():
                    self.covered_lines += 1
                elif annotation.startswith("%"):
                    self.uncovered_lines += 1
                elif annotation.startswith("~"):
                    self.mixed_lines += 1

    def tag_waived_lines(self) -> None:
        """Read and process coverage annotation file.
        Update the coverage data structures with information about coverage.
        Check: https://verilator.org/guide/latest/exe_verilator_coverage.html for
        more details.
        """
        # read file lines
        lines = []
        with open(self.path, "r") as file:
            lines = file.readlines()
        waived_line_numbers = self.waived_line_numbers
        for lnum in waived_line_numbers:
            # replace waived line annotation with %waived
            lines[lnum - 1] = re.sub(r"[%~]([0-9]+)", "%waived", lines[lnum - 1], count=1)
        with open(self.path, "w") as file:
            file.writelines(lines)

    def exclude_waives(self, lines: list[str]) -> list[str]:
        """Exclude waived lines from coverage analysis.
        Args:
            lines list[str]:
        Returns:
            list[str]: List of lines excluding waived lines.
        """
        excluded_lines = self.waived_line_numbers
        # exclude waived lines
        filtered_lines = [
            line
            for lnum, line in enumerate(lines, start=1)
            if lnum not in excluded_lines
        ]
        # update waived lines count
        self.waived_lines = len(excluded_lines)
        return filtered_lines


def get_annotated_files(path: str, exclude: list[str]) -> list[CovFile]:
    """Get all verilog coverage annotation file in path.
    Args:
        path str: Path to search for coverage annotation files.
        exclude list[str]: List of files to exclude from coverage.
    Returns:
        list[CovFile]: List of Coverage Files.
    """
    files = list(Path(path).rglob("*.v"))
    cov_files: list[CovFile] = []
    for f in files:
        if str(f.name) in exclude:
            continue  # skip excluded files
        cov_files.append(
            CovFile(
                path=str(f),
            )
        )
    return cov_files


def add_waive_rules(cov_files: list[CovFile], waive_files: list[str]):
    """Add waive rules to waive files.
    Args:
        cov_files list[CovFile]: List of coverage files.
        waive_files list[str]: List of waive files.
    """
    rules: list[WaiveRule] = []
    for wf in waive_files:
        with open(wf, "r") as waive_file:
            lines = waive_file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("waive"):
                    rules.append(create_waive_rule(line))
    # attach rules to specific coverage files
    for rule in rules:
        for cov_file in cov_files:
            if cov_file.filename == rule.file:
                cov_file.waive_rules.append(rule)
                break
    return rules


def process_annotated_files(files: list[CovFile], waived_tag: bool) -> None:
    """Read and process coverage annotation files.
    Update the coverage data structures with information about coverage.
    Check: https://verilator.org/guide/latest/exe_verilator_coverage.html for
    more details.
    Args:
        files list[CovFile]: List of coverage files to process.
        waived_tag bool: Tag waived lines in verilog coverage annotations.
    """
    for f in files:
        f.process()
        if waived_tag:
            f.tag_waived_lines()


def report_results(files: list[CovFile], output: str) -> None:
    """Generate a coverage report from the processed coverage files.
    Args:
        files list[CovFile]: List of coverage files to report on.
        output str: Output report file path.
    """
    with open(output, "w") as rpt:
        rpt.write("==========================\n")
        rpt.write("Verilator Coverage Summary\n")
        rpt.write("==========================\n")
        total_files = len(files)
        covered_files = 0
        total_lines = 0
        covered_lines = 0
        waived_lines = 0
        for f in files:
            total_lines += f.total_lines
            covered_lines += f.covered_lines
            waived_lines += f.waived_lines
            if f.is_covered():
                covered_files += 1
        rpt.write(f"Total Files: {total_files}\n")
        rpt.write(f"Covered Files: {covered_files}\n")
        rpt.write(f"Files Missing Coverage: {total_files - covered_files}\n\n")
        rpt.write(f"[Covered/Total] Lines: [{covered_lines}/{total_lines}]\n\n")
        if total_lines == 0:
            global_coverage = 100.0
        else:
            global_coverage = ((covered_lines + waived_lines) / total_lines) * 100
        rpt.write(f"Global Coverage: {global_coverage:.2f} %\n\n")
        rpt.write("=================\n")
        rpt.write("Covered File List\n")
        rpt.write("=================\n")
        rpt.write("File Name\t|\t[(Covered+Waived)/Total lines]\t|\tCoverage (%)\n")
        for f in files:
            rpt.write(
                f"{f.path}\t|\t[({f.covered_lines}+{f.waived_lines})/{f.total_lines}]\t|\t"
                f"{f.coverage_level:.2f}%\n"
            )


if __name__ == "__main__":
    print("==============================")
    print("Running Coverage Analysis Tool")
    print("==============================")

    args = parse_arguments()

    # 1. Read annotation files
    cov_files = get_annotated_files(args.annotations, args.exclude)
    # 2. Add waive rules to coverage files
    add_waive_rules(cov_files, args.waive)
    # 3. Process annotation files
    process_annotated_files(cov_files, args.waived_tag)
    # 4. Report Results
    report_results(cov_files, args.output)
