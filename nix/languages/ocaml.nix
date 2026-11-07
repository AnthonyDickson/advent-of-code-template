pkgs:
let
  ocamlPackages = pkgs.ocaml-ng.ocamlPackages_5_5;
in
{
  packages = [
    ocamlPackages.ocaml
    ocamlPackages.utop
    ocamlPackages.dune_3
    ocamlPackages.odoc
    ocamlPackages.ocaml-lsp
    ocamlPackages.ocamlformat
    ocamlPackages.alcotest
  ];
}
