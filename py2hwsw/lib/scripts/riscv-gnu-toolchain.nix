# SPDX-FileCopyrightText: 2026 IObundle
#
# SPDX-License-Identifier: GPL-3.0-only

{ pkgs ? import <nixpkgs> {} }:

let
  # 1. Create a custom GitHub fetcher that uses your own logic, since pkgs.fetchFromGitHub does not work well for riscv-gnu-toolchain
  sourcedata = pkgs.stdenv.mkDerivation {
    name = "riscv-toolchain-source-custom";
    
    # This is the "Magic Sauce": Providing a hash turns this into 
    # a Fixed-Output Derivation, which grants internet access.
    outputHashMode = "recursive";
    outputHashAlgo = "sha256";
    #outputHash = pkgs.lib.fakeSha256; # Replace this with the real hash later
    outputHash = "sha256-6ppfH5gASHPepByOH6A7QxW+YrZFhaqinLVcwDWBjVw=";

    nativeBuildInputs = [ pkgs.git pkgs.cacert ];

    builder = pkgs.writeShellScript "fetcher-script.sh" ''
      export PATH=$PATH:${pkgs.git}/bin
      # Git needs a place to store its config
      export HOME=$TMPDIR
      
      # Perform the fetch exactly how you want it
      git clone https://github.com/riscv/riscv-gnu-toolchain.git $out
      cd $out
      git checkout 2026.04.05
      
      # You can even do manual fixes here if a submodule is still failing
      # git submodule update --init --recursive ...
      git submodule update --init --depth 1 gcc gdb binutils newlib
      
      # Clean up .git folders if you want to save space/ensure determinism
      # The .git folders are not deterministic, causes issues with hash. https://github.com/NixOS/nixpkgs/issues/8567
      find $out -name ".git" -exec rm -rf {} +
    '';
  };
in
pkgs.stdenv.mkDerivation {
  name = "riscv-gnu-toolchain";
  src = sourcedata;
  #src = pkgs.fetchFromGitHub {
  #  repo = "riscv-gnu-toolchain";
  #  owner = "riscv-collab";
  #  rev = "2026.04.05";
  #  fetchSubmodules = true; # This causes issues cloning submodules of riscv-gnu-toolchain. Use our own custom fetcher script instead.
  #  #leaveDotGit = true; #This is not deterministic, causes issues with hash. https://github.com/NixOS/nixpkgs/issues/8567
  #  sha256 = "sha256-U0DbS93/6APc0gcIKigMpQR8CwyCj6WvKCg2f2aVbnU=";
  #};
  buildInputs = [ 
     pkgs.gmp
     pkgs.libmpc
     pkgs.mpfr
   ];
  nativeBuildInputs = [
     pkgs.gcc
     pkgs.which
     pkgs.python3
     pkgs.util-linux
     pkgs.git
     pkgs.cacert
     pkgs.autoconf
     pkgs.automake
     pkgs.curl
     pkgs.python3
     pkgs.gawk
     pkgs.bison
     pkgs.flex
     pkgs.texinfo
     pkgs.gperf
     pkgs.bc
     pkgs.perl
     pkgs.expat
     pkgs.gettext
  ];
  buildPhase = ''
    # Build in /tmp dir because the Nix tmpfs build/ partition does not have enough space to build this toolchain
    rm -fr /tmp/`basename $src`
    cp -r $src /tmp/`basename $src`
    cd /tmp/`basename $src`
    chmod +w -R .

    # Rewrites shebang lines (e.g., #!/bin/sh) in executable scripts to use Nix store paths instead of standard system paths like /bin/sh or /usr/bin/env python
    patchShebangs .

    # Hack to manually create git reposiories because .git folders were deleted by leaveDotGit=false
    for path in "." "gcc" "gdb" "binutils" "newlib"; do
        env -C $path git init --initial-branch=main;
    done

    ./configure \
      --prefix=$out \
      --enable-multilib
    make -j$(nproc)
  '';
  installPhase = ''
    cd /tmp/`basename $src`
    make install
  '';

  clean = ''
    rm -fr /tmp/`basename $src`
  '';

  hardeningDisable = [ "format" ];
}
