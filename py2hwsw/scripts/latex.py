#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Script with LaTeX related functions

import re


def write_table(outfile, table, unbreakable_rows=4):
    """
    unbreakable_rows: configures the amount of rows from the start of the table that should not be broken. This avoids the table from breaking on the first N rows. Set to zero to allow breaking on any row.
    """

    """Write Latex table contents"""
    fout = open(outfile + "_tab.tex", "w")
    for i in range(len(table)):
        if (i % 2) != 0:
            fout.write("\\rowcolor{iob-blue}\n")
        line = table[i]
        # Escape special characters
        for j in range(len(line)):
            line[j] = escape_latex(str(line[j]))
        # if one of the elements has matching parenthesis, remove the enclosing ones
        for j in range(len(line)):
            if line[j].count("(") == line[j].count(")") and line[j].count("(") > 0:
                if line[j][0] == "(" and line[j][-1] == ")":
                    line[j] = line[j][1:-1]
        # Assemble the line
        line_out = str(line[0])
        for num in range(1, len(line)):
            line_out = line_out + (" & %s" % line[num])

        if i == len(table)-1:
            # Don't insert \\hline (or \nobreakhline) at the last row to prevent latex from breaking the table before footer
            row_end = r"\\"
        elif i < unbreakable_rows-1:
            # Insert special \nobreakhline at the end of unbreakable rows. This prevents latex from breaking the table into a new page on the first rows.
            row_end = r"\\* \nobreakhline"
        else:
            # Allow breaking into new page
            row_end = r"\\ \hline"

        # Write the line
        fout.write(line_out + f" {row_end}\n")

    fout.close()
    return


def write_description(outfile, text):
    """Write Latex description"""
    fout = open(outfile + "_desc.tex", "w")
    for line in text:
        fout.write("\\item[" + line[0] + "] " + "{" + line[1] + "}\n")
    fout.close()


def escape_latex(s):
    """Given a string, escape latex special characters"""
    latex_special_chars = r"[&%$#_{}~^]"
    escaped_str = s.replace("\\", "\\textbackslash ")
    escaped_str = re.sub(
        latex_special_chars, lambda match: "\\" + match.group(), escaped_str
    )
    escaped_str = escaped_str.replace("<", "\\textless ").replace(">", "\\textgreater ")
    escaped_str = escaped_str.replace("$clog2", "log2")
    return escaped_str
