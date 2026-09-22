# Shared dev-shell definitions for every language template.
#
# Each language maps to a function of `pkgs` returning the shell attributes it
# needs on top of the shared tooling: `packages`, plus optional `env` entries or
# a `shellHook`. The `common` tooling (task runner, markdown formatter, benchmark
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

  common =
    pkgs: with pkgs; [
      just
      # For locating files to pass to formatters
      fd
      # For formatting markdown
      dprint
      # For running the language lottery in tools/lottery (it fetches its own deps, and
      # asks git which files the templates ignore)
      uv
      git
      # Benchmarking
      hyperfine
      time
    ];

  languages = {
    clojure = pkgs: {
      packages = with pkgs; [
        clojure
        clojure-lsp # lsp
        # For linting and formatting Clojure source
        clj-kondo
        cljfmt
        jdk21
      ];
    };

    common-lisp = pkgs: {
      # `sbcl.withPackages` puts the listed systems, and their transitive
      # dependencies, on ASDF's source registry, so the template needs no
      # Quicklisp: `rove` is the test framework.
      packages = [
        (pkgs.sbcl.withPackages (ps: [ ps.rove ]))
      ];
    };

    elixir = pkgs: {
      packages = with pkgs; [
        beam29Packages.elixir_1_20
        beam29Packages.erlang
        elixir-ls
      ];
    };

    fsharp = pkgs: {
      packages = with pkgs; [
        dotnet-sdk_10
      ];

      # .NET tooling that does not go through the SDK wrapper on `PATH` (editor
      # integrations, `dotnet` apphosts) resolves the shared runtime from here.
      # The SDK installs its payload under `share/dotnet`, which is what an
      # apphost expects `DOTNET_ROOT` to point at; the wrapper store path itself
      # has no `shared/Microsoft.NETCore.App`, so apphosts fail to launch against
      # it while the `dotnet` muxer keeps working.
      env.DOTNET_ROOT = "${pkgs.dotnet-sdk_10}/share/dotnet";

      shellHook = ''
        echo "F# dev shell"
        echo "  dotnet $(dotnet --version)"

        # Restore the tools pinned by the nearest .config/dotnet-tools.json
        # (fantomas, fsautocomplete, ...). They are restored per project rather
        # than taken from nixpkgs so they always match this SDK.
        manifest_dir=$PWD
        while [ "$manifest_dir" != "/" ]; do
          if [ -f "$manifest_dir/.config/dotnet-tools.json" ]; then
            dotnet tool restore --tool-manifest "$manifest_dir/.config/dotnet-tools.json"
            break
          fi
          manifest_dir=$(dirname "$manifest_dir")
        done
        unset manifest_dir
      '';
    };

    gleam = pkgs: {
      packages = with pkgs; [
        gleam
        beam29Packages.erlang
      ];
    };

    go = pkgs: {
      packages = with pkgs; [
        go_1_27
        gopls # lsp
        golangci-lint
      ];
    };

    haskell =
      pkgs:
      let
        ghcPackages = pkgs.haskell.packages.ghc912;
      in
      {
        packages = with pkgs; [
          haskell.compiler.ghc912
          ghcPackages.cabal-install
          ghcPackages.haskell-language-server
          # For formatting Haskell source
          ormolu
        ];
      };

    ocaml =
      pkgs:
      let
        ocamlPackages = pkgs.ocaml-ng.ocamlPackages_5_5;
      in
      {
        packages = [
          ocamlPackages.ocaml
          ocamlPackages.utop
          ocamlPackages.dune_3
          ocamlPackages.odoc
          ocamlPackages.ocaml-lsp
          ocamlPackages.ocamlformat
          ocamlPackages.alcotest
        ];
      };

    odin = pkgs: {
      # nixpkgs only carries Odin on the unversioned `odin` attribute
      # (dev-<year>-<month>), so there is no explicit version to pin here.
      packages = with pkgs; [
        odin
        ols # lsp, also provides `odinfmt`
      ];
    };

    python = pkgs: {
      packages = with pkgs; [
        python314
        python314Packages.pytest
        pyright
        ruff
        uv
      ];
    };

    rust = pkgs: {
      packages = with pkgs; [
        rust-bin.stable."1.98.1".default
        rust-analyzer
      ];
    };

    scala = pkgs: {
      packages = with pkgs; [
        scala-cli
        metals # lsp
        scalafmt
        jdk21
      ];

      # Scala CLI and scalafmt take the JDK from here instead of fetching one
      # with coursier, so entering the shell does not download a JVM.
      env.JAVA_HOME = "${pkgs.jdk21}";
    };

    shakespeare = pkgs: {
      # nixpkgs packages no Shakespeare Programming Language implementation, so `uv`
      # builds the environment that runs the plays from PyPI. The dev shell only has
      # to supply the Python that environment is built on, so point `uv` at this one
      # rather than letting it download (or reuse a cached) interpreter of its own.
      packages = with pkgs; [
        python314
      ];

      env.UV_PYTHON_DOWNLOADS = "never";
      env.UV_PYTHON_PREFERENCE = "only-system";
    };

    typst = pkgs: {
      # nixpkgs carries Typst on the unversioned `typst` attribute, so its version
      # moves with the pinned nixpkgs rather than being pinned here.
      packages = with pkgs; [
        typst
        typstyle # formatter
        tinymist # lsp
      ];
    };

    zig = pkgs: {
      packages = with pkgs; [
        zig_0_16
        zls_0_16
      ];
    };
  };
}
