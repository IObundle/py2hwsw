# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


### Launch minicom if running Linux
# pass CI variable over ssh commands
UFLAGS+=CI=$(CI)
ifeq ($(RUN_LINUX),1)
# Check if minicom test script exists
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
else # CI is not set
FAKE_STDOUT:=
RUN_MINICOM_IN_BACKGROUND:=
endif # CI
endif # minicom_linux_script.txt
# Set a capture file and print its contents (to work around minicom clearing the screen)
LOG_STR:=-C minicom_out.log $(FAKE_STDOUT) || cat minicom_out.log
# Set HOME to current (fpga) directory (needed because minicom always reads the '.minirc.*' config file from HOME)
HOME_STR:=HOME=$$(pwd)
# Append minicom to interact with linux after running console.
# Always exit with code 0 (since linux is terminated with CTRL-C).
CONSOLE_CMD +=$(PYTHON_DIR)/console.py -s $(BOARD_SERIAL_PORT) && (($(HOME_STR) $(TERM_STR) minicom iobundle.dfl $(SCRIPT_STR) $(LOG_STR) || (exit 0)) $(RUN_MINICOM_IN_BACKGROUND) )
endif # RUN_LINUX


# include fpga build segment of child systems
# child systems can add their own child2_fpga_build.mk without having to override this one.
ifneq ($(wildcard child2_fpga_build.mk),)
include child2_fpga_build.mk
endif
