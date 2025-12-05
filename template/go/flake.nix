{
  description = "Go Dev Environment";

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
              go
              gopls # lsp
              golangci-lint
              gnumake
              dprint # For formatting markdown
              hyperfine # Benchmarking
            ];
          };
      }
    );
}
