pkgs:
let
  ghcPackages = pkgs.haskell.packages.ghc912;
in
{
  packages = with pkgs; [
    haskell.compiler.ghc912
    ghcPackages.cabal-install
    ghcPackages.haskell-language-server
    # For formatting Haskell source
    ormolu
  ];
}
