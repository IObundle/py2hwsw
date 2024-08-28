def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_int_sqrt",
        "name": "iob_int_sqrt",
        "version": "0.1",
        "confs": [
            "DATA_W P 32 $mNA $MNA $D'Data bus width'",
            "FRACTIONAL_W P 0 $mNA $MNA $D'Fractional part width'",
            "REAL_W P 'DATA_W - FRACTIONAL_W' $mNA $MNA $D'Real part width'",
            "SIZE_W P '(REAL_W / 2) + FRACTIONAL_W' $mNA $MNA $D'Size width'",
            "END_COUNT F '(DATA_W + FRACTIONAL_W) >> 1' $mNA $MNA $D'End count'",
            "COUNT_W F '$clog2(END_COUNT)' $mNA $MNA $D'Count width'",
        ],
        "ports": [
            {
                "name": "start_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "start",
                        "width": 1,
                        "direction": "input",
                    },
                ],
            },
            {
                "name": "op_i",
                "descr": "Input port",
                "signals": [
                    {
                        "name": "op",
                        "width": "DATA_W",
                        "direction": "input",
                    },
                ],
            },
            {
                "name": "done_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "done",
                        "width": 1,
                        "direction": "output",
                    },
                ],
            },
            {
                "name": "res_o",
                "descr": "Output port",
                "signals": [
                    {
                        "name": "res",
                        "width": "SIZE_W",
                        "direction": "output",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "right",
                "descr": "right wire",
                "signals": [
                    {"name": "right", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "left",
                "descr": "left wire",
                "signals": [
                    {"name": "left", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "a_in",
                "descr": "a_in wire",
                "signals": [
                    {"name": "a_in", "width": "DATA_W"},
                ],
            },
            {
                "name": "tmp",
                "descr": "tmp wire",
                "signals": [
                    {"name": "tmp", "width": "SIZE_W+2"},
                ],
            },
            {
                "name": "q",
                "descr": "q wire",
                "signals": [
                    {"name": "q", "width": "SIZE_W"},
                ],
            },
            {
                "name": "counter",
                "descr": "counter wire",
                "signals": [
                    {"name": "counter", "width": "COUNT_W"},
                ],
            },
            {
                "name": "a",
                "descr": "a wire",
                "signals": [
                    {"name": "a", "width": "DATA_W"},
                ],
            },
            {
                "name": "r",
                "descr": "r wire",
                "signals": [
                    {"name": "r", "width": "SIZE_W+2"},
                ],
            },
        ],
        "snippets": [
            {
                "verilog_code": """
""",
            },
        ],
        "fsm": {
            "verilog_code": """
default_assignments:
        right = {q, r[SIZE_W+1], 1'b1};
        left = {r[SIZE_W-1:0], a[DATA_W-1 -: 2]};
        a_in = {a[DATA_W-3:0], 2'b00};
        tmp =  r[SIZE_W+1] ? left + right : left - right;
        res_o = q;
        done_o = ~pc;

        idle:
            if (start_i) begin
                a_nxt = op_i;
                q_nxt = 0;
                r_nxt = 0;
                counter_nxt = 0;
            end else begin
                pc_nxt = pc;
            end

            r_nxt = tmp;
            q_nxt = {q[SIZE_W-2:0], ~tmp[SIZE_W+1]};
            a_nxt = a_in;
            if (counter != END_COUNT[COUNT_W-1:0] - 1) begin
                counter_nxt = counter + 1'b1;
                pc_nxt = pc;
            end else begin
                pc_nxt = idle; end
""",
        }
    }
    return attributes_dict
