# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

{ pkgs ? import <nixpkgs> {} }:

let
  # Required qt6 components for kactus2
  qt6Components = with pkgs.qt6; [ qtbase qttools qtsvg ];
  # Combine all qt6 components into one virtual package
  unifiedQt6Bin = pkgs.symlinkJoin {
    name = "unified-qt6-bin";
    paths = qt6Components;
  };
in
pkgs.stdenv.mkDerivation {
  name = "kactus2";
  src = pkgs.fetchFromGitHub {
    owner = "kactus2";
    repo = "kactus2dev";
    rev = "19c5702";
    sha256 = "jAMu/BqBjXP35skXXPu2zU5PZVJvangyyoLRjqkmLuI=";
  };

  # Replace pkgs.swig4 with pkgs.swig on newer nixpkgs (> 24.05)
  nativeBuildInputs = [ pkgs.git pkgs.swig4 pkgs.qt6.wrapQtAppsHook ];
  buildInputs = [ pkgs.qt6.qtbase pkgs.qt6.qttools pkgs.qt6.qtsvg unifiedQt6Bin pkgs.libGL pkgs.python3 ];

  configurePhase = ''
    # Set QTBIN_PATH to unifiedQt6Bin
    sed -i 's|^QTBIN_PATH=""|QTBIN_PATH="${unifiedQt6Bin}/bin/"\nQTLIBEXEC_PATH="${unifiedQt6Bin}/libexec/"|' ./configure
    ./configure --prefix=$out
  '';

  buildPhase = ''
    make -j$NIX_BUILD_CORES
  '';

  installPhase = ''
    # Set temporary writable home directory (kactus2 tries to create files in home).
    # Nix does not recommend creating files in home during build of packages.
    export HOME=$TMPDIR/nix-build-kactus2
    # Set correct install directories
    sed -i 's|^LOCAL_INSTALL_DIR=""|LOCAL_INSTALL_DIR="'$out'"|' ./.qmake.conf
    sed -i 's|^    bin_path = $$LOCAL_INSTALL_DIR|    bin_path = $$LOCAL_INSTALL_DIR/bin|' ./.qmake.conf
    sed -i 's|^    lib_path = $$LOCAL_INSTALL_DIR|    lib_path = $$LOCAL_INSTALL_DIR/lib|' ./.qmake.conf
    # Install
    make install
    # Add kactus2 PythonAPI directory to the PYTHONPATH environment variable
    mkdir -p $out/nix-support
    cat > $out/nix-support/setup-hook <<EOF
      export PYTHONPATH=$out/lib:''${PYTHONPATH:-}
    EOF
  '';


  meta = {
    description = "Open source IP-XACT-based tool for ASIC, FPGA and embedded systems design";
    homepage = https://research.tuni.fi/system-on-chip/tools/;
    license = pkgs.lib.licenses.gpl2;
    platforms = pkgs.lib.platforms.all;
  };
}
