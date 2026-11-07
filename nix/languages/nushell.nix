pkgs: {
  # nixpkgs carries Nushell on the unversioned `nushell` attribute, so its
  # version moves with the pinned nixpkgs rather than being pinned here. The
  # language server is built in (`nu --lsp`), so there is no separate package.
  packages = with pkgs; [
    nushell
  ];
}
