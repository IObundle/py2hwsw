ETHERNET_DIR:=../../../../..

include $(ETHERNET_DIR)/hardware/hardware.mk

all: iob_eth-iob_eth.qxp

iob_eth-iob_eth.qxp: rmac $(VSRC) $(VHDR)
	quartus_map --read_settings_files=on --write_settings_files=off iob_eth -c iob_eth --verilog_macro=$(RMAC_DEFINE)
	quartus_cdb --read_settings_files=off --write_settings_files=off iob_eth -c iob_eth --merge=on
	quartus_cdb iob_eth -c iob_eth --incremental_compilation_export=iob_eth.qxp --incremental_compilation_export_partition_name=Top --incremental_compilation_export_post_synth=on --incremental_compilation_export_post_fit=off --incremental_compilation_export_routing=on --incremental_compilation_export_flatten=on

rmac:
	$(eval RMAC = $(shell ethtool -P $(RMAC_INTERFACE) | awk '{print $$3}' | sed "s/://g"))
	$(eval PREFACE = "-DETH_RMAC_ADDR=48")
	$(eval RMAC_DEFINE = $(PREFACE)\'$(RMAC))

clean: 
	quartus_sh --clean iob_eth
	@rm -f *.qarlog *.qws *.qxp *~
	@rm -rf db incremental_db output_files

.PHONY: all clean
