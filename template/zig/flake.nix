{
  description = "Zig Dev Environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default =
          with pkgs;
          mkShell {
            packages = with pkgs; [
              # Zig 0.15.2
              zig
              # ZLS 0.15.0
              zls
              # For formatting markdown
              dprint
              # Benchmarking
              hyperfine
            ];
          };
      }
    );
}

