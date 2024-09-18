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
            """
            a_i -s a 1 input
            'Input port a'

            b_i -s b 1 input
            'Input port b'

            c_i -s c 1 input
            'Input port c'

            d_i -s d 1 input
            'Input port d'

            y_o -s y 1 output
            'Output port y'
            """
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
            """
            iob_and iob_and_ab -p W:1 -c
            a_i:a_i
            b_i:b_i
            y_o:and_ab_out
            'First and gate'

            iob_and io_and_cd -p W:1 -c 
            a_i:c_i 
            b_i:d_i 
            y_o:and_cd_out
            'Second and gate'

            iob_or iob_or_abcd -p W:1 -c
            a_i:and_ab_out
            b_i:and_cd_out
            y_o:or_out
            'Or gate'

            iob_inv iob_inv_out -p W:1 -c
            a_i:or_out
            y_o:y_o
            'Inverter'
            """
        ]
    }

    return attributes_dict
