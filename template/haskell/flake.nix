{
  description = "Haskell Dev Environment";

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
              ghc
              cabal-install
              haskell-language-server
              gnumake
              # For formatting markdown
              dprint
              # Benchmarking
              hyperfine
            ];
          };
      }
    );
}

