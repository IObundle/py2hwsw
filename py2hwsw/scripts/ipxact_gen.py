#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# TODO: account for log2n_items in the memory map
import math
import re
import os
import sys
from iob_wire import iob_wire
from api_base import convert2internal

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib/hardware/iob_csrs")
)
from iob_csrs import static_reg_tables

#
# Generates IP-XACT for the given core
#


def find_suffix_from_list(full_string, list_of_suffix_strings):
    """
    Given a string and a list of possible suffixes, check if string given has a suffix from the list
    Returns a tuple:
        -(prefix, suffix): 'prefix' is the full_string with the suffix removed.
            'suffix' is the string from the list that is a suffix of the full_string.
        -(None, None): if no suffix is found
    """
    return next(
        (
            (full_string[: -len(i)], i)
            for i in list_of_suffix_strings
            if full_string.endswith(i)
        ),
        (None, None),
    )


def replace_params_with_ids(string, parameters_list, double_usage_count=False):
    """
    Replace the parameters in the string with their ID
    @param string: hardware size
    @param parameters_list: list of parameters objects
    return: string with the parameters replaced with their ID
    """

    xml_output = string
    # Search for parameters in the hw_size and replace them with their ID
    if isinstance(string, str):
        # divide the string expression into a list of strings separated by operators, parenthesis or spaces
        string_list = re.split(r"(\+|\-|\*|\/|\(|\)|\s)", string)
        for value in string_list:
            for param in parameters_list:
                # if the parameter is in the string, increment it's usage count for each time it's used
                if value == param.name:
                    if double_usage_count:
                        param.usage_count += 2 * string.count(param.name)
                    else:
                        param.usage_count += string.count(param.name)
                    # replace the parameter with it's ID
                    xml_output = xml_output.replace(param.name, param.name + "_ID")
                    continue

    return xml_output


def escape_xml_special_chars(string):
    """
    Replace special XML characters with their XML escaped version
    """
    if type(string) is not str:
        return string
    return (
        string.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Parameter:
    """
    Parameter class


    """

    def __init__(self, name, kind, def_value, min_value, max_value, description):
        self.name = name
        self.kind = kind
        self.def_value = def_value
        self.min_value = min_value
        self.max_value = max_value
        self.usage_count = 0
        self.description = description

    def gen_xml(self, parameters_list):
        """
        Generate the xml code for the parameter
        @param self: parameter object
        @param parameters_list: list of parameters objects
        return: xml code
        """

        # if the parameter is a string, it has params, change them to their ID
        def_value = replace_params_with_ids(self.def_value, parameters_list)
        def_value = escape_xml_special_chars(def_value)

        # Try to convert def_value to int
        if type(def_value) is str and def_value.isnumeric():
            def_value = int(def_value)

        param_val_type = "int"
        if type(def_value) is not int:
            param_val_type = "string"

        # Generate the xml code
        xml_code = f"""<ipxact:parameter kactus2:usageCount="{self.usage_count}" """
        if self.max_value != "NA":
            xml_code += f"""maximum="{self.max_value}" """
        if self.min_value != "NA":
            xml_code += f"""minimum="{self.min_value}" """
        xml_code += f"""parameterId="{self.name}_ID" type="{param_val_type}">
			<ipxact:name>{self.name}</ipxact:name>
			<ipxact:description>{self.description}</ipxact:description>
			<ipxact:value>{def_value}</ipxact:value>
		</ipxact:parameter>"""

        return xml_code


class SwRegister:
    """
    Software register class


    """

    def __init__(
        self,
        name,
        address,
        hw_size,
        access,
        rst,
        rst_val,
        volatile,
        description,
        parameters_list,
        fields,
    ):
        self.name = name
        self.address = address

        if type(hw_size) is str and hw_size.isnumeric():
            hw_size = int(hw_size)

        self.hw_size = hw_size

        max_size = hw_size
        # if the max_size is a string, it has params, retrieve it's maximum value
        if isinstance(max_size, str):
            # transform the string into a mathemathical expression and retrieve the maximum value
            max_size = max_size.replace(" ", "")
            while True:
                for param in parameters_list:
                    # only replace complete words
                    max_size = re.sub(
                        r"\b" + param.name + r"\b", str(param.max_value), max_size
                    )

                # if the string only contains numbers or operators, evaluate it and break the loop
                if re.match(r"^[0-9\+\-\*\/\(\)]+$", max_size):
                    max_size = eval(max_size)
                    break

        # Compute the size of the register in steps of 8 bits, rounding up
        sw_size = 8 * math.ceil(max_size / 8)
        # If the size is 24 bits, set it to 32 bits
        if sw_size == 24:
            sw_size = 32
        self.sw_size = sw_size

        self.access = access
        self.rst = rst
        self.rst_val = rst_val
        self.volatile = volatile
        self.description = description
        self.fields = fields

    def gen_xml(self):
        """
        Generate the xml code for the software register
        @param self: software register object
        return: xml code
        """

        # set the access type
        if self.access == "R":
            access_type = "read-only"
        elif self.access == "W":
            access_type = "write-only"
        else:
            access_type = "read-write"

        fields_xml = ""
        for csr_field in self.fields:
            # set the access type
            if csr_field.mode == "R":
                field_access_type = "read-only"
            elif csr_field.mode == "W":
                field_access_type = "write-only"
            else:
                field_access_type = "read-write"
            fields_xml += f"""\
					<ipxact:field>
						<ipxact:name>{csr_field.name}</ipxact:name>
						<ipxact:bitOffset>{csr_field.base_bit}</ipxact:bitOffset>
						<ipxact:resets>
							<ipxact:reset resetTypeRef="{self.rst}">
								<ipxact:value>{csr_field.rst_val}</ipxact:value>
							</ipxact:reset>
						</ipxact:resets>
						<ipxact:bitWidth>{csr_field.width}</ipxact:bitWidth>
						<ipxact:volatile>{str(csr_field.volatile).lower()}</ipxact:volatile>
						<ipxact:access>{field_access_type}</ipxact:access>
						<ipxact:modifiedWriteValue>{csr_field.write_action}</ipxact:modifiedWriteValue>
						<ipxact:readAction>{csr_field.read_action}</ipxact:readAction>
					</ipxact:field>
"""

        # Generate the xml code
        xml_code = f"""<ipxact:register>
					<ipxact:name>{self.name}</ipxact:name>
					<ipxact:description>{self.description}</ipxact:description>
					<ipxact:addressOffset>"16'h{self.address:04X}</ipxact:addressOffset>
					<ipxact:size>{self.sw_size}</ipxact:size>
					<ipxact:volatile>{str(self.volatile).lower()}</ipxact:volatile>
					<ipxact:access>{access_type}</ipxact:access>
{fields_xml}
				</ipxact:register>"""

        return xml_code


class Port:
    """
    Port class
    """

    def __init__(self, name, direction, n_bits, description, tag):
        self.name = name
        self.direction = direction
        self.n_bits = n_bits
        self.description = description
        self.tag = tag

    def gen_xml(self, parameters_list):
        """
        Generate the xml code for the port
        @param self: port object
        @param parameters_list: list of parameters objects
        return: xml code
        """

        # set the direction
        if self.direction == "input":
            direction = "in"
        elif self.direction == "output":
            direction = "out"
        elif self.direction == "inout":
            direction = "input-output"
        else:
            print(f"ERROR: Port direction not recognized. {self.direction}")
            exit(1)

        # Search for parameters in the n_bits and replace them with their ID
        if isinstance(self.n_bits, str):
            left_bit = replace_params_with_ids(f"{self.n_bits}-1", parameters_list)
            left_bit = escape_xml_special_chars(left_bit)
        else:
            left_bit = self.n_bits - 1

        tag = self.tag

        # Generate the xml code
        xml_code = f"""<ipxact:port>
				<ipxact:name>{self.name}</ipxact:name>
				<ipxact:description>{self.description}</ipxact:description>
				<ipxact:wire>
					<ipxact:direction>{direction}</ipxact:direction>
					<ipxact:vectors>
						<ipxact:vector>
							<ipxact:left>{left_bit}</ipxact:left>
							<ipxact:right>0</ipxact:right>
						</ipxact:vector>
					</ipxact:vectors>
				</ipxact:wire>
				<ipxact:vendorExtensions>
					<kactus2:portTags>{tag}</kactus2:portTags>
				</ipxact:vendorExtensions>
			</ipxact:port>"""

        return xml_code


def gen_ports_list(core):
    """
    Generate the ports list for the given core
    @param core: core object
    return: ports list
    """

    ports_list = []

    for api_group in core.ports:
        group = convert2internal(api_group)
        # Skip doc_only interfaces
        if group.doc_only:
            continue

        tag = ""
        if group.interface:
            tag = group.name

        for api_wire in group.wires:
            wire = convert2internal(api_wire)
            if not isinstance(wire, iob_wire):
                continue
            n_bits = wire.width
            if type(n_bits) is str and n_bits.isnumeric():
                n_bits = int(n_bits)

            ports_list.append(
                Port(
                    wire.name,
                    wire.direction,
                    n_bits,
                    wire.descr,
                    tag,
                )
            )

    return ports_list


def gen_bus_interfaces_list(core):
    """
    Generate the bus interfaces list for the given core
    @param core: core object
    return: bus interfaces list with grouped wires (py2 ports)
    """

    bus_interfaces_list = []

    for api_group in core.ports:
        group = convert2internal(api_group)
        # Skip doc_only interfaces
        if group.doc_only:
            continue

        if group.interface:
            bus_interfaces_list.append(group)

    return bus_interfaces_list


def gen_ports_xml(ports_list, parameters_list):
    """
    Generate the ports xml code
    @param ports_list: list of ports objects
    return: xml code
    """

    # Generate the xml code for the ports
    ports_xml = ""
    for port in ports_list:
        if ports_xml != "":
            ports_xml += "\n"
            # indent the xml code
            ports_xml += "\t" * 3
        ports_xml += port.gen_xml(parameters_list)

    # Generate the xml code for the ports
    xml_code = f"""<ipxact:ports>
			{ports_xml}
		</ipxact:ports>"""

    return xml_code


def gen_bus_interfaces_xml(bus_interfaces_list, ports_list, parameters_list):
    """
    Generate the bus interfaces xml code
    @param bus_interfaces_list: list of bus interfaces with grouped wires (py2 ports)
    @param ports_list: list of ports objects
    return: xml code
    """

    if_ports = {}
    # Generate port_list (wire list) of each interface (py2 port)
    for port in ports_list:
        if port.tag:
            if port.tag not in if_ports:
                if_ports[port.tag] = []
            if_ports[port.tag].append(port)

    # Generate the xml code for the bus interfaces
    bus_interfaces_xml = ""
    for group in bus_interfaces_list:
        portmap_xml = ""
        port_name = group.name
        bus_interface = group.interface
        for port in if_ports[port_name]:
            portmap_xml += f"""\
			<portMap>
				<logicalPort>{port.name}</logicalPort>
				<physicalPort>{port.name}</physicalPort>
			</portMap>
"""

        # Find interface details (including VLNV)
        bus_details = bus_interface.get_interface_details()
        if_mode = "master" if port_name.endswith("_m") else "slave"
        bus_interfaces_xml += f"""\
		<ipxact:busInterface>
			<ipxact:name>{port_name}</ipxact:name>
			<ipxact:displayName>{bus_details["full_name"]}</ipxact:displayName>
			<ipxact:description>{group.descr}</ipxact:description>
			<ipxact:busType vendor="{bus_details["vendor"]}" library="{bus_details["lib"]}" name="{bus_details["name"]}" version="{bus_details["version"]}"/>
			<ipxact:{if_mode}/>
			<ipxact:connectionRequired>true</ipxact:connectionRequired>
{portmap_xml}
		</ipxact:busInterface>
"""

    # Generate the xml code for the bus interfaces
    xml_code = f"""\
<ipxact:busInterfaces>
{bus_interfaces_xml}
	</ipxact:busInterfaces>
"""

    return xml_code


def gen_bus_interface_xml_file(bus_interface, dest_dir):
    """
    Generate the IPXACT XML file for given bus interface.
    @param bus_interface: bus interface object (interfaces.py 'interface' object)
    @param dest_dir: destination directory
    """
    # Find interface details (including VLNV)
    bus_details = bus_interface.get_interface_details()

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Create the Bus Definition file for the interface
    with open(
        f"{dest_dir}/interface_{bus_details['name']}.{bus_details['version']}.xml", "w"
    ) as f:
        f.write(
            f"""\
<?xml version="1.0" encoding="UTF-8"?>
<ipxact:busDefinition xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2022" xmlns:kactus2="http://kactus2.cs.tut.fi" xsi:schemaLocation="http://www.accellera.org/XMLSchema/IPXACT/1685-2022 http://www.accellera.org/XMLSchema/IPXACT/1685-2022/index.xsd">
	<ipxact:vendor>{bus_details["vendor"]}</ipxact:vendor>
	<ipxact:library>{bus_details["lib"]}</ipxact:library>
	<ipxact:name>{bus_details["name"]}</ipxact:name>
	<ipxact:version>{bus_details["version"]}</ipxact:version>
	<ipxact:displayName>{bus_details["full_name"]}</ipxact:displayName>
	<ipxact:shortDescription>{""}</ipxact:shortDescription>
	<ipxact:description>{""}</ipxact:description>
	<ipxact:directConnection>true</ipxact:directConnection>
	<ipxact:vendorExtensions>
		<kactus2:version>3,13,308,0</kactus2:version>
	</ipxact:vendorExtensions>
</ipxact:busDefinition>
"""
        )


#    # Create the Abstraction Definition file for the interface
#    with open(f"{dest_dir}/interface_{bus_interface.kind}.{bus_details['version']}.absDef.xml", "w") as f:
#        f.write(f"""\
# <?xml version="1.0" encoding="UTF-8"?>
# <ipxact:abstractionDefinition xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2022" xmlns:kactus2="http://kactus2.cs.tut.fi" xsi:schemaLocation="http://www.accellera.org/XMLSchema/IPXACT/1685-2022 http://www.accellera.org/XMLSchema/IPXACT/1685-2022/index.xsd">
# 	<ipxact:vendor>{bus_details["vendor"]}</ipxact:vendor>
# 	<ipxact:library>{bus_details["lib"]}</ipxact:library>
# 	<ipxact:name>{bus_details["name"]}.absDef</ipxact:name>
# 	<ipxact:version>{bus_details["version"]}</ipxact:version>
# 	<ipxact:busType vendor="{bus_details["vendor"]}" library="{bus_details["lib"]}" name="{bus_details["name"]}" version="{bus_details["version"]}"/>
# 	<ipxact:vendorExtensions>
# 		<kactus2:version>3,13,308,0</kactus2:version>
# 	</ipxact:vendorExtensions>
# </ipxact:abstractionDefinition>
# """)


def gen_memory_map_xml(sw_regs, parameters_list):
    """
    Generate the memory map xml code
    @param core: core object
    @param sw_regs: list of software registers
    @param parameters_list: list of parameters objects
    return: xml code
    """

    # Generate the software registers list
    sw_regs_list = []
    for sw_reg in sw_regs:
        # create the sw register object
        sw_reg_obj = SwRegister(
            sw_reg.name,
            sw_reg.addr,
            sw_reg.n_bits,
            sw_reg.mode,
            "arst_i",
            sw_reg.rst_val,
            sw_reg.volatile,
            sw_reg.descr,
            parameters_list,
            sw_reg.fields,
        )

        # add it to the sw_regs list
        sw_regs_list.append(sw_reg_obj)

    # Sort the software registers list by address
    sw_regs_list.sort(key=lambda x: x.address)

    # Generate the xml code for the software registers
    sw_regs_xml = ""
    for sw_reg in sw_regs_list:
        if sw_regs_xml != "":
            sw_regs_xml += "\n"
            # indent the xml code
            sw_regs_xml += "\t" * 4
        sw_regs_xml += sw_reg.gen_xml()

    # Compute the memory map range by adding the address and sw_size (in bytes) of the last register
    memory_map_range = sw_regs_list[-1].address + sw_regs_list[-1].sw_size / 8
    # Round up if not an integer
    memory_map_range = math.ceil(memory_map_range)

    # Substitute the ADDR_W parameter value with the memory map range log2
    for param in parameters_list:
        if param.name == "ADDR_W":
            param.def_value = math.ceil(math.log2(memory_map_range))

    # Generate the xml code for the memory map
    xml_code = f"""<ipxact:memoryMaps>
		<ipxact:memoryMap>
			<ipxact:name>CSR</ipxact:name>
			<ipxact:addressBlock>
				<ipxact:name>CSR_REGS</ipxact:name>
				<ipxact:baseAddress>0</ipxact:baseAddress>
				<ipxact:range>{memory_map_range}</ipxact:range>
				<ipxact:width>32</ipxact:width>
				<ipxact:usage>register</ipxact:usage>
				<ipxact:access>read-write</ipxact:access>
				{sw_regs_xml}
			</ipxact:addressBlock>
			<ipxact:addressUnitBits>8</ipxact:addressUnitBits>
		</ipxact:memoryMap>
	</ipxact:memoryMaps>"""

    return xml_code


def gen_parameters_list(core):
    """
    Generate the parameters list for the given core
    @param core: core object
    return: parameters list
    """

    parameters_list = []
    for api_group in core.confs:
        group = convert2internal(api_group)
        # Skip doc_only groups
        if group.doc_only:
            continue
        for api_conf in group.confs:
            conf = convert2internal(api_conf)
            # Skip doc_only confs
            if conf.doc_only:
                continue
            if conf.kind != ["M", "C"]:
                parameters_list.append(
                    Parameter(
                        conf.name,
                        conf.kind,
                        conf.value,
                        conf.min_value,
                        conf.max_value,
                        conf.descr,
                    )
                )

    return parameters_list


def gen_instantiations_xml(core, parameters_list):
    """
    Generate the instantiations xml code
    @param core: core object
    @param parameters_list: list of parameters objects
    return: xml code
    """

    # Generate the parameters xml code
    inst_parameters_xml = ""
    for param in parameters_list:
        # generate the parameter ID and the instance parameter ID
        param_id = param.name + "_ID"
        inst_param_id = param.name + "_INST_ID"
        # increment the usage count of the parameter
        param.usage_count += 1
        if inst_parameters_xml != "":
            inst_parameters_xml += "\n"
            # indent the xml code
            inst_parameters_xml += "\t" * 5
        # generate the xml code
        inst_parameters_xml += f"""<ipxact:moduleParameter parameterId="{inst_param_id}" usageType="nontyped">
						<ipxact:name>{param.name}</ipxact:name>
						<ipxact:value>{param_id}</ipxact:value>
					</ipxact:moduleParameter>"""

    # Generate the xml code for the instantiations
    xml_code = f"""<ipxact:instantiations>
			<ipxact:componentInstantiation>
				<ipxact:name>verilog_implementation</ipxact:name>
				<ipxact:language>Verilog</ipxact:language>
				<ipxact:moduleName>{core.name}</ipxact:moduleName>
				<ipxact:moduleParameters>
					{inst_parameters_xml}
				</ipxact:moduleParameters>
			</ipxact:componentInstantiation>
		</ipxact:instantiations>"""

    return xml_code


def gen_resets_xml(ports_list):
    """
    Generate the resets xml code by finding ports with the word "arst_i" in the last 6 characters
    @param ports_list: list of ports objects
    return: xml code
    """

    # Find the ports with the word "arst_i" in the last 6 characters
    arst_ports = []
    for port in ports_list:
        if port.name[-6:] == "arst_i":
            arst_ports.append(port)

    # Generate the xml code for the resets
    ports_xml_code = ""
    for rst in arst_ports:
        if ports_xml_code != "":
            ports_xml_code += "\n"
            # indent the xml code
            ports_xml_code += "\t" * 2
        ports_xml_code += f"""<ipxact:resetType>
			<ipxact:name>{rst.name}</ipxact:name>
			<ipxact:displayName>{rst.name}</ipxact:displayName>
			<ipxact:description>{rst.description}</ipxact:description>
		</ipxact:resetType>"""

    # Generate the xml code for the resets
    xml_code = f"""<ipxact:resetTypes>
		{ports_xml_code}
	</ipxact:resetTypes>"""

    return xml_code


def gen_parameters_xml(parameters_list):
    """
    Generate the parameters xml code
    @param parameters_list: list of parameters objects
    return: xml code
    """

    # Generate the xml code for the parameters
    parameters_xml = ""
    for param in parameters_list:
        if parameters_xml != "":
            parameters_xml += "\n"
            # indent the xml code
            parameters_xml += "\t" * 2
        parameters_xml += param.gen_xml(parameters_list)

    # Generate the xml code for the parameters
    xml_code = f"""<ipxact:parameters>
		{parameters_xml}
	</ipxact:parameters>"""

    return xml_code


def generate_ipxact_xml(core, dest_dir):
    """
    Generate the xml file for the given core
    @param core: core object
    @param dest_dir: destination directory
    return: None
    """

    csr_block = None
    # Find iob_csrs block in subblocks list
    for api_block in core.subblocks:
        block = convert2internal(api_block)
        if block.original_name == "iob_csrs":
            csr_block = block
            break

    # Add the CSR IF,
    core_name = core.name
    if csr_block and "csr_if" in core.received_iob_parameters:
        core_name += "_" + core.received_iob_parameters["csr_if"]
    # core_name += += "_" + core.data_if

    # Core name to be displayed in the xml file
    # Change "_" to "-" and capitalize all the letters
    core_name_display = core_name.replace("_", "-").upper()

    # Set the core vendor and library
    core_vendor = "IObundle"
    core_library = "IP"

    # Generate the parameters table
    parameters_list = gen_parameters_list(core)

    # Genererate the memory map xml code
    memory_map_xml = ""
    if csr_block:
        sw_regs = static_reg_tables[core.name + "_csrs"]
        memory_map_xml = gen_memory_map_xml(sw_regs, parameters_list)

    # Generate instantiations xml code
    instantiations_xml = gen_instantiations_xml(core, parameters_list)

    # Generate ports list
    ports_list = gen_ports_list(core)

    # Generate ports xml code
    ports_xml = gen_ports_xml(ports_list, parameters_list)

    # Generate bus interfaces list
    bus_interfaces_list = gen_bus_interfaces_list(core)

    for bus_interface in bus_interfaces_list:
        gen_bus_interface_xml_file(bus_interface.interface, dest_dir)

    # Generate bus interfaces xml code
    bus_interfaces_xml = gen_bus_interfaces_xml(
        bus_interfaces_list, ports_list, parameters_list
    )

    # Generate resets xml code
    resets_xml = gen_resets_xml(ports_list)

    # Generate parameters xml code
    parameters_xml = gen_parameters_xml(parameters_list)

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Create the xml file
    xml_file = open(dest_dir + "/" + core_name + ".xml", "w+")

    core_license = convert2internal(core.license)

    # Write the xml header
    xml_text = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<ipxact:component xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2014" xmlns:kactus2="http://kactus2.cs.tut.fi" xsi:schemaLocation="http://www.accellera.org/XMLSchema/IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd">
	<ipxact:vendor>{core_vendor}</ipxact:vendor>
	<ipxact:library>{core_library}</ipxact:library>
	<ipxact:name>{core_name_display}</ipxact:name>
	<ipxact:version>{core.version}</ipxact:version>
	{bus_interfaces_xml}
	{memory_map_xml}
	<ipxact:model>
		<ipxact:views>
			<ipxact:view>
				<ipxact:name>flat_verilog</ipxact:name>
				<ipxact:envIdentifier>Verilog:kactus2.cs.tut.fi:</ipxact:envIdentifier>
				<ipxact:componentInstantiationRef>verilog_implementation</ipxact:componentInstantiationRef>
			</ipxact:view>
		</ipxact:views>
		{instantiations_xml}
		{ports_xml}
	</ipxact:model>
	{resets_xml}
	<ipxact:description>{core.description}</ipxact:description>
	{parameters_xml}
	<ipxact:vendorExtensions>
		<kactus2:author>{core_license.author}</kactus2:author>
		<kactus2:version>3,10,15,0</kactus2:version>
		<kactus2:kts_attributes>
			<kactus2:kts_productHier>Flat</kactus2:kts_productHier>
			<kactus2:kts_implementation>HW</kactus2:kts_implementation>
			<kactus2:kts_firmness>Mutable</kactus2:kts_firmness>
		</kactus2:kts_attributes>
		<kactus2:license>{core_license.name} License, Copyright (c) {core_license.year}</kactus2:license>
	</ipxact:vendorExtensions>
</ipxact:component>"""

    # Write the xml code to the file
    xml_file.write(xml_text)
    xml_file.close()
