pkgs: {
  packages = with pkgs; [
    rust-bin.stable."1.98.1".default
    rust-analyzer
  ];
}
