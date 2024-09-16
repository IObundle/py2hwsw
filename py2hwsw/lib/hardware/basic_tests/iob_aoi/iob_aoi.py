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
                "name": "a",
                "descr": "Input port",
                "signals": [
                    {"name": "a", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "b",
                "descr": "Input port",
                "signals": [
                    {"name": "b", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "c",
                "descr": "Input port",
                "signals": [
                    {"name": "c", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "d",
                "descr": "Input port",
                "signals": [
                    {"name": "d", "width": 1, "direction": "input"},
                ],
            },
            {
                "name": "y",
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
                    "a i": "a",
                    "b i": "b",
                    "y o": "and_ab_out",
                },
            },
            """
            iob_and io_and_cd -p W 1 -c 
            'a i' c 
            'b i' d 
            'y o' d_cd_out
            'Second and gate'
            """,
            {
                "core_name": "iob_or",
                "instance_name": "iob_or_abcd",
                "parameters": {
                    "W": 1,
                },
                "connect": {
                    "a input": "and_ab_out",
                    "b input": "and_cd_out",
                    "y output": "or_out",
                },
            },
            {
                "core_name": "iob_inv",
                "instance_name": "iob_inv_out",
                "parameters": {
                    "W": 1,
                },
                "connect": {
                    "a": "or_out",
                    "y": "y",
                },
            },
        ],
    }

    return attributes_dict
