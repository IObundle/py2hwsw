bsp = [
    {"name": "BAUD", "type": "M", "val": "115200"},
    {"name": "FREQ", "type": "M", "val": "100000000"},
    {"name": "XILINX", "type": "M", "val": "1"},
]


def setup(py_params_dict):
    attributes_dict = {
        "confs": bsp,
    }

    return attributes_dict
