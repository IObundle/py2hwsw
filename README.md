# py2hwsw
## A Python framework for embedded HW/SW projects

In this project, we propose to develop a Python framework to (1) manage the files of an embedded hardware/software (HW/SW) codesign project and (2) generate the Verilog code of the hardware components. The framework will be tested on the OpenCrypto system created in previously NGI-supported projects. The flow will use only open-source tools.

An embedded HW/SW project requires that various source files be conveniently organized in a directory tree so that the build scripts can produce the needed artifacts. Typically, Makefiles and different scripting languages are employed, which is often a barrier for new developers. The proposed Python framework will raise developer accessibility by providing a single cockpit for the design process.

Hardware Design Languages such as Verilog and VHDL give a lot of flexibility to users. Still, the design tools reject most of their features and force users to use a small, low-level subset if we want the code to be human-readable and portable to both FPGAs and ASICs. The result is a very tedious and error-prone hardware design process. Therefore, we propose a  tool to generate portable Verilog code using a Python API.
