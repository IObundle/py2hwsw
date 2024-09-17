def setup(py_params_dict):
    """Standard py2hwsw setup method
    This method is called during the py2hwsw setup process to obtain the dictionary of
    attributes for this core.
    param py_params_dict: Dictionary of py2hwsw instance parameters
    returns: Py2hwsw dictionary of core attributes
    """
    # Dictionary that describes this core using the py2hw dictionary interface
    attributes_dict = {
        "original_name": "iob_aoi",
        "name": "iob_aoi",
        "version": "0.1",
        "ports": [
            {
                "name": "a_i",
                "descr": "Input port",
                "signals": [
                    {"name": "a", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "b_i",
                "descr": "Input port",
                "signals": [
                    {"name": "b", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "c_i",
                "descr": "Input port",
                "signals": [
                    {"name": "c", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "d_i",
                "descr": "Input port",
                "signals": [
                    {"name": "d", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "y_o",
                "descr": "Output port",
                "signals": [
                    {"name": "y", "width": 1, "direction": "output"},
                ],
            },
        ],
        "wires": [
            """
            and_ab_out -s aab 1
            'and ab output'

            and_cd_out -s cad 1
            'and cd output'

            or_out -s oab 1
            'or output'
            """,
        ],
        "blocks": [
            {
                "core_name": "iob_and",
                "instance_name": "iob_and_ab",
                "parameters": {
                    "W": 1,
                },
                "connect": {
                    "a_i": "a_i",
                    "b_i": "b_i",
                    "y_o": "and_ab_out",
                },
            },
            """
            iob_and io_and_cd -p W:1 -c 
            a_i:c_i 
            b_i:d_i 
            y_o:and_cd_out
            'Second and gate'
            """,
            {
                "core_name": "iob_or",
                "instance_name": "iob_or_abcd",
                "parameters": {
                    "W": 1,
                },
                "connect": {
                    "a_i": "and_ab_out",
                    "b_i": "and_cd_out",
                    "y_o": "or_out",
                },
            },
            {
                "core_name": "iob_inv",
                "instance_name": "iob_inv_out",
                "parameters": {
                    "W": 1,
                },
                "connect": {
                    "a_i": "or_out",
                    "y_o": "y_o",
                },
            },
        ],
    }

    return attributes_dict
