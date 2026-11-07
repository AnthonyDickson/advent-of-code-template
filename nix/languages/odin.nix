pkgs: {
  # nixpkgs only carries Odin on the unversioned `odin` attribute
  # (dev-<year>-<month>), so there is no explicit version to pin here.
  packages = with pkgs; [
    odin
    ols # lsp, also provides `odinfmt`
  ];
}
