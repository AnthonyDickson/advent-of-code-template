# The new Roc compiler only ships as a nightly binary release from
# roc-lang/nightlies; nixpkgs still packages the old alpha4 line. Pin the
# nightly here, keep the `roc:` entry in the templates' `app` headers in step
# with it, and unpack the prebuilt binary, which is statically linked on Linux
# and so needs no patching.
{
  stdenvNoCC,
  fetchurl,
}:
let
  stamp = "2026-09-19-d025939";
  version = "nightly-${stamp}";
  asset =
    {
      x86_64-linux = {
        platform = "linux_x86_64";
        hash = "sha256-yo2KodhzjyeyyPMD398DQ9ij9ny+PYS0AvaHxkIcJfI=";
      };
      aarch64-linux = {
        platform = "linux_arm64";
        hash = "sha256-d5HIgsN7q7Unh16XB0VY3KnqdABQaubNku6R3nUgMiM=";
      };
      x86_64-darwin = {
        platform = "macos_x86_64";
        hash = "sha256-UIJcUibUx1O+UuAaPZTFt8k+LGGmTQ/43zTN4MHkhaY=";
      };
      aarch64-darwin = {
        platform = "macos_apple_silicon";
        hash = "sha256-NmuBgOedQ2fV3wsUYiTq/meP5EIPBUfUXrEfOL8mwNA=";
      };
    }
    .${stdenvNoCC.hostPlatform.system};
in
stdenvNoCC.mkDerivation {
  pname = "roc";
  inherit version;

  src = fetchurl {
    url = "https://github.com/roc-lang/nightlies/releases/download/${version}/roc_nightly-${asset.platform}-${stamp}.tar.gz";
    inherit (asset) hash;
  };

  sourceRoot = "roc_nightly-${asset.platform}-${stamp}";
  installPhase = ''
    install -Dm755 roc $out/bin/roc
  '';
}
