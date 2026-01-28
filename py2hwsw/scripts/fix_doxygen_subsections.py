#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import re
import sys
from pathlib import Path


def extract_input_files(doxygen_tex_path: Path) -> set[Path]:
    """
    Parse doxygen.tex to find all \\input{...} under the 'File Documentation' chapter.
    Returns a set of Path objects (without assuming an extension).
    """
    text = doxygen_tex_path.read_text(encoding="utf-8")

    inputs = set()
    for match in re.finditer(r"\\input\{([^}]+)\}", text):
        name = match.group(1)
        # Assuume input files are in 'latex/' directory
        p = Path("latex/" + name)
        # If no extension, assume .tex
        if p.suffix == "":
            p = p.with_suffix(".tex")
        if not p.is_absolute():
            p = doxygen_tex_path.parent / p
        inputs.add(p)

    return inputs


def remove_orphaned_doxysubsections(tex_path: Path) -> None:
    """
    If tex_path contains exactly one '\\doxysubsection{', change it to
    '\\doxysubsection*{' and write back the file.
    """
    if not tex_path.is_file():
        return

    content = tex_path.read_text(encoding="utf-8")

    # Count occurrences without modifying first
    occurrences = len(re.findall(r"\\doxysubsection\{", content))
    if occurrences == 1:
        # Replace that single occurrence with the starred version
        new_content = content.replace(r"\doxysubsection{", r"\doxysubsection*{", 1)
        tex_path.write_text(new_content, encoding="utf-8")


def remove_orphaned_doxysections(files: list[Path]) -> None:
    """
    If tex_path contains exactly one file and file only has a single
    '\\doxysection{', change it to
    '\\doxysection*{' and write back the file.
    """
    # if more than 1 file, assume multiple doxysections
    if len(files) == 1:
        tex_path = list(files)[0]

        if not tex_path.is_file():
            return

        content = tex_path.read_text(encoding="utf-8")

        # Count section and subsection occurrences
        section_occurrences = len(re.findall(r"\\doxysection\{", content))
        subsection_occurrences = len(re.findall(r"\\doxysubsection\{", content))

        # Only remove section if it's the only one and it has no subsections
        if section_occurrences == 1 and subsection_occurrences == 0:
            # Replace that single occurrence with the starred version
            new_content = content.replace(r"\doxysection{", r"\doxysection*{", 1)
            tex_path.write_text(new_content, encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_doxygen_subsections.py DOXYGEN_TEX", file=sys.stderr)
        sys.exit(1)

    doxygen_tex_path = Path(sys.argv[1]).resolve()
    inputs = extract_input_files(doxygen_tex_path)

    for tex_file in inputs:
        remove_orphaned_doxysubsections(tex_file)

    remove_orphaned_doxysections(inputs)


if __name__ == "__main__":
    main()
