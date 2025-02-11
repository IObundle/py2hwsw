#compile verilog

all: build

a.out: iob_v_tb.v
	iverilog -g2005-sv iob_v_tb.v

#compile C
tb: iob_c_tb.c iob_core_tb.c
	gcc -o $@ $^


build: a.out tb

run: build
	./tb
	./a.out
