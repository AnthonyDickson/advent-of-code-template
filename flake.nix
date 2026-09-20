{
  description = "Advent of Code development environments";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      rust-overlay,
      ...
    }:
    let
      devshells = import ./nix/devshells.nix;
      overlays = [ (import rust-overlay) ];
    in
    {
      # `nix develop .#<language>` from anywhere in the repository.
      # `nix develop` (or `.#default`) provides only the shared tooling.
      devShells = nixpkgs.lib.genAttrs devshells.systems (
        system:
        let
          pkgs = import nixpkgs {
            inherit system overlays;
          };
          mkShell = extra: pkgs.mkShell { packages = devshells.common pkgs ++ extra pkgs; };
        in
        {
          default = mkShell (_: [ ]);
        }
        // nixpkgs.lib.mapAttrs (_: mkShell) devshells.languages
      );
    };
}
