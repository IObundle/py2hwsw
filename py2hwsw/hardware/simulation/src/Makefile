#compile verilog

all: build

a.out: iob_v_tb.v
	iverilog -g2005-sv iob_v_tb.v

#compile C
tb: iob_c_tb.c iob_core_tb.c
	gcc -g -o $@ $^


build: a.out tb

run: build
	./a.out &
	./tb && killall -9 a.out

clean:
	rm -f a.out tb *.txt
