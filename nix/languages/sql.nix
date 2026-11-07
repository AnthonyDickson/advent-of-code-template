pkgs: {
  # nixpkgs carries DuckDB on the unversioned `duckdb` attribute, so its
  # version moves with the pinned nixpkgs rather than being pinned here. The
  # CLI is the whole toolchain: a solution needs no server and no libraries.
  packages = with pkgs; [
    duckdb
  ];
}
