pkgs: {
  # nixpkgs carries Typst on the unversioned `typst` attribute, so its version
  # moves with the pinned nixpkgs rather than being pinned here.
  packages = with pkgs; [
    typst
    typstyle # formatter
    tinymist # lsp
  ];
}
