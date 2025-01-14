ETHERNET_DIR:=../../..

defmacro:=-D
incdir:=-I

include ../simulation.mk

#icarus verilog simulator
VLOG:=iverilog -W all -g2005-sv

run: a.out
	./$< $(TEST_LOG)
ifeq ($(VCD),1)
	if [ "`pgrep -u $(USER) gtkwave`" ]; then killall -q -9 gtkwave; fi
	gtkwave -a waves.gtkw iob_eth.vcd &
endif

a.out: $(VSRC) $(VHDR)
	$(VLOG) $(INCLUDE) $(DEFINE) $(VSRC)

clean: ethernet-sim-clean
	@rm -f a.out

.phony: all clean
