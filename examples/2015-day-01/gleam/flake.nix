{
  description = "Gleam Dev Environment";

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
              gleam
              beam28Packages.erlang
              gnumake
              # For formatting markdown
              dprint
              # Benchmarking
              hyperfine
              time
            ];
          };
      }
    );
}
