#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from pathlib import Path


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
    # TODO: include / exclude options?
    parser.add_argument(
        "-E",
        "--exclude",
        default=[],
        action="append",
        help="List of files to exclude from coverage.",
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
class CovFile:
    """Represent a Verilator coverage annotation file"""

    path: str = ""
    covered_lines: int = 0
    uncovered_lines: int = 0
    mixed_lines: int = 0

    @property
    def total_lines(self) -> int:
        return self.covered_lines + self.uncovered_lines + self.mixed_lines

    def is_covered(self) -> bool:
        return self.total_lines == self.covered_lines

    @property
    def coverage_level(self) -> float:
        if self.total_lines == 0:
            return 100
        else:
            return (self.covered_lines / self.total_lines) * 100


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


def process_annotated_files(files: list[CovFile]) -> None:
    """Read and process coverage annotation files.
    Update the coverage data structures with information about coverage.
    Check: https://verilator.org/guide/latest/exe_verilator_coverage.html for
    more details.
    Args:
        files list[CovFile]: List of coverage files to process.
    """
    for f in files:
        # read file lines
        with open(f.path, "r") as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                if not tokens:
                    continue  # skip empty lines
                annotation = tokens[0]
                if annotation.isdigit():
                    f.covered_lines += 1
                elif annotation.startswith("%"):
                    f.uncovered_lines += 1
                elif annotation.startswith("~"):
                    f.mixed_lines += 1


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
        for f in files:
            total_lines += f.total_lines
            covered_lines += f.covered_lines
            if f.is_covered():
                covered_files += 1
        rpt.write(f"Total Files: {total_files}\n")
        rpt.write(f"Covered Files: {covered_files}\n")
        rpt.write(f"Files Missing Coverage: {total_files - covered_files}\n\n")
        rpt.write(f"[Covered/Total] Lines: [{covered_lines}/{total_lines}]\n\n")
        global_coverage = (covered_lines / total_lines) * 100
        rpt.write(f"Global Coverage: {global_coverage:.2f} %\n\n")
        rpt.write("=================\n")
        rpt.write("Covered File List\n")
        rpt.write("=================\n")
        rpt.write("File Name\t|\t[Covered/Total lines]\t|\tCoverage (%)\n")
        for f in files:
            rpt.write(
                f"{f.path}\t|\t[{f.covered_lines}/{f.total_lines}]\t|\t"
                f"{f.coverage_level:.2f}%\n"
            )


if __name__ == "__main__":
    print("==============================")
    print("Running Coverage Analysis Tool")
    print("==============================")

    args = parse_arguments()

    # 1. Read annotation files
    cov_files = get_annotated_files(args.annotations, args.exclude)
    # 2. Process annotation files
    process_annotated_files(cov_files)
    # 3. Report Results
    report_results(cov_files, args.output)
