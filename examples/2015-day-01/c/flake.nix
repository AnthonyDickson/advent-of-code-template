{
  description = "C Dev Environment";

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
              gcc15
              gnumake
              clang-tools # for clangd and clang-format
              bear # for auto-generating compile_commands.json for clangd
              dprint # For formatting markdown
              hyperfine # Benchmarking
            ];
          };
      }
    );
}
