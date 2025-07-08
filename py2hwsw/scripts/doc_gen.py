# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#
#    doc_gen.py: generate documentation
#
import os

import config_gen
import io_gen
import block_gen

from latex import write_table, escape_latex
from iob_base import fail_with_msg, find_path, get_lib_cores


def generate_docs(core):
    """Generate common documentation files"""
    if core.is_top_module:
        config_gen.generate_confs_tex(core.confs, core.build_dir + "/document/tsrc")
        io_gen.generate_ios_tex(core.ports, core.build_dir + "/document/tsrc")
        block_gen.generate_subblocks_tex(
            core.subblocks, core.build_dir + "/document/tsrc"
        )
        generate_py_params_tex(
            core.python_parameters, core.build_dir + "/document/tsrc"
        )
        generate_tex_file(
            core.build_dir + "/document/tsrc/rn_overview.tex", core.description
        )
        generate_tex_file(core.build_dir + "/document/tsrc/name.tex", core.title)
        generate_tex_file(
            core.build_dir + "/document/tsrc/description.tex", core.description
        )


def generate_tex_file(file_path, contents):
    """Generate TeX file with given contents
    :param str file_path: Path to the file
    :param str contents: TeX contents
    """
    with open(file_path, "w") as f:
        f.write(escape_latex(contents))


def generate_tex_py2hwsw_attributes(iob_core_instance, out_dir):
    """Generate TeX table of supported attributes of the py2hwsw interface.
    The attributes listed can be used in the 'attributes' dictionary of cores.
    :param iob_core_instance: Dummy instance of the iob_core class. Used to obtain attributes of iob_core.
    :param out_dir: Path to the output directory
    """

    tex_table = []
    for name in iob_core_instance.ATTRIBUTE_PROPERTIES.keys():
        tex_table.append(
            [
                name,
                iob_core_instance.ATTRIBUTE_PROPERTIES[name].datatype,
                iob_core_instance.ATTRIBUTE_PROPERTIES[name].descr,
            ]
        )

    write_table(f"{out_dir}/py2hwsw_attributes", tex_table)


def generate_tex_py2hwsw_standard_py_params(out_dir):
    """Generate TeX table of standard Python Parameters given by py2hwsw to every core.
    The Python Parameters listed are always received in the argument of the core's setup() function.
    :param iob_core_instance: Dummy instance of the iob_core class. Used to obtain python parameters of iob_core.
    :param out_dir: Path to the output directory
    """

    tex_table = [
        [
            "core_name",
            str,
            "Name of current core (determined by the core's file name).",
        ],
        [
            "build_dir",
            str,
            "Build directory of this core. Usually defined by `--build-dir` flag or issuer.",
        ],
        [
            "py2hwsw_target",
            str,
            "The reason why py2hwsw is invoked. Usually `setup` meaning the Py2HWSW is calling the core's script to obtain information on how to generate the core. May also be other targets like `clean`, `print_attributes`, or `deliver`. These are usually to obtain information about the core for various purposes, but not to generate the build directory.",
        ],
        [
            "issuer",
            dict,
            "Core dictionary with attributes of the issuer core (if any). Allows subblocks to obtain information about their issuer core.",
        ],
        [
            "py2hwsw_version",
            str,
            "Version of Py2HWSW.",
        ],
    ]

    write_table(f"{out_dir}/py2hwsw_py_params", tex_table)


def generate_tex_core_lib(out_dir):
    """Generate TeX table of cores available in py2hwsw library.
    :param out_dir: Path to the output directory
    """
    lib_path = os.path.join(os.path.dirname(__file__), "../lib")

    tex_table = []
    cores = get_lib_cores()
    for path in cores:
        file = os.path.basename(path)
        dir = os.path.dirname(path)
        tex_table.append([os.path.splitext(file)[0], os.path.relpath(dir, lib_path)])

    write_table(f"{out_dir}/py2hwsw_core_lib", tex_table)


def generate_py_params_tex(python_parameters, out_dir):
    """Generate TeX section for python parameters of given core.
    :param list python_parameters: list of python parameter groups
    :param str out_dir: path to output directory
    """

    py_params_file = open(f"{out_dir}/py_params.tex", "w")

    # FIXME: These python parameters are only used during the setup process. So from the point of view of the build directory, they are not needed.
    # Maybe we should have a user guide specific for the setup stage?
    py_params_file.write(
        """
The following tables describe the supported \\textit{Python Parameters} for the setup of this IP core.
Note that these \\textit{Python Parameters} are not used during the build process of this core from this build directory.
They only serve a purpose during the setup process, to configure how the core build directory will be generated.
See the \\textit{Python Parameters} section of the \\href{https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/py2hwsw_document/document/ug.pdf}{Py2HWSW User Guide} for more details.
"""
    )

    for group in python_parameters:
        py_params_file.write(
            """
\\begin{xltabular}{\\textwidth}{|l|c|X|}

  \\hline
  \\rowcolor{iob-green}
  {\\bf Name} & {\\bf Default Value} & {\\bf Description} \\\\ \\hline \\hline

  \\input """
            + group.name
            + """_py_params_tab

  \\caption{"""
            + group.descr.replace("_", "\\_")
            + """}
\\end{xltabular}
\\label{"""
            + group.name
            + """_py_params_tab:is}
"""
        )
        if group.doc_clearpage:
            py_params_file.write("\\clearpage")

    py_params_file.close()

    generate_py_params_tex_table(python_parameters, out_dir)


def generate_py_params_tex_table(python_parameters, out_dir):
    """Create TeX table for each python parameter group in given list.
    :param list python_parameters: list of python parameter groups
    :param str out_dir: path to output directory
    """

    for group in python_parameters:
        tex_table = []
        for param in group.python_parameters:
            tex_table.append(
                [
                    param.name,
                    param.value,
                    param.descr,
                ]
            )

        # Write table with true parameters and macros
        write_table(f"{out_dir}/{group.name}_py_params", tex_table)


def process_tex_macros(tex_src_dir):
    """Search for special macros in TeX sources and replace them with appropriate values.
    :param tex_src_dir: Path to directory with TeX sources to be processed
    """
    tex_files = [f for f in os.listdir(tex_src_dir) if f.endswith(".tex")]

    for file in tex_files:
        with open(os.path.join(tex_src_dir, file), "r") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            if line.strip().startswith("% py2_macro:"):
                lines[idx] = process_tex_macro(line)

        with open(os.path.join(tex_src_dir, file), "w") as f:
            f.writelines(lines)


#
# Methods to parse python code
#


def get_method_body(start_idx, lines):
    method_body = [lines[start_idx]]
    # Count how many spaces are at the beginning of the line to find indentation of method body
    indentation = len(lines[start_idx + 1]) - len(lines[start_idx + 1].lstrip())
    idx = start_idx + 1
    # Copy method body, including blank lines
    while idx < len(lines) and (
        lines[idx] == "\n" or len(lines[idx]) - len(lines[idx].lstrip()) >= indentation
    ):
        method_body.append(lines[idx])
        idx += 1
    # Remove ending blank lines
    idx = -1
    while method_body[idx] == "\n":
        method_body.pop()
        idx -= 1
    return method_body


def get_class_body(start_idx, lines):
    return get_method_body(start_idx, lines)


def get_class_attributes(start_idx, lines):
    class_body = get_method_body(start_idx, lines)
    idx = start_idx
    # Copy everything before first def
    for idx, line in enumerate(class_body):
        if line.strip().startswith("def"):
            return class_body[:idx]
    return []


def get_attribute_contents(start_idx, lines):
    attribute_contents = [lines[start_idx]]
    # Find attribute body start char
    first_char = lines[start_idx].replace(" ", "").split("=")[1][0]
    delimiter_chars = {"(": ")", "[": "]", "{": "}"}
    if first_char in delimiter_chars.keys():
        attribute_contents = lines[start_idx].split("=")[0] + " = "
        content_str = "".join(lines[start_idx:]).split("=")[1].lstrip()
        idx = 1
        delimiter_char_count = 1
        while delimiter_char_count > 0:
            if content_str[idx] == first_char:
                delimiter_char_count += 1
            elif content_str[idx] == delimiter_chars[first_char]:
                delimiter_char_count -= 1
            idx += 1
        attribute_contents += content_str[:idx]

    return attribute_contents.splitlines(keepends=True)


def get_between_lines(lines, start_line, end_line=None):
    start_idx = -1
    for idx, line in enumerate(lines):
        if start_line in line:
            start_idx = idx
            break

    if start_idx == -1:
        fail_with_msg(f"Could not find '{start_line}' in content:\n{''.join(lines)}")

    end_idx = len(lines)
    if end_line:
        for idx, line in enumerate(lines[start_idx:]):
            if end_line in line:
                end_idx = start_idx + idx
                break

    return lines[start_idx:end_idx]


#
# End of methods to parse python code
#


def process_tex_macro(line):
    """Given a TeX macro line, return a new (multi)line with appropriate value."""
    macro = line.strip().split(":")[1].strip().split()
    macro_command = macro[0]
    listing_content = ""
    file_path = None
    file_extension = None

    def _find_file(file):
        """Local function to find file, and print error otherwise"""
        filename, extension = file.split(".")
        if "/" in filename:
            filename = filename.split("/")[-1]
        extension = "." + extension
        found_file = find_path(os.path.join(os.path.dirname(__file__), ".."), file)
        if not found_file:
            fail_with_msg(f"File '{file}' not found! From macro line '{line}'.")
        # Update file path and extension for use in TeX
        nonlocal file_path
        nonlocal file_extension
        file_path = found_file[len(os.path.join(os.path.dirname(__file__), "..")) + 1 :]
        file_extension = extension
        return found_file

    if macro_command == "listing":
        # Search for given attribute/class/method, and print its body
        code_obj_name = macro[1]
        file = _find_file(macro[macro.index("from") + 1])
        with open(file, "r") as f:
            # Search for start line and print lines after it
            _lines = f.readlines()
            for idx, _line in enumerate(_lines):
                if _line.strip().startswith("def " + code_obj_name):
                    # Copy method body
                    listing_content = "".join(get_method_body(idx, _lines))
                    break
                elif _line.strip().startswith(code_obj_name):
                    # Copy attribute body
                    listing_content = "".join(get_attribute_contents(idx, _lines))
                    break
                elif _line.strip().startswith("class " + code_obj_name):
                    # Copy class body
                    listing_content = "".join(get_class_body(idx, _lines))
                    break
    elif macro_command == "class_attributes":
        # Search for given class, and print only its attributes (not methods)
        class_name = macro[1]
        file = _find_file(macro[macro.index("from") + 1])
        # Copy class attributes
        with open(file, "r") as f:
            _lines = f.readlines()
            for idx, _line in enumerate(_lines):
                if _line.strip().startswith("class " + class_name):
                    listing_content = "".join(get_class_attributes(idx, _lines))
    elif macro_command == "file":
        # Replace with content of given file
        file = _find_file(macro[1])
        # Copy file contents
        with open(file, "r") as f:
            listing_content = f.read()
    elif macro_command == "start_line":
        # Search for start line and print lines after it
        start_line = macro[1]
        # If start_line has quotes, find ending quote as well
        if start_line.startswith('"'):
            idx = 1
            while not macro[idx].endswith('"'):
                idx += 1
            start_line = " ".join(macro[1:idx])[1:-1]

        file = _find_file(macro[macro.index("from") + 1])

        end_line = None
        if "end_line" in macro:
            idx = macro.index("end_line")
            end_line = macro[idx + 1]

            # If end_line has quotes, find ending quote as well
            if end_line.startswith('"'):
                while not macro[idx].endswith('"'):
                    idx += 1
                end_line = " ".join(macro[1:idx])[1:-1]

        with open(file, "r") as f:
            _lines = f.readlines()
            listing_content = "".join(get_between_lines(_lines, start_line, end_line))
    else:
        fail_with_msg(f"Unknown macro command '{macro_command}' in line '{line}'!")

    languages = {
        ".py": "python",
        ".sh": "bash",
        ".c": "c",
        ".cpp": "cpp",
    }
    lang_snippet = ""
    if file_extension in languages:
        lang_snippet = f"[language={languages[file_extension]}]"
    source_link = ""
    if file_path:
        source_link = f"\href{{https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/{file_path}}}{{View Source}}"

    return f"""
\\begin{{lstlisting}}{lang_snippet}
{listing_content}
\\end{{lstlisting}}
{source_link}
"""
