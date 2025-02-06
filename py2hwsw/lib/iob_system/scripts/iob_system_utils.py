# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import os

#
# Functions for iob_system.py
#


def update_params(params, py_params):
    """Update given `params` dictionary with values from `py_params` dictionary.
    Paramters will be updated to have the same type as the default value.
    :param dict params: dictionary to update. Contains default values and their types.
    :param dict py_params: dictionary to use as source. Contains new values.
                           Their types will be converted to match the corresponding default type.
    """
    for name, default_val in params.items():
        if name not in py_params:
            continue
        if type(default_val) is bool and py_params[name] == "0":
            params[name] = False
        else:
            params[name] = type(default_val)(py_params[name])


def iob_system_scripts(attributes_dict, params, py_params):
    """IOb-SoC automatic setup scripts.
    :param dict attributes_dict: iob_system attributes
    :param dict params: iob_system python parameters
    :param dict py_params: iob_system argument python parameters
    """
    assert_block_attributes(attributes_dict, py_params)
    handle_system_overrides(attributes_dict, py_params)
    append_board_wrappers(attributes_dict, params)
    set_build_dir(attributes_dict, py_params)
    peripherals = get_iob_system_peripherals_list(attributes_dict)
    connect_peripherals_cbus(attributes_dict, peripherals, params)
    generate_memory_map(attributes_dict, peripherals, params, py_params)
    generate_makefile_segments(attributes_dict, peripherals, params, py_params)


#
# Local functions
#


def assert_block_attributes(attributes_dict, py_params):
    """Assert that all block attributes are valid."""
    child_attributes = py_params.get("system_attributes", {})
    for attribute in ["subblocks", "superblocks"]:
        for block in attributes_dict.get(attribute, []) + child_attributes.get(
            attribute, []
        ):
            assert block.get("core_name", None), "All subblocks must have a core name!"
            assert block.get(
                "instance_name", None
            ), f"Block '{block['core_name']}' must have an instance name!"


def append_board_wrappers(attributes_dict, params):
    """Append board wrappers to superblocks list based on boards_list.
    :param dict attributes_dict: iob_system attributes
    :param dict params: iob_system python parameters
    """
    # FIXME: We should have a way for child cores to specify their board's tool (assuming child cores may add new unknown boards)

    # Find memory wrapper dictionary
    mwrap_dict = None
    for block in attributes_dict["superblocks"]:
        if block["instance_name"] == "iob_system_mwrap":
            mwrap_dict = block
            break

    tools = {
        "aes_ku040_db_g": "vivado",
        "cyclonev_gt_dk": "quartus",
        "zybo_z7": "vivado",
        "basys3": "vivado",
    }
    for board in attributes_dict.get("board_list", []):
        tool = tools[board]
        mwrap_dict["superblocks"].append(
            {
                "core_name": "iob_system_" + board,
                "instance_name": "iob_system_" + board,
                "instance_description": f"FPGA wrapper for {board}",
                "dest_dir": f"hardware/fpga/{tool}/{board}",
                "iob_system_params": params,
            },
        )


def handle_system_overrides(attributes_dict, py_params):
    """Override/append attributes given in `system_attributes` python parameter (usually by child core).
    :param dict attributes_dict: iob_system attributes
    :param dict py_params: Dictionary containing `system_attributes` python parameter
    """
    child_attributes = py_params.get("system_attributes")
    if not child_attributes:
        return

    for child_attribute_name, child_value in child_attributes.items():
        # Don't override child-specific attributes
        if child_attribute_name in ["original_name", "setup_dir", "parent"]:
            continue

        # Override other attributes of type string and bool
        if type(child_value) is str or type(child_value) is bool:
            attributes_dict[child_attribute_name] = child_value
            continue

        # Override or append elements from list attributes
        assert (
            type(child_value) is list
        ), f"Invalid type for attribute '{child_attribute_name}': {type(child_value)}"

        # Select identifier attribute. Used to compare if should override each element.
        identifier = "name"
        if child_attribute_name in ["subblocks", "superblocks", "sw_modules"]:
            identifier = "instance_name"
        elif child_attribute_name in ["board_list", "snippets", "ignore_snippets"]:
            # Elements in list do not have identifier, so just append them to parent list
            for child_obj in child_value:
                attributes_dict[child_attribute_name].append(child_obj)
            continue

        # Process each object from list
        for child_obj in child_value:
            # Find object and override it
            for idx, obj in enumerate(attributes_dict[child_attribute_name]):
                if obj[identifier] == child_obj[identifier]:
                    # print(f"DEBUG: Overriding {child_obj[identifier]}", file=sys.stderr)
                    attributes_dict[child_attribute_name][idx] = child_obj
                    break
            else:
                # Didn't override, so append it to list
                attributes_dict[child_attribute_name].append(child_obj)


def set_build_dir(attributes_dict, py_params):
    """If build_dir not given in py_params, set a default one.
    :param dict attributes_dict: iob_system attributes
    :param dict py_params: iob_system argument python parameters
    """
    if "build_dir" in py_params and py_params["build_dir"]:
        build_dir = py_params["build_dir"]
    else:
        build_dir = f"../{attributes_dict['name']}_V{attributes_dict['version']}"

    # If this system is a tester, set build dir based on dest_dir
    if attributes_dict.get("is_tester", False):
        build_dir = os.path.join(
            build_dir, py_params.get("dest_dir", "submodules/tester")
        )

    attributes_dict["build_dir"] = build_dir


def get_iob_system_peripherals_list(attributes_dict):
    """Parses subblocks list in iob_system attributes, for subblocks with the `is_peripheral` attribute set.
    Also removes `is_peripheral` attribute from each block after adding it to the peripherals list.
    """
    peripherals = []
    for block in attributes_dict["subblocks"]:
        if block.pop("is_peripheral", False):
            peripherals.append(block)
    return peripherals


def connect_peripherals_cbus(attributes_dict, peripherals, params):
    """Update given attributes_dict to connect peripherals cbus to system's pbus_split.
    :param dict attributes_dict: iob_system attributes
    :param list peripherals: list of peripheral subblocks
    :param dict params: iob_system python parameters
    """
    # Find pbus_split
    pbus_split = None
    for block in attributes_dict["subblocks"]:
        if block["instance_name"] == "iob_pbus_split":
            pbus_split = block

    # Number of peripherals = peripherals + CLINT + PLIC
    num_peripherals = len(peripherals) + 2
    peripheral_addr_w = params["addr_w"] - 2 - (num_peripherals - 1).bit_length()

    # Configure number of connections to pbus_split
    pbus_split["num_outputs"] = num_peripherals

    for idx, peripheral in enumerate(peripherals):
        peripheral_name = peripheral["instance_name"].lower()
        # Add peripheral cbus wire
        attributes_dict["wires"].append(
            {
                "name": f"{peripheral_name}_cbus",
                "descr": f"{peripheral_name} Control/Status Registers bus",
                "signals": {
                    "type": "iob",
                    "prefix": f"{peripheral_name}_cbus_",
                    "ADDR_W": peripheral_addr_w - 2,
                },
            },
        )
        # Connect cbus to pbus_split
        pbus_split["connect"][f"output_{idx}_m"] = f"{peripheral_name}_cbus"
        # Connect cbus to peripheral
        peripheral["connect"][
            f"{peripheral['core_name']}_csrs_cbus_s"
        ] = f"{peripheral_name}_cbus"

    # Add CLINT and PLIC wires (they are not in peripherals list)
    attributes_dict["wires"] += [
        {
            "name": "clint_cbus",
            "descr": "CLINT Control/Status Registers bus",
            "signals": {
                "type": "iob",
                "prefix": "clint_cbus_",
                "ADDR_W": peripheral_addr_w - 2,
            },
        },
        {
            "name": "plic_cbus",
            "descr": "PLIC Control/Status Registers bus",
            "signals": {
                "type": "iob",
                "prefix": "plic_cbus_",
                "ADDR_W": peripheral_addr_w - 2,
            },
        },
    ]

    # Connect CLINT and PLIC cbus to last outputs of pbus_split
    pbus_split["connect"][f"output_{num_peripherals-2}_m"] = "clint_cbus"
    pbus_split["connect"][f"output_{num_peripherals-1}_m"] = "plic_cbus"


def generate_memory_map(attributes_dict, peripherals_list, params, py_params):
    """Create C header file containing system memory map.
    :param dict attributes_dict: iob_system attributes
    :param list peripherals_list: list of peripheral subblocks
    :param dict params: iob_system python parameters
    :param dict py_params: iob_system argument python parameters
    """

    # Don't create files for other targets (like clean)
    if "py2hwsw_target" not in py_params or py_params["py2hwsw_target"] != "setup":
        return

    memory_map = {}

    num_memory_regions = 0
    memory_region_enable_parameters = [
        "use_intmem",
        "use_extmem",
        "use_bootrom",
        "use_peripherals",
    ]
    for param_name in memory_region_enable_parameters:
        if params[param_name]:
            region_name = param_name[4:]
            memory_map[region_name] = num_memory_regions
            num_memory_regions += 1
    num_sel_bits = (num_memory_regions - 1).bit_length()
    assert num_memory_regions, "No memory regions defined"
    region_width = params["addr_w"] - num_sel_bits
    print("------------------------------------------------------")
    print(f"Memory map for {attributes_dict['name']} (iob_system):")
    for region_name in memory_map.keys():
        memory_map[region_name] = memory_map[region_name] << (
            params["addr_w"] - num_sel_bits
        )
        region_size = 1 << region_width
        print(
            f"[{memory_map[region_name]:#0{2+(params['addr_w']>>2)}x}-{memory_map[region_name]+region_size-1:#0{2+(params['addr_w']>>2)}x}]: {region_name} ({region_width} bits)"
        )
    print("------------------------------------------------------")

    if params["use_peripherals"]:
        memory_map |= generate_peripheral_base_addresses(
            attributes_dict,
            peripherals_list,
            params,
            py_params,
            memory_map["peripherals"],
            region_width,
        )

    out_file = os.path.join(
        attributes_dict["build_dir"], "software", f"{attributes_dict['name']}_mmap.h"
    )

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w") as f:
        for region_name, base_address in memory_map.items():
            f.write(f"#define {region_name.upper()}_BASE {hex(base_address)}\n")
    print(f"See '{out_file}' for complete list of memory regions.")

    # Find CPU subblock
    cpu_subblock = None
    for subblock in attributes_dict["subblocks"]:
        if subblock["instance_name"] == "cpu":
            cpu_subblock = subblock
            break
    # Update reset address and uncached region passed via python parameters to the CPU
    bootrom_addr = memory_map.get("bootrom", None)
    if bootrom_addr is not None:
        cpu_subblock["reset_addr"] = bootrom_addr
    peripherals_addr = memory_map.get("peripherals", None)
    if peripherals_addr is not None:
        cpu_subblock["uncached_start_addr"] = peripherals_addr
        cpu_subblock["uncached_size"] = 2**region_width


def generate_peripheral_base_addresses(
    attributes_dict, peripherals_list, params, py_params, pbus_base, region_width
):
    """Create C header file containing peripheral base addresses.
    :param dict attributes_dict: iob_system attributes
    :param list peripherals_list: list of peripheral subblocks
    :param dict params: iob_system python parameters
    :param dict py_params: iob_system argument python parameters
    :param int region_width: width of the peripheral region
    :returns dict: peripheral base addresses. Format: {peripheral_name: address}
    """

    # Include CLINT and PLIC in peripherals list
    complete_peripherals_list = peripherals_list + [
        {"instance_name": "CLINT0"},
        {"instance_name": "PLIC0"},
    ]
    n_slaves_w = (len(complete_peripherals_list) - 1).bit_length()

    peripherals_base_addresses = {}
    for idx, instance in enumerate(complete_peripherals_list):
        instance_name = instance["instance_name"]
        peripherals_base_addresses[instance_name] = pbus_base + (
            idx << (region_width - n_slaves_w)
        )
    return peripherals_base_addresses


def generate_makefile_segments(attributes_dict, peripherals, params, py_params):
    """Generate automatic makefile segments for iob_system.
    :param dict attributes_dict: iob_system attributes
    :param list peripherals: list of peripheral subblocks
    :param dict params: iob_system python parameters
    :param dict py_params: iob_system argument python parameters
    """
    name = attributes_dict["name"]
    build_dir = attributes_dict["build_dir"]

    # Don't create files for other targets (like clean)
    if "py2hwsw_target" not in py_params or py_params["py2hwsw_target"] != "setup":
        return

    #
    # Create auto_sw_build.mk
    #
    os.makedirs(f"{build_dir}/software", exist_ok=True)
    with open(f"{build_dir}/software/auto_sw_build.mk", "w") as file:
        file.write("#This file was auto generated by iob_system_utils.py\n")
        # Create a list with every unique peripheral name, except clint, and plic
        peripheral_name_list = []
        for peripheral in peripherals:
            if peripheral["core_name"] not in peripheral_name_list:
                peripheral_name_list.append(peripheral["core_name"])
        if peripherals:
            file.write("PERIPHERALS ?=" + " ".join(peripheral_name_list) + "\n")
        if params["use_ethernet"]:
            # Set custom ethernet CONSOLE_CMD
            file.write(
                'CONSOLE_CMD ?=rm -f soc2cnsl cnsl2soc; $(IOB_CONSOLE_PYTHON_ENV) $(PYTHON_DIR)/console_ethernet.py -L -c $(PYTHON_DIR)/console.py -m "$(RMAC_ADDR)" -i "$(ETH_IF)"\n',
            )
            file.write(
                """
UTARGETS+=iob_eth_rmac.h
EMUL_HDR+=iob_eth_rmac.h
iob_eth_rmac.h:
	echo "#define ETH_RMAC_ADDR 0x$(RMAC_ADDR)" > $@\n
""",
            )
        if attributes_dict.get("is_tester", False):
            # Create target to build UUT's software
            file.write(
                """
# Tester target to build UUT's software
# Build UUT software with "TESTER" macro defined
UTARGETS+=build_uut_software
build_uut_software:
	make -C $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/software clean
	cp $(ROOT_DIR)/software/src/iob_bsp.h $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/software/src/
	USER_CFLAGS=-DTESTER make -C $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/software build

.PHONY: build_uut_software
"""
            )

    #
    # Create auto_fpga_build.mk
    #
    os.makedirs(f"{build_dir}/hardware/fpga", exist_ok=True)
    with open(f"{build_dir}/hardware/fpga/auto_fpga_build.mk", "w") as file:
        file.write("#This file was auto generated by iob_system_utils.py\n")

        # Set USE_EXTMEM variable
        file.write(f"USE_EXTMEM:={int(params['use_extmem'])}\n")
        # Set INIT_MEM variable
        file.write(f"INIT_MEM:={int(params['init_mem'])}\n")
        if params["use_ethernet"]:
            # Set custom ethernet CONSOLE_CMD
            file.write(
                'CONSOLE_CMD=$(IOB_CONSOLE_PYTHON_ENV) $(PYTHON_DIR)/console_ethernet.py -s $(BOARD_SERIAL_PORT) -c $(PYTHON_DIR)/console.py -m "$(RMAC_ADDR)" -i "$(ETH_IF)"\n',
            )
        if attributes_dict.get("is_tester", False):
            # Create target to copy UUT's hex files
            file.write(
                """
# Tester targets to build and get UUT's hex files
RUN_DEPS+=get_uut_run_deps
BUILD_DEPS+=get_uut_build_deps

get_uut_build_deps:
	make -C $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/fpga build_deps
	cp $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/fpga/*.hex .

get_uut_run_deps:
	make -C $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/fpga run_deps
	cp $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/fpga/*.hex .

.PHONY: get_uut_build_deps get_uut_run_deps
"""
            )

    #
    # Create auto_sim_build.mk
    #
    os.makedirs(f"{build_dir}/hardware/simulation", exist_ok=True)
    with open(f"{build_dir}/hardware/simulation/auto_sim_build.mk", "w") as file:
        file.write("#This file was auto generated by iob_system_utils.py\n")
        if params["use_ethernet"]:
            file.write("ETH_IF ?= eth-$(SIMULATOR)\n")
            file.write("USE_ETHERNET=1\n")
            # Set custom ethernet CONSOLE_CMD
            file.write(
                'ETH2FILE_SCRIPT="$(PYTHON_DIR)/eth2file.py"\n'
                'CONSOLE_CMD=$(IOB_CONSOLE_PYTHON_ENV) $(PYTHON_DIR)/console_ethernet.py -L -c $(PYTHON_DIR)/console.py -e $(ETH2FILE_SCRIPT) -m "$(RMAC_ADDR)" -i "$(ETH_IF)" -t 60\n',
            )
        if attributes_dict.get("is_tester", False):
            # Create target to copy UUT's hex files
            file.write(
                """
# Tester target to build and get UUT's hex files
HEX+=get_uut_hex

get_uut_hex:
	make -C $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/simulation build_hex
	cp $(ROOT_DIR)/$(RELATIVE_PATH_TO_UUT)/hardware/simulation/*.hex .

.PHONY: get_uut_hex
"""
            )

    #
    # Create auto_iob_system_boot.lds and auto_iob_system_firmware.lds
    #
    os.makedirs(f"{build_dir}/software", exist_ok=True)
    with open(f"{build_dir}/software/auto_{name}_boot.lds", "w") as file:
        file.write("/* This file was auto generated by iob_system_utils.py */\n")
        file.write(
            f". = {hex((1 << params['fw_addr_w']) - (1 << params['bootrom_addr_w']))};\n"
        )
    with open(f"{build_dir}/software/auto_{name}_firmware.lds", "w") as file:
        file.write("/* This file was auto generated by iob_system_utils.py */\n")
        file.write(f". = {params['fw_addr']};\n")
