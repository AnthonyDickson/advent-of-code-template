pkgs: {
  # The nightly compiler, pinned in `../packages/roc.nix`; keep the `roc:` entry
  # in the templates' `app` headers in step with it.
  packages = [
    (pkgs.callPackage ../packages/roc.nix { })
  ];
}
