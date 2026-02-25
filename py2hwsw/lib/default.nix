# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# The following installs py2hwsw in nix
# py2hwsw can also be installed with pip using the following command:
# > pip install -e path/to/py2hwsw_directory


{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/25.05.tar.gz") {}, py2hwsw_pkg ? "none", extra_pkgs ? [] }:
# Py2HWSW uses the following dependencies from nixpkgs version 24.05:
# bash-interactive-5.2p37
# gnumake-4.4.1
# iverilog-12.0
# verilator (custom version v5.040)
# gtkwave-3.3.121
# python3-3.12.10
# python3 black-25.1.0
# python3 mypy-1.15.0
# python3 parse-1.20.2
# python3 numpy-2.2.5
# python3 wavedrom-2.0.3.post3
# python3 matplotlib-3.10.1
# python3 scipy-1.15.3
# python3 pyserial-3.5
# python3 pydantic-2.11.1
# python3 jinja2-3.1.6
# texlive-combined-2024
# riscv-gnu-toolchain (tag 2022.06.10)
# verible-0.0.3956
# black-25.1.0
# clang-wrapper-14.0.6
# librsvg-2.60.0
# soffice
# openjdk-21.0.7+6
# minicom-2.10
# lrzsz-0.12.20
# python3.12-volare (commit 47325949b87e857d75f81d306f02ebccf952cb15)
# yosys (commit 543faed9c8cd7c33bbb407577d56e4b7444ba61c)
# gcc-wrapper-14.2.1.20250322
# libcap-2.75
# reuse-5.0.2
# python3.12-fusesoc-2.4.5
# kactus2 (commit 19c5702)
# doxygen-1.13.2

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

  verilator_v5_040 = import ./scripts/verilator.nix { inherit pkgs; };

  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    black
    mypy
    parse
    numpy
    wavedrom
    matplotlib
    scipy
    pyserial
    pydantic
    jinja2
  ]);

  # FuseSoC provided by nixpkgs is not adequate for py2hwsw. Use custom version from GitHub.
  custom_fusesoc = pkgs.python3.pkgs.buildPythonPackage rec {
    pname = "fusesoc";
    version = "2.4.5";
  
    src = pkgs.fetchzip {
      url = "https://github.com/olofk/fusesoc/archive/refs/tags/${version}.tar.gz";
      sha256 = "1sw0zl6hjlzp1a0agdl9yp901pih70ppzzss18l8f3jxs6q7jm1n";  # Run `nix-prefetch-url --unpack https://...` to get the hash
    };

    format = "pyproject";  # Tells Nix to use pyproject.toml instead of setup.py

   # FuseSoC dependencies (from its pyproject.toml)
    propagatedBuildInputs = with pkgs.python3.pkgs; [
      click
      toml
      jsonschema
      packaging
      pyyaml
      edalize
      pyparsing
      fastjsonschema
      argcomplete
      simplesat
    ]; 

    # BUILD INPUTS - required by [build-system] in pyproject.toml
    nativeBuildInputs = with pkgs.python3.pkgs; [
      setuptools
      wheel
      setuptools_scm
    ];

    #doCheck = false;  # Skip tests (optional, speeds up build)

    # FuseSoC uses pyproject.toml (PEP 621), so format="pyproject" is auto-detected in modern nixpkgs (25.05+).
    # Add propagatedBuildInputs if needed (e.g., for click, toml; check `pip show fusesoc` after manual install).
    # propagatedBuildInputs = with pkgs.python3.pkgs; [ click toml ];
  };

  py2hwsw_dependencies = with pkgs; [
    bash
    gnumake
    verilog
    gtkwave
    python3
    pythonEnv
    (texlive.combine { inherit (texlive) scheme-medium multirow lipsum catchfile nowidow enumitem placeins xltabular ltablex titlesec makecell datetime fmtcount comment textpos csquotes amsmath cancel listings hyperref biblatex pmboxdraw varwidth hanging adjustbox stackengine alphalph; })
    (callPackage ./scripts/riscv-gnu-toolchain.nix { })
    verible
    black
    llvmPackages_14.clangUseLLVM
    librsvg
    libreofficeWithEnv
    jre # Dependency of libreoffice
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
    verilator_v5_040
    yosys
    gcc
    libcap # Allows setting POSIX capabilities
    reuse
    custom_fusesoc
    (callPackage ./scripts/kactus2.nix { })
    doxygen
    py2hwsw
  ] ++ extra_pkgs;

  get_name = pkg:
    if pkg == null then
      ""
    else
      pkg.name;
  list_of_pkg_names = builtins.filter (x: x != null) (map get_name py2hwsw_dependencies);
  bin_path = builtins.toPath ../../bin;

in

# Uncomment line below to print the Py2HWSW dependency names and versions
# builtins.trace ("Nix dependency versions:\n" + (builtins.concatStringsSep "\n" list_of_pkg_names))

pkgs.mkShell {
  name = "iob-shell";
  buildInputs = py2hwsw_dependencies;
  shellHook = ''
    export PATH="$PATH:${bin_path}"
    export PYTHONPATH=${pythonEnv}/${pythonEnv.sitePackages}
  '';
}
