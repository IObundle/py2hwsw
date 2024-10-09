# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

{ pkgs ? import <nixpkgs> {} }:
import py2hwsw/lib/scripts/default.nix { inherit pkgs; }
