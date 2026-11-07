pkgs: {
  # nixpkgs packages no Shakespeare Programming Language implementation, so `uv`
  # builds the environment that runs the plays from PyPI. The dev shell only has
  # to supply the Python that environment is built on, so point `uv` at this one
  # rather than letting it download (or reuse a cached) interpreter of its own.
  packages = with pkgs; [
    python314
  ];

  env.UV_PYTHON_DOWNLOADS = "never";
  env.UV_PYTHON_PREFERENCE = "only-system";
}
