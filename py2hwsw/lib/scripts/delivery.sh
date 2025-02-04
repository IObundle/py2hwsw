#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

#
# This script is used to create the IP core deliverables package.
#
# The varibles not defined here are assumed defined in the parent script, tipically a Makefile.
#

#make this script exit on error
set -e

echo "Setup the build directory and tar it up"
make clean setup


#get name and version using bootstrap.py
NAME=`py2hwsw $CORE print_core_name`
VERSION_STR=`py2hwsw $CORE print_core_version`

BUILD_VSRC_DIR=$BUILD_DIR/hardware/src
BUILD_SIM_DIR=$BUILD_DIR/hardware/simulation
BUILD_FPGA_DIR=$BUILD_DIR/hardware/fpga
BUILD_SYN_DIR=$BUILD_DIR/hardware/syn
BUILD_DOC_DIR=$BUILD_DIR/document
BUILD_FIG_DIR=$BUILD_DOC_DIR/figures
BUILD_TSRC_DIR=$BUILD_DIR/software/src

echo "Base tar file name"
TARNAME=$NAME
TARNAME+="_"
TARNAME+=$VERSION_STR
TARNAME+="_"
TARNAME+=$SUFFIX

echo "Simulation files"
rm -f $BUILD_SIM_DIR/xcelium_cov_commands.ccf
rm -f $BUILD_SIM_DIR/xcelium_cov.tcl
rm -f $BUILD_SIM_DIR/uut.gtkw
rm -f $BUILD_SIM_DIR/iob_cov_waiver.tcl

echo "Documentation files"
UG=$NAME-$VERSION_STR-usg.pdf
RN=$NAME-$VERSION_STR-rel.pdf

echo "User guide"
make -C $BUILD_DIR doc-build DOC=ug
mv $BUILD_DOC_DIR/ug.pdf $BUILD_DOC_DIR/$UG

echo "Release notes"
make -C $BUILD_DIR doc-build DOC=rn && mv $BUILD_DOC_DIR/rn.pdf $BUILD_DOC_DIR/$RN

echo "Removing unnecessary files"
find $BUILD_DOC_DIR -not \( -name document \
	-o -name $UG \
	-o -name $RN \
	-o -name iob_cov_waiver.tcl \
	-o -name ipxact \
        -o -name README \
        \) -delete

make -C $BUILD_SIM_DIR very-clean
rm -rf $BUILD_DIR/hardware/lint
sed -i '/^clean:/s/lint-clean //g' $BUILD_DIR/Makefile
rm -rf $BUILD_DIR/scripts
find $BUILD_DIR/hardware/fpga -name \*.pdf -delete
find $BUILD_DIR -name \*.ods -delete
rm -f $BUILD_DIR/config_delivery.mk

echo "Release tar file"
DELIVERYTARNAME=$TARNAME
DELIVERYTARNAME+="_rel.tgz"
tar cvzf ../$DELIVERYTARNAME $BUILD_DIR

echo ""
echo "Done"
echo ""
