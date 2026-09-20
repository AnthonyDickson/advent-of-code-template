# Shared dev-shell definitions for every language template.
#
# Each language maps to a function of `pkgs` returning the extra packages it
# needs. The `common` tooling (task runner, markdown formatter, benchmark
# helpers) is added to every shell, including the lean `default` shell.
#
# Toolchains are pinned to the latest explicit versions offered by the pinned
# nixpkgs (see flake.lock). Bump them here when newer versions are available.
# Tools without a versioned attribute (LSPs, formatters, benchmark helpers)
# stay on their unversioned package name, which tracks the pinned nixpkgs.
{
  systems = [
    "aarch64-darwin"
    "aarch64-linux"
    "x86_64-darwin"
    "x86_64-linux"
  ];

  common = pkgs: with pkgs; [
    just
    # For locating files to pass to formatters
    fd
    # For formatting markdown
    dprint
    # Benchmarking
    hyperfine
    time
  ];

  languages = {
    elixir = pkgs: with pkgs; [
      beam29Packages.elixir_1_20
      beam29Packages.erlang
      elixir-ls
    ];

    gleam = pkgs: with pkgs; [
      gleam
      beam29Packages.erlang
    ];

    go = pkgs: with pkgs; [
      go_1_27
      gopls # lsp
      golangci-lint
    ];

    haskell =
      pkgs:
      let
        ghcPackages = pkgs.haskell.packages.ghc912;
      in
      with pkgs; [
        haskell.compiler.ghc912
        ghcPackages.cabal-install
        ghcPackages.haskell-language-server
        # For formatting Haskell source
        ormolu
      ];

    ocaml =
      pkgs:
      let
        ocamlPackages = pkgs.ocaml-ng.ocamlPackages_5_5;
      in
      [
        ocamlPackages.ocaml
        ocamlPackages.utop
        ocamlPackages.dune_3
        ocamlPackages.odoc
        ocamlPackages.ocaml-lsp
        ocamlPackages.ocamlformat
        ocamlPackages.alcotest
      ];

    python = pkgs: with pkgs; [
      python314
      python314Packages.pytest
      pyright
      ruff
    ];

    rust = pkgs: with pkgs; [
      rust-bin.stable."1.98.1".default
      rust-analyzer
    ];

    zig = pkgs: with pkgs; [
      zig_0_16
      zls_0_16
    ];
  };
}
