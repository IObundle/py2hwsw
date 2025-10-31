//These macros may be dependent on instance parameters
//address macros
//addresses
`define IOB_BOOTROM_CSRS_ROM_ADDR 0
`define IOB_BOOTROM_CSRS_ROM_ADDR_W 12
`define IOB_BOOTROM_CSRS_ROM_W ((DATA_W > 1) ? DATA_W : 1)

`define IOB_BOOTROM_CSRS_VERSION_ADDR 4096
`define IOB_BOOTROM_CSRS_VERSION_W 16

