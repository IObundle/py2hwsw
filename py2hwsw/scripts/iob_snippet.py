# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from api_base import internal_api_class


@internal_api_class("user_api.api", "iob_snippet")
@dataclass
class iob_snippet:
    """Py2HWSW's internal implementation of 'iob_snippet' API class."""

    pass


#
# API methods
#


def snippet_from_dict(snippet_dict):
    return iob_snippet(**snippet_dict)


def snippet_text2dict(snippet_text):
    return {"verilog_code": snippet_text}


def snippet_from_text(snippet_text):
    return snippet_from_dict(snippet_text2dict(snippet_text))
