pkgs: {
  packages = with pkgs; [
    go_1_27
    gopls # lsp
    golangci-lint
  ];
}
