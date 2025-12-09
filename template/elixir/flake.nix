{
  description = "Elixir Dev Environment";

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
              beam28Packages.elixir_1_19
              beam28Packages.erlang
              elixir-ls
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

