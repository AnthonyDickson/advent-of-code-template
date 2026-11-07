pkgs:
let
  # nixpkgs wraps each of these tools around its default `jre` (JDK 21):
  # scala-cli and metals set JAVA_HOME in their wrappers, overriding the
  # shell's, and scalafmt runs that JRE's `java` directly. Rebuild the
  # wrappers on the same JDK as `java`, the current LTS, so the build, its
  # Bloop server, the tests, `just run`, and the editor all use JDK 25
  # without coursier downloading a JVM.
  withJdk = pkg: pkg.override { jre = pkgs.jdk25; };
in
{
  packages = with pkgs; [
    (withJdk scala-cli)
    (withJdk metals) # lsp
    (withJdk scalafmt)
    jdk25
  ];

  # For `java` and any other JVM tool started from the shell.
  env.JAVA_HOME = "${pkgs.jdk25}";
}
