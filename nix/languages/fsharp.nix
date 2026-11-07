pkgs: {
  packages = with pkgs; [
    dotnet-sdk_10
  ];

  # .NET tooling that does not go through the SDK wrapper on `PATH` (editor
  # integrations, `dotnet` apphosts) resolves the shared runtime from here.
  # The SDK installs its payload under `share/dotnet`, which is what an
  # apphost expects `DOTNET_ROOT` to point at; the wrapper store path itself
  # has no `shared/Microsoft.NETCore.App`, so apphosts fail to launch against
  # it while the `dotnet` muxer keeps working.
  env.DOTNET_ROOT = "${pkgs.dotnet-sdk_10}/share/dotnet";

  shellHook = ''
    echo "F# dev shell"
    echo "  dotnet $(dotnet --version)"

    # Restore the tools pinned by the nearest .config/dotnet-tools.json
    # (fantomas, fsautocomplete, ...). They are restored per project rather
    # than taken from nixpkgs so they always match this SDK.
    manifest_dir=$PWD
    while [ "$manifest_dir" != "/" ]; do
      if [ -f "$manifest_dir/.config/dotnet-tools.json" ]; then
        dotnet tool restore --tool-manifest "$manifest_dir/.config/dotnet-tools.json"
        break
      fi
      manifest_dir=$(dirname "$manifest_dir")
    done
    unset manifest_dir
  '';
}
