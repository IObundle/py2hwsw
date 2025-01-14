ETHERNET_DIR:=../../..

defmacro:=-define 
incdir:=-incdir 

include ../simulation.mk

CFLAGS = -errormax 15 $(INCLUDE) -status -update -linedebug -sv -define ETH_SIZE=20 -define VCD
EFLAGS = -errormax 15 -access +wc -status
SFLAGS = -errormax 15 -status

all: $(VSRC) $(VHDR)
	VSRC="$(VSRC)" CFLAGS="$(CFLAGS)" EFLAGS="$(EFLAGS)" SFLAGS="$(SFLAGS)" ./setup.sh

clean:
	@rm -f *#
	@rm -f xtop.tcf
	@rm -f ncsim.key
	@rm -f *.log
	@rm -f *~ 
	@rm -rf INCA_libs
	@rm -f *.vcd
	@rm -rf xcelium.d

.phony: all clean
