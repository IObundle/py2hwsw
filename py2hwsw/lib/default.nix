# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

# The following installs py2hwsw in nix
# py2hwsw can also be installed with pip using the following command:
# > pip install -e path/to/py2hwsw_directory


{ pkgs ? import <nixpkgs> {}, py2hwsw_pkg ? "none" }:

let
  # For debug
  disable_py2_build = 0;

  py2hwsw =
    if py2hwsw_pkg == "none" then
      # Caller does not provide py2hwsw package
      if disable_py2_build == 0 then
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
in

pkgs.mkShell {
  name = "iob-shell";
  buildInputs = with pkgs; [
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
    (texlive.combine { inherit (texlive) scheme-medium multirow lipsum catchfile nowidow enumitem placeins xltabular ltablex titlesec makecell datetime fmtcount comment textpos csquotes amsmath cancel listings hyperref biblatex; })
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
    py2hwsw
  ];
}
