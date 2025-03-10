# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# The following installs py2hwsw in nix
# py2hwsw can also be installed with pip using the following command:
# > pip install -e path/to/py2hwsw_directory


{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/24.05.tar.gz") {}, py2hwsw_pkg ? "none" }:
# Py2HWSW uses the following dependencies from nixpkgs version 24.05:
# bash-5.2p26
# gnumake-4.4.1
# iverilog-12.0
# verilator-5.022
# gtkwave-3.3.119
# python3-3.11.9
# python3.11-black-24.4.0
# python3.11-mypy-1.9.0
# python3.11-parse-1.20.1
# python3.11-numpy-1.26.4
# python3.11-wavedrom-2.0.3.post3
# python3.11-matplotlib-3.8.4
# python3.11-scipy-1.13.0
# python3.11-pyserial-3.5
# texlive-combined-2023
# riscv-gnu-toolchain (tag 2022.06.10)
# verible-0.0.3515
# black-24.4.0
# clang-wrapper-14.0.6
# librsvg-2.58.0
# libreoffice-7.6.7.2
# minicom-2.9
# lrzsz-0.12.20
# python3.11-volare (commit 47325949b87e857d75f81d306f02ebccf952cb15)
# yosys (commit 543faed9c8cd7c33bbb407577d56e4b7444ba61c)
# gcc-wrapper-13.2.0
# libcap-2.69
# reuse-3.0.2


let
  # For debug
  force_py2_build = 0;

  py2hwsw =
    if py2hwsw_pkg == "none" then
      # Caller does not provide py2hwsw package
      if force_py2_build == 1 then
        # Environment variable with py2hwsw path is set
        pkgs.python3.pkgs.buildPythonPackage rec {
          pname = "py2hwsw";
          version = "";

          src = pkgs.lib.cleanSource ./../..;

          # Add any necessary dependencies here.
          #propagatedBuildInputs = [ pkgs.python38Packages.someDependency ];
        }
      else
        # Environment variable not set. Dont build py2hwsw package (May have been build previously with pip).
        null
    else
      # Caller provided py2hwsw package
      py2hwsw_pkg;

  # Hack to make Nix libreoffice wrapper work.
  # This is because Nix wrapper breaks ghactions test by requiring the `/run/user/$(id -u)` folder to exist
  libreofficeWithEnv = pkgs.writeShellScriptBin "soffice" ''
    export DBUS_SESSION_BUS_ADDRESS="unix:path=/dev/null"
    exec ${pkgs.libreoffice}/bin/soffice "$@"
  '';

  yosys = import ./scripts/yosys.nix { inherit pkgs; };

  py2hwsw_dependencies = with pkgs; [
    bash
    gnumake
    verilog
    verilator
    gtkwave
    python3
    python3Packages.black
    python3Packages.mypy
    python3Packages.parse
    python3Packages.numpy
    python3Packages.wavedrom
    python3Packages.matplotlib
    python3Packages.scipy
    python3Packages.pyserial
    (texlive.combine { inherit (texlive) scheme-medium multirow lipsum catchfile nowidow enumitem placeins xltabular ltablex titlesec makecell datetime fmtcount comment textpos csquotes amsmath cancel listings hyperref biblatex pmboxdraw; })
    (callPackage ./scripts/riscv-gnu-toolchain.nix { })
    verible
    black
    llvmPackages_14.clangUseLLVM
    librsvg
    libreofficeWithEnv
    minicom     # Terminal emulator
    lrzsz       # For Zmodem file transfers via serial connection of the terminal emulator
    # Add Volare custom Python installation
    (let
      volareSrc = pkgs.fetchFromGitHub {
        owner = "efabless";
        repo = "volare";
        rev = "47325949b87e857d75f81d306f02ebccf952cb15";
        sha256 = "sha256-H9B/vZUs0O2jwmidCTMYhO0JY4DL+gmQNeVawaccvuU=";
      };
    in import "${volareSrc}" {
      inherit pkgs;
    })
    yosys
    gcc
    libcap # Allows setting POSIX capabilities
    reuse
    fusesoc
    py2hwsw
  ];

  get_name = pkg:
    if pkg == null then
      ""
    else
      pkg.name;
  list_of_pkg_names = builtins.filter (x: x != null) (map get_name py2hwsw_dependencies);
  bin_path = builtins.toPath ../../bin;

in

# Uncomment line below to print the Py2HWSW dependency names and versions
#builtins.trace ("Nix dependency versions:\n" + (builtins.concatStringsSep "\n" list_of_pkg_names))

pkgs.mkShell {
  name = "iob-shell";
  buildInputs = py2hwsw_dependencies;
  shellHook = ''
    export PATH="$PATH:${bin_path}"
  '';
}
