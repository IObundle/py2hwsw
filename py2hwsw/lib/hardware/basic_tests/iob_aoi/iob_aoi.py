# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    """Standard py2hwsw setup method
    This method is called during the py2hwsw setup process to obtain the dictionary of
    attributes for this core.
    param py_params_dict: Dictionary of py2hwsw instance parameters
    returns: Py2hwsw dictionary of core attributes
    """
    # Dictionary that describes this core using the py2hw dictionary interface
    attributes_dict = {
        "version": "0.1",
        "confs": [
            """
            W -t P -v 1 -m 1 -M 32
            'Ports width'
            """
        ],
        "ports": [
            """
            a_i -s a W input
            'Input port a'

            b_i -s b W input
            'Input port b'

            c_i -s c W input
            'Input port c'

            d_i -s d W input
            'Input port d'

            y_o -s y W output
            'Output port y'
            """
        ],
        "wires": [
            """
            and_ab_out -s aab W
            'and ab output'

            and_cd_out -s cad W
            'and cd output'

            or_out -s oab 1
            'or output'
            """,
        ],
        "blocks": [
            """
            iob_and iob_and_ab -p W:W -c
            a_i:a_i
            b_i:b_i
            y_o:and_ab_out
            'First and gate'

            iob_and io_and_cd -p W:W -c 
            a_i:c_i 
            b_i:d_i 
            y_o:and_cd_out
            'Second and gate'

            iob_or iob_or_abcd -p W:W -c
            a_i:and_ab_out
            b_i:and_cd_out
            y_o:or_out
            'Or gate'

            iob_inv iob_inv_out -p W:W -c
            a_i:or_out
            y_o:y_o
            'Inverter'
            """
        ],
    }

    return attributes_dict
