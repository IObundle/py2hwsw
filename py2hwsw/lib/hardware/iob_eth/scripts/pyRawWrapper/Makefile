
all: compile set-capabilities

compile:
	gcc -Wall pyRawWrapper.c -o pyRawWrapper -lcap
	chmod 750 pyRawWrapper

set-capabilities:
	@echo "Setting CAP_NET_RAW capability..."
	su root -c "setcap cap_net_raw,cap_setpcap=p pyRawWrapper"

.PHONY: all compile set-capabilities
