# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  name = "kactus2";
  src = pkgs.fetchFromGitHub {
    owner = "kactus2";
    repo = "kactus2dev";
    rev = "16813a2";
    sha256 = "1pj6rwl4h6lcpmqw4cm9im7k8pfrya6ca0hjpgijix0lndfpz1n6";
  };

  nativeBuildInputs = [ pkgs.git pkgs.swig pkgs.qt6.wrapQtAppsHook ];
  buildInputs = [ pkgs.qt6.qtbase pkgs.qt6.qttools pkgs.qt6.qtsvg pkgs.libGL pkgs.python3 ];

  # Ignore errors generating help files
  # patchPhase = ''
  #   sed -i 's/^cp -f Help\/Kactus2Help\.qhc executable\/Help\/Kactus2Help\.qhc$/& || true/; s/^cp -f Help\/Kactus2Help\.qch executable\/Help\/Kactus2Help\.qch$/& || true/' createhelp
  # '';

  configurePhase = ''
    ./configure --prefix=$out
  '';

  buildPhase = ''
    make -j$NIX_BUILD_CORES
  '';

  installPhase = ''
    make INSTALL_ROOT=$out install
    mv $out/lib64 $out/lib
    install -D -m644 LICENSE $out/share/licenses/kactus2-git/LICENSE
  '';

  meta = {
    description = "Open source IP-XACT-based tool for ASIC, FPGA and embedded systems design";
    homepage = https://research.tuni.fi/system-on-chip/tools/;
    license = pkgs.lib.licenses.gpl2;
    platforms = pkgs.lib.platforms.all;
  };
}
