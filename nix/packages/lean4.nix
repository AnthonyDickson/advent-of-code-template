# nixpkgs carries Lean 4 on the unversioned `lean4` attribute, but the
# derivation in the pinned nixpkgs fails its install step and its output is in
# no binary cache, so building it is slow as well as broken. Pin the official
# prebuilt toolchain instead, and keep the `lean-toolchain` file in the template
# in step with this version. `lean --server`, which that toolchain provides, is
# the language server, so there is no separate package.
{
  lib,
  stdenvNoCC,
  fetchurl,
  zstd,
  autoPatchelfHook,
}:
let
  version = "4.30.0";
  asset =
    {
      x86_64-linux = {
        platform = "linux";
        hash = "sha256-Ta10FBwsEZyhqmJmVr6DuOFCOK+6lycf178es/CBsxk=";
      };
      aarch64-linux = {
        platform = "linux_aarch64";
        hash = "sha256-yZxvDt1EaVbUdYxZ1Dg+jmQR/2zHGgH5yqvl66RUEh0=";
      };
      aarch64-darwin = {
        platform = "darwin_aarch64";
        hash = "sha256-By3KSjj7wNPO25b+qIbMJDtCTyvRYkdZYgC5qauT8PU=";
      };
    }
    .${stdenvNoCC.hostPlatform.system};
in
stdenvNoCC.mkDerivation {
  pname = "lean4";
  inherit version;

  src = fetchurl {
    url = "https://github.com/leanprover/lean4/releases/download/v${version}/lean-${version}-${asset.platform}.tar.zst";
    inherit (asset) hash;
  };

  # The Linux binaries need their interpreter and libraries patched to point
  # into the store; the macOS ones are not ELF and need nothing.
  nativeBuildInputs = [
    zstd
  ]
  ++ lib.optionals stdenvNoCC.hostPlatform.isLinux [ autoPatchelfHook ];

  installPhase = ''
    mkdir -p $out
    cp -r ./. $out/
  '';
}
