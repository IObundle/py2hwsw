#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Script with LaTeX related functions

import re


def write_table(outfile, table):
    """Write Latex table"""
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
        # Write the line
        fout.write(line_out + " \\\\ \\hline\n")

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
    latex_special_chars = r"[&%$#_{}~^\\]"
    escaped_str = re.sub(latex_special_chars, lambda match: "\\" + match.group(), s)
    escaped_str = escaped_str.replace("<", "\\textless ").replace(">", "\\textgreater ")
    escaped_str = escaped_str.replace("$clog2", "log2")
    return escaped_str
