pkgs: {
  # `sbcl.withPackages` puts the listed systems, and their transitive
  # dependencies, on ASDF's source registry, so the template needs no
  # Quicklisp: `rove` is the test framework.
  packages = [
    (pkgs.sbcl.withPackages (ps: [ ps.rove ]))
  ];
}
