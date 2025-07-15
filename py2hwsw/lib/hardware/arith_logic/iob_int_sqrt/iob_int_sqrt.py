# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    attributes_dict = {
        "generate_hw": True,
        "confs": [
            """
            DATA_W -t P -v 32 -m NA -M NA
            -d 'Data bus width'

            FRACTIONAL_W -t P -v 0 -m NA -M NA
            -d 'Fractional part width'

            REAL_W -t P -v 'DATA_W - FRACTIONAL_W' -m NA -M NA
            -d 'Real part width'

            SIZE_W -t P -v '(REAL_W / 2) + FRACTIONAL_W' -m NA -M NA
            -d 'Size width'

            END_COUNT -t D -v '(DATA_W + FRACTIONAL_W) >> 1' -m NA -M NA
            -d 'End count'

            COUNT_W -t D -v $clog2(END_COUNT) -m NA -M NA
            -d 'Count width'
            """,
        ],
        "ports": [
            {
                "name": "start_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "start_i",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "op_i",
                "descr": "Input port",
                "wires": [
                    {
                        "name": "op_i",
                        "width": "DATA_W",
                    },
                ],
            },
            {
                "name": "done_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "done_o",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Output port",
                "wires": [
                    {
                        "name": "res_o",
                        "width": "SIZE_W",
                    },
                ],
            },
        ],
        "buses": [
            {
                "name": "right",
                "descr": "right bus",
                "wires": [
                    {"name": "right", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "left",
                "descr": "left bus",
                "wires": [
                    {"name": "left", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "a_in",
                "descr": "a_in bus",
                "wires": [
                    {"name": "a_in", "width": "DATA_W"},
                ],
            },
            {
                "name": "tmp",
                "descr": "tmp bus",
                "wires": [
                    {"name": "tmp", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "q",
                "descr": "q bus",
                "wires": [
                    {"name": "q", "width": "SIZE_W"},
                ],
            },
            {
                "name": "counter",
                "descr": "counter bus",
                "wires": [
                    {"name": "counter", "width": "COUNT_W"},
                ],
            },
            {
                "name": "a",
                "descr": "a bus",
                "wires": [
                    {"name": "a", "width": "DATA_W"},
                ],
            },
            {
                "name": "r",
                "descr": "r bus",
                "wires": [
                    {"name": "r", "width": "SIZE_W+2"},
                ],
            },
        ],
        "fsm": {
            "default_assignments": """
        right = {q, r[SIZE_W+1], 1'b1};
        left = {r[SIZE_W-1:0], a[DATA_W-1 -: 2]};
        a_in = {a[DATA_W-3:0], 2'b00};
        tmp =  r[SIZE_W+1] ? left + right : left - right;
        res_o = q;
        done_o = ~pcnt;
""",
            "state_descriptions": """
        idle:
            if (start_i) begin
                a_nxt = op_i;
                q_nxt = 0;
                r_nxt = 0;
                counter_nxt = 0;
            end else begin
                pcnt_nxt = pcnt;
            end

            r_nxt = tmp;
            q_nxt = {q[SIZE_W-2:0], ~tmp[SIZE_W+1]};
            a_nxt = a_in;
            if (counter != END_COUNT[COUNT_W-1:0] - 1) begin
                counter_nxt = counter + 1'b1;
                pcnt_nxt = pcnt;
            end else begin
                pcnt_nxt = idle; end
""",
        },
    }
    return attributes_dict
