#!/usr/bin/env python3
import os
import sys
import shutil
import math

from iob_soc_opencryptolinux_create_periphs_tmp import (
    create_periphs_tmp,
    check_linux_build_macros,
)

from config_gen import append_str_config_build_mk

from iob_soc import iob_soc
from iob_vexriscv import iob_vexriscv
from iob_uart16550 import iob_uart16550
from iob_uart import iob_uart
from iob_spi_master import iob_spi_master
from iob_eth import iob_eth
from N25Qxxx import N25Qxxx
from axil2iob import axil2iob
from iob_reset_sync import iob_reset_sync
from iob_ram_sp import iob_ram_sp
from iob_versat import CreateVersatClass

DMA_DEMO = "OCL_DMA_DEMO" in sys.argv

# For DMA demo
if DMA_DEMO:
    from iob_axistream_in import iob_axistream_in
    from iob_axistream_out import iob_axistream_out
    from iob_dma import iob_dma
    from verilog_gen import insert_verilog_in_module


class iob_soc_opencryptolinux(iob_soc):
    name = "iob_soc_opencryptolinux"
    version = "V0.70"
    flows = "pc-emul emb sim doc fpga"
    setup_dir = os.path.dirname(__file__)

    @classmethod
    def _create_instances(cls):
        super()._create_instances()
        # Verilog modules instances if we have them in the setup list (they may not be in the list if a subclass decided to remove them).
        if iob_vexriscv in cls.submodule_list:
            cls.cpu = iob_vexriscv("cpu_0")
        # Instantiate OpenCryptoLinux peripherals
        if iob_uart16550 in cls.submodule_list:
            cls.peripherals.append(iob_uart16550("UART0", "Default UART interface"))
        if iob_spi_master in cls.submodule_list:
            cls.peripherals.append(iob_spi_master("SPI0", "SPI master peripheral"))
        # Instantiate versat
        if cls.versatType in cls.submodule_list:
            cls.versat = cls.versatType(
                "VERSAT0",
                "Versat accelerator",
                parameters={
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
            )
            cls.peripherals.append(cls.versat)

        if iob_eth in cls.submodule_list:
            cls.peripherals.append(
                iob_eth(
                    "ETH0",
                    "Ethernet interface",
                    parameters={
                        "AXI_ID_W": "AXI_ID_W",
                        "AXI_LEN_W": "AXI_LEN_W",
                        "AXI_ADDR_W": "AXI_ADDR_W",
                        "AXI_DATA_W": "AXI_DATA_W",
                        "MEM_ADDR_OFFSET": "MEM_ADDR_OFFSET",
                    },
                )
            )

        if DMA_DEMO:
            cls.peripherals.append(
                iob_axistream_in(
                    "AXISTREAMIN0",
                    "AXI stream input interface",
                    parameters={"TDATA_W": "32"},
                )
            )
            cls.peripherals.append(
                iob_axistream_out(
                    "AXISTREAMOUT0",
                    "AXI stream output interface",
                    parameters={"TDATA_W": "32"},
                )
            )
            cls.peripherals.append(
                iob_dma(
                    "DMA0",
                    "DMA interface",
                    parameters={
                        "AXI_ID_W": "AXI_ID_W",
                        "AXI_LEN_W": "AXI_LEN_W",
                        "AXI_ADDR_W": "AXI_ADDR_W",
                        "N_INPUTS": "1",
                        "N_OUTPUTS": "1",
                    },
                )
            )

        # Add custom N_SLAVES and N_SLAVES_W
        cls.confs += [
            {
                "name": "N_SLAVES",
                "type": "M",
                "val": str(
                    len(cls.peripherals) + 3
                ),  # + 3 for internal BOOT_CTR, PLIC and CLINT
                "min": "NA",
                "max": "NA",
                "descr": "Number of peripherals",
            },
            {
                "name": "N_SLAVES_W",
                "type": "M",
                "val": str(
                    math.ceil(
                        math.log(
                            len(cls.peripherals)
                            + 3,  # + 3 for internal BOOT_CTR, PLIC and CLINT
                            2,
                        )
                    )
                ),
                "min": "NA",
                "max": "NA",
                "descr": "Peripheral bus width",
            },
        ]

    @classmethod
    def _create_submodules_list(cls, extra_submodules=[]):
        """Create submodules list with dependencies of this module"""

        VERSAT_SPEC = f"{__class__.setup_dir}/software/versat/versatSpec.txt"
        VERSAT_EXTRA_UNITS = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "hardware/src/units")
        )

        cls.versatType = CreateVersatClass(
            False, VERSAT_SPEC, "CryptoAlgos", VERSAT_EXTRA_UNITS, cls.build_dir
        )

        if DMA_DEMO:
            extra_submodules += [
                iob_axistream_in,
                iob_axistream_out,
                iob_dma,
            ]

        super()._create_submodules_list(
            [
                {"interface": "peripheral_axi_wire"},
                {"interface": "intmem_axi_wire"},
                {"interface": "dBus_axi_wire"},
                {"interface": "iBus_axi_wire"},
                {"interface": "dBus_axi_m_port"},
                {"interface": "iBus_axi_m_port"},
                {"interface": "dBus_axi_m_portmap"},
                {"interface": "iBus_axi_m_portmap"},
                iob_vexriscv,
                iob_uart16550,
                axil2iob,
                iob_reset_sync,
                iob_ram_sp,
                cls.versatType,
                iob_eth,
                iob_spi_master,
                (N25Qxxx, {"purpose": "simulation"}),
                (iob_uart, {"purpose": "simulation"}),
            ]
            + extra_submodules
        )
        # Remove picorv32 and uart from iob-soc
        i = 0
        while i < len(cls.submodule_list):
            if type(cls.submodule_list[i]) == type and cls.submodule_list[i].name in [
                "iob_picorv32",
                "iob_uart",
                "iob_cache",
            ]:
                cls.submodule_list.pop(i)
                continue
            i += 1

    @classmethod
    def _post_setup(cls):
        dst = f"{cls.build_dir}/software/src"
        src = f"{__class__.setup_dir}/submodules/OS/software/OS_build"
        files = ["rootfs.cpio.gz", "Image"]
        for fname in files:
            src_file = os.path.join(src, fname)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst)

        super()._post_setup()

        # Copy scripts to scripts build directory
        iob_soc_scripts = [
            "terminalMode",
            "makehex",
            "hex_split",
            "hex_join",
            "board_client",
            "console",
            "console_ethernet",
        ]
        dst = f"{cls.build_dir}/scripts"
        for script in iob_soc_scripts:
            src_file = f"{__class__.setup_dir}/submodules/IOBSOC/scripts/{script}.py"
            shutil.copy2(src_file, dst)
        src_file = f"{__class__.setup_dir}/scripts/check_if_run_linux.py"
        shutil.copy2(src_file, dst)

        shutil.copy2(
            f"{__class__.setup_dir}/software/versat/module/versat.ko",
            f"{cls.build_dir}/software",
        )
        shutil.copy2(
            f"{__class__.setup_dir}/software/tests/exampleTransfer.sh",
            f"{cls.build_dir}/software",
        )
        shutil.copy2(
            f"{__class__.setup_dir}/software/tests/setupTest.sh",
            f"{cls.build_dir}/software",
        )
        shutil.copy2(
            f"{__class__.setup_dir}/software/tests/test.sh",
            f"{cls.build_dir}/software",
        )

        shutil.copytree(
            f"{__class__.setup_dir}/hardware/src/units",
            f"{cls.build_dir}/hardware/src",
            dirs_exist_ok=True,
        )

        # Override periphs_tmp.h of iob-soc with one specific for opencryptolinux
        create_periphs_tmp(
            cls.name,
            next(i["val"] for i in cls.confs if i["name"] == "ADDR_W"),
            cls.peripherals,
            f"{cls.build_dir}/software/{cls.name}_periphs.h",
        )
        check_linux_build_macros(cls, f"{__class__.setup_dir}/submodules/OS")

        if cls.is_top_module:
            # Set variables in fpga_build.mk
            with open(cls.build_dir + "/hardware/fpga/fpga_build.mk", "r") as file:
                contents = file.readlines()
            contents.append(
                "#Lines below were auto generated by iob_soc_opencryptolinux.py\n"
            )
            # Set custom ethernet CONSOLE_CMD
            contents.append(
                f"""
RUN_DEPS+=boot_flow
GRAB_TIMEOUT = 1200
### Launch minicom if running Linux
# pass CI variable over ssh commands
UFLAGS+=CI=$(CI)
UFLAGS+=BOOT_FLOW=$(BOOT_FLOW)
ifeq ($(shell grep -o rootfs.cpio.gz ../{cls.name}_mem.config),rootfs.cpio.gz)
ifneq ($(wildcard minicom_linux_script.txt),)
SCRIPT_STR:=-S minicom_linux_script.txt
# Set TERM variable to linux-c-nc (needed to run in non-interactive mode https://stackoverflow.com/a/49077622)
TERM_STR:=TERM=linux-c-nc
# Give fake stdout to minicom on CI (continuous integration), as it does not have any available (based on https://www.linuxquestions.org/questions/linux-general-1/capuring-data-with-minicom-over-tty-interface-4175558631/#post5448734)
# Run minicom process in background for Github Actions and wait for minicom to
# finish so that board_client does not finish as soon as minicom goes to
# background
# Github Actions sets CI="true" (https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables)
ifneq ($(CI),)
FAKE_STDOUT:=> minicom2.log
RUN_MINICOM_IN_BACKGROUND:= & wait $$!
else
FAKE_STDOUT:=
RUN_MINICOM_IN_BACKGROUND:=
endif
endif
# Set a capture file and print its contents (to work around minicom clearing the screen)
LOG_STR:=-C minicom_out.log $(FAKE_STDOUT) || cat minicom_out.log
# Set HOME to current (fpga) directory (needed because minicom always reads the '.minirc.*' config file from HOME)
HOME_STR:=HOME=$$(pwd)
# Always exit with code 0 (since linux is terminated with CTRL-C)
CONSOLE_CMD += && (($(HOME_STR) $(TERM_STR) minicom iobundle.dfl $(SCRIPT_STR) $(LOG_STR) || (exit 0)) $(RUN_MINICOM_IN_BACKGROUND) )
endif
            """
            )
            with open(cls.build_dir + "/hardware/fpga/fpga_build.mk", "w") as file:
                file.writelines(contents)

            # Set ETH_IF in sim_build.mk
            with open(cls.build_dir + "/hardware/simulation/sim_build.mk", "r") as file:
                contents = file.readlines()

            contents.insert(0, "\n")
            contents.insert(
                0,
                """
#Lines below were auto generated by iob_soc_opencryptolinux.py
ETH_IF ?= eth-$(SIMULATOR)
""",
            )
            with open(cls.build_dir + "/hardware/simulation/sim_build.mk", "w") as file:
                file.writelines(contents)

        if cls.is_top_module:
            # Set ethernet MAC address
            append_str_config_build_mk(
                f"""
### Set Ethernet environment variables
#Eth interface address of pc connected to ethernet peripheral (based on board name)
$(if $(findstring sim,$(MAKECMDGOALS))$(SIMULATOR),$(eval BOARD=))
ifeq ($(BOARD),AES-KU040-DB-G)
ETH_IF ?=eno1
endif
ifeq ($(BOARD),CYCLONEV-GT-DK)
ETH_IF ?= enp0s31f6
endif
# Set a MAC address for console (randomly generated)
RMAC_ADDR ?=88431eafa897
export RMAC_ADDR
#Set correct environment if running on IObundle machines
ifneq ($(filter feynman pudim-flan sericaia,$(shell hostname)),)
IOB_CONSOLE_PYTHON_ENV ?= /opt/pyeth3/bin/python
else
IOB_CONSOLE_PYTHON_ENV ?= {__class__.setup_dir}/submodules/ETHERNET/scripts/pyRawWrapper/pyRawWrapper
endif
                    """,
                cls.build_dir,
            )

        if DMA_DEMO:
            # Connect General signals from iob-axis cores
            insert_verilog_in_module(
                """
        assign AXISTREAMIN0_axis_clk_i = clk_i;
        assign AXISTREAMIN0_axis_cke_i = cke_i;
        assign AXISTREAMIN0_axis_arst_i = arst_i;
        assign AXISTREAMOUT0_axis_clk_i = clk_i;
        assign AXISTREAMOUT0_axis_cke_i = cke_i;
        assign AXISTREAMOUT0_axis_arst_i = arst_i;
                 """,
                cls.build_dir + f"/hardware/src/{cls.name}.v",
            )

    @classmethod
    def _setup_confs(cls, extra_confs=[]):
        if DMA_DEMO:
            extra_confs += [
                {
                    "name": "DMA_DEMO",
                    "type": "M",
                    "val": True,
                    "min": "0",
                    "max": "1",
                    "descr": "Enable DMA demo",
                },
            ]
        # Append confs or override them if they exist
        super()._setup_confs(
            [
                {
                    "name": "INIT_MEM",
                    "type": "M",
                    "val": False,
                    "min": "0",
                    "max": "1",
                    "descr": "Used to select running linux.",
                },
                {
                    "name": "USE_EXTMEM",
                    "type": "M",
                    "val": True,
                    "min": "0",
                    "max": "1",
                    "descr": "Always use external memory in the SoC.",
                },
                {
                    "name": "N_CORES",
                    "type": "P",
                    "val": "1",
                    "min": "1",
                    "max": "32",
                    "descr": "Number of CPU cores used in the SoC.",
                },
                {
                    "name": "BOOTROM_ADDR_W",
                    "type": "P",
                    "val": "15",
                    "min": "1",
                    "max": "32",
                    "descr": "Boot ROM address width",
                },
                {
                    "name": "MEM_ADDR_W",
                    "type": "P",
                    "val": "26",
                    "min": "1",
                    "max": "32",
                    "descr": "Memory bus address width",
                },
                {
                    "name": "OS_ADDR_W",
                    "type": "M",
                    "val": "25",
                    "min": "1",
                    "max": "32",
                    "descr": "Memory bus address width",
                },
                # INTERRUPTS ARCHITECTURE
                {
                    "name": "N_SOURCES",
                    "type": "P",
                    "val": "32",
                    "min": "1",
                    "max": "32",
                    "descr": "Number of peripherals that can generate an external interrupt to be interpreted by the PLIC.",
                },
                {
                    "name": "N_TARGETS",
                    "type": "P",
                    "val": "2",
                    "min": "1",
                    "max": "32",
                    "descr": "Number of HARTs in the SoC.",
                },
                {
                    "name": "USE_ETHERNET",
                    "type": "M",
                    "val": True,
                    "min": "0",
                    "max": "1",
                    "descr": "Enable ethernet support.",
                },
            ]
            + extra_confs
        )

        # Remove unnecessary confs of IOb-SoC
        i = 0
        while i < len(cls.confs):
            if cls.confs[i]["name"] in ["USE_MUL_DIV", "USE_COMPRESSED"]:
                cls.confs.pop(i)
                continue
            i += 1

    # Method that runs the setup process of this class
    @classmethod
    def _setup_portmap(cls):
        if iob_uart16550 in cls.submodule_list:
            cls.peripheral_portmap += [
                # Map interrupt port to internal wire
                (
                    {
                        "corename": "UART0",
                        "if_name": "interrupt",
                        "port": "interrupt_o",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "uart", "port": "", "bits": []},
                ),
                # Map other rs232 ports to external interface (system IO)
                (
                    {
                        "corename": "UART0",
                        "if_name": "rs232",
                        "port": "txd_o",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "uart", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "UART0",
                        "if_name": "rs232",
                        "port": "rxd_i",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "uart", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "UART0",
                        "if_name": "rs232",
                        "port": "cts_i",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "uart", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "UART0",
                        "if_name": "rs232",
                        "port": "rts_o",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "uart", "port": "", "bits": []},
                ),
            ]
        if iob_eth in cls.submodule_list:
            cls.peripheral_portmap += [
                # ETHERNET
                (
                    {
                        "corename": "ETH0",
                        "if_name": "general",
                        "port": "inta_o",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                # phy - connect to external interface
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MTxClk",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MTxD",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MTxEn",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MTxErr",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MRxClk",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MRxDv",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MRxD",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MRxErr",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MColl",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MCrS",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MDC",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "MDIO",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "ETH0",
                        "if_name": "phy",
                        "port": "phy_rstn_o",
                        "bits": [],
                    },
                    {
                        "corename": "external",
                        "if_name": "ETH0",
                        "port": "",
                        "bits": [],
                    },
                ),
            ]
        if iob_spi_master in cls.submodule_list:
            cls.peripheral_portmap += [
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "avalid_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "address_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "wdata_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "wstrb_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "rdata_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "rvalid_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "iob_s_cache",
                        "port": "ready_cache",
                        "bits": [],
                    },
                    {"corename": "internal", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "SS",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "SCLK",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "MISO",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "MOSI",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "WP_N",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
                (
                    {
                        "corename": "SPI0",
                        "if_name": "flash_if",
                        "port": "HOLD_N",
                        "bits": [],
                    },
                    {"corename": "external", "if_name": "spi", "port": "", "bits": []},
                ),
            ]

        if DMA_DEMO:
            cls.peripheral_portmap += [
                # AXISTREAM IN - General signals
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_clk_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMIN0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_cke_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMIN0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_arst_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMIN0",
                        "port": "",
                        "bits": [],
                    },
                ),
                # AXISTREAM OUT - General signals
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_clk_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMOUT0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_cke_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMOUT0",
                        "port": "",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_arst_i",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMOUT0",
                        "port": "",
                        "bits": [],
                    },
                ),
                # AXISTREAM IN DMA
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "sys_axis",
                        "port": "sys_tvalid_o",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_input",
                        "port": "tvalid_i",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "sys_axis",
                        "port": "sys_tready_i",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_input",
                        "port": "tready_o",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "sys_axis",
                        "port": "sys_tdata_o",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_input",
                        "port": "tdata_i",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "general",
                        "port": "interrupt_o",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMIN0",
                        "port": "",
                        "bits": [],
                    },
                ),
                # AXISTREAM OUT DMA
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "sys_axis",
                        "port": "sys_tvalid_i",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_output",
                        "port": "tvalid_o",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "sys_axis",
                        "port": "sys_tready_o",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_output",
                        "port": "tready_i",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "sys_axis",
                        "port": "sys_tdata_i",
                        "bits": [],
                    },
                    {
                        "corename": "DMA0",
                        "if_name": "dma_output",
                        "port": "tdata_o",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "general",
                        "port": "interrupt_o",
                        "bits": [],
                    },
                    {
                        "corename": "internal",
                        "if_name": "AXISTREAMOUT0",
                        "port": "",
                        "bits": [],
                    },
                ),
                # Connect AXISTREAM IN to AXISTREAM OUT
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_tvalid_i",
                        "bits": [],
                    },
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_tvalid_o",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_tready_o",
                        "bits": [],
                    },
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_tready_i",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_tdata_i",
                        "bits": [],
                    },
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_tdata_o",
                        "bits": [],
                    },
                ),
                (
                    {
                        "corename": "AXISTREAMIN0",
                        "if_name": "axistream",
                        "port": "axis_tlast_i",
                        "bits": [],
                    },
                    {
                        "corename": "AXISTREAMOUT0",
                        "if_name": "axistream",
                        "port": "axis_tlast_o",
                        "bits": [],
                    },
                ),
            ]
