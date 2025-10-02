# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  name = "verilator";
  src = pkgs.fetchFromGitHub {
    repo = "verilator";
    owner = "verilator";
    rev = "v5.040";
    sha256 = "sha256-S+cDnKOTPjLw+sNmWL3+Ay6+UM8poMadkyPSGd3hgnc=";
  };

  # patch and postpatch, taken from:
  # https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/ve/verilator/package.nix
  patches = [
    (pkgs.fetchpatch {
      name = "clang-V3hash-overload-fix.patch";
      url = "https://github.com/verilator/verilator/commit/2aa260a03b67d3fe86bc64b8a59183f8dc21e117.patch";
      hash = "sha256-waUsctWiAMG3lCpQi+VUUZ7qMw/kJGu/wNXPHZGuAoU=";
    })
  ];

  postPatch = ''
    patchShebangs bin/* src/* nodist/* docs/bin/* examples/xml_py/* \
    test_regress/{driver.py,t/*.{pl,pf}} \
    test_regress/t/t_a1_first_cc.py \
    test_regress/t/t_a2_first_sc.py \
    ci/* ci/docker/run/* ci/docker/run/hooks/* ci/docker/buildenv/build.sh
    # verilator --gdbbt uses /bin/echo to test if gdb works.
    substituteInPlace bin/verilator --replace-fail "/bin/echo" "${pkgs.coreutils}/bin/echo"
  '';

  enableParallelBuilding = true;

  # build + run dependencies
  buildInputs = [ 
     pkgs.perl
     (pkgs.python3.withPackages (
        pp: with pp; [
            distro
        ]
     ))
   ];
  # build only dependencies
  nativeBuildInputs = [
     pkgs.makeWrapper
     pkgs.flex
     pkgs.bison
     pkgs.autoconf
     pkgs.help2man
     pkgs.git
  ];

  nativeCheckInputs = [
     pkgs.which
     pkgs.coreutils
     pkgs.python3
     pkgs.numactl
  ];

  configurePhase = ''
    autoconf
    ./configure --prefix=$out
  '';
  buildPhase = "make -j$(nproc)";
  installPhase = "make install";
}
