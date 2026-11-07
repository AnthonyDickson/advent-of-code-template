pkgs: {
  packages = with pkgs; [
    scala-cli
    metals # lsp
    scalafmt
    jdk25
  ];

  # Scala CLI and scalafmt take the JDK from here instead of fetching one
  # with coursier, so entering the shell does not download a JVM.
  env.JAVA_HOME = "${pkgs.jdk25}";
}
