pkgs: {
  # `uv` builds the project's `.venv` (pytest and ruff, pinned in uv.lock) on
  # this Python rather than downloading (or reusing a cached) interpreter of
  # its own. `ruff` and `pyright` are here for editors.
  packages = with pkgs; [
    python314
    pyright
    ruff
    uv
  ];

  env.UV_PYTHON_DOWNLOADS = "never";
  env.UV_PYTHON_PREFERENCE = "only-system";
}
