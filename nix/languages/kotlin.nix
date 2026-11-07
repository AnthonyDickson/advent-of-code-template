pkgs:
let
  # JetBrains' official language server, pinned in `../packages/kotlin-lsp`.
  kotlin-lsp = pkgs.callPackage ../packages/kotlin-lsp { };
in
{
  # Gradle fetches the Kotlin compiler named by the `kotlin("jvm")` plugin
  # version in `build.gradle.kts`, so keep that in step with `kotlin` here,
  # which provides `kotlinc` for scripts and the REPL.
  #
  # nixpkgs wraps ktfmt around its default headless JRE (JDK 21) and puts
  # that JRE on kotlinc's PATH, so rebuild both on the same JDK as `java`.
  # Gradle follows JAVA_HOME below, and kotlin-lsp runs on the JetBrains
  # Runtime it bundles.
  packages = with pkgs; [
    gradle_9
    jdk25
    (kotlin.override { jre = jdk25; })
    kotlin-lsp # lsp
    (ktfmt.override { jre_headless = jdk25; })
  ];

  # Gradle and its Kotlin toolchain take the JDK from here instead of
  # provisioning one, so `jvmToolchain(25)` resolves to this JDK.
  env.JAVA_HOME = "${pkgs.jdk25}";

  # A build that has expired refuses to start, and the editor only shows
  # the language server failing, so report the pinned build's age.
  shellHook = ''
    kotlin_lsp_age=$(( ($(date +%s) - ${toString kotlin-lsp.releasedEpoch}) / 86400 ))
    if [ "$kotlin_lsp_age" -ge 25 ]; then
      echo "WARNING: kotlin-lsp ${kotlin-lsp.version} was released ${kotlin-lsp.released}, $kotlin_lsp_age days ago."
      echo "  JetBrains builds expire about a month after release, so it may already refuse to start."
      echo "  Update the pin with \`just update-kotlin-lsp\` from the repository root, then re-enter this shell."
    else
      echo "kotlin-lsp ${kotlin-lsp.version} was released ${kotlin-lsp.released} ($kotlin_lsp_age days ago); builds expire about a"
      echo "  month after release, so update it with \`just update-kotlin-lsp\` before then."
    fi
    unset kotlin_lsp_age
  '';
}
