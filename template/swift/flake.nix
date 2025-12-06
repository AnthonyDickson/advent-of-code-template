{
  description = "Swift development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = with pkgs; mkShell {
          packages = with pkgs; [
            # NOTE: Assumes swift 6.2.1 and sourcekit-lsp is already installed
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
