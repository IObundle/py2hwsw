def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_int_sqrt",
        "name": "iob_int_sqrt",
        "version": "0.1",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width",
            },
            {
                "name": "FRACTIONAL_W",
                "type": "P",
                "val": 0,
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "REAL_W",
                "type": "P",
                "val": "DATA_W - FRACTIONAL_W",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "SIZE_W",
                "type": "P",
                "val": "(REAL_W / 2) + FRACTIONAL_W",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "END_COUNT",
                "type": "F",
                "val": "(DATA_W + FRACTIONAL_W) >> 1",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
            {
                "name": "COUNT_W",
                "type": "F",
                "val": "$clog2(END_COUNT)",
                "min": "NA",
                "max": "NA",
                "descr": "Reset value.",
            },
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
        assign right = {q, r[SIZE_W+1], 1'b1};
        assign left = {r[SIZE_W-1:0], a[DATA_W-1 -: 2]};
        assign a_in = {a[DATA_W-3:0], 2'b00};
        assign tmp =  r[SIZE_W+1] ? left + right : left - right;
        assign res_o = q;
        assign done_o = ~pc;
""",
            },
        ],
        "fsm": {
            "verilog_code": """
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
