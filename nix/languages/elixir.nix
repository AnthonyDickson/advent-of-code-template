pkgs: {
  packages = with pkgs; [
    beam29Packages.elixir_1_20
    beam29Packages.erlang
    beam29Packages.expert # lsp
  ];
}
