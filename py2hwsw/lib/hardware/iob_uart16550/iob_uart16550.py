def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "version": "0.1",
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "clk_en_rst",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "cbus_s",
                "signals": {
                    "type": "iob",
                    "ADDR_W": 5,
                },
                "descr": "CPU native interface",
            },
            {
                "name": "rs232_m",
                "signals": {
                    "type": "rs232",
                },
                "descr": "RS232 interface",
            },
            {
                "name": "interrupt_o",
                "descr": "UART16550 interrupt related signals",
                "signals": [
                    {
                        "name": "interrupt_o",
                        "width": "1",
                        "descr": "UART interrupt source",
                    },
                ],
            },
        ],
        "subblocks": [
            {
                "core_name": "iob_iob2wishbone",
                "instantiate": False,
            },
        ],
    }

    return attributes_dict
