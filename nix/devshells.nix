# Shared dev-shell definitions for every language template.
#
# Each language has a file in `languages/`, named after its `template/` folder:
# a function of `pkgs` returning the shell attributes it needs on top of the
# shared tooling, `packages` plus optional `env` entries or a `shellHook`. The
# files are discovered, not listed, so adding a language means adding a file.
# The `common` tooling (task runner, markdown formatter, benchmark helpers) is
# added to every shell, including the lean `default` shell.
#
# Toolchains are pinned to the latest explicit versions offered by the pinned
# nixpkgs (see flake.lock). Bump them in the language files when newer versions
# are available. Tools without a versioned attribute (LSPs, formatters,
# benchmark helpers) stay on their unversioned package name, which tracks the
# pinned nixpkgs. Toolchains nixpkgs cannot provide are packaged from prebuilt
# releases in `packages/`, each pinning its own version.
{
  systems = [
    "aarch64-darwin"
    "aarch64-linux"
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
      # For counting the application code lines the results recorder records
      tokei
    ];

  # `languages/<lang>.nix` becomes the `<lang>` shell.
  languages =
    let
      files = builtins.filter (file: builtins.match ".+\\.nix" file != null) (
        builtins.attrNames (builtins.readDir ./languages)
      );
    in
    builtins.listToAttrs (
      map (file: {
        name = builtins.substring 0 (builtins.stringLength file - 4) file;
        value = import (./languages + "/${file}");
      }) files
    );
}
