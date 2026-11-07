pkgs: {
  # The prebuilt toolchain, pinned in `../packages/lean4.nix`; keep the
  # template's `lean-toolchain` file in step with its version.
  packages = [
    (pkgs.callPackage ../packages/lean4.nix { })
  ];
}
