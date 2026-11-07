pkgs: {
  # Deno runs and type-checks TypeScript directly, and nixpkgs carries it on
  # the unversioned `deno` attribute, so its version moves with the pinned
  # nixpkgs rather than being pinned here. The language server is built in
  # (`deno lsp`), so there is no separate package.
  packages = with pkgs; [
    deno
  ];
}
