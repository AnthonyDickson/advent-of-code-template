pkgs: {
  packages = with pkgs; [
    # Run the Clojure CLI on the same JDK as `java`, the current LTS.
    (clojure.override { jdk = jdk25; })
    clojure-lsp # lsp
    # For linting and formatting Clojure source
    clj-kondo
    cljfmt
    jdk25
  ];
}
