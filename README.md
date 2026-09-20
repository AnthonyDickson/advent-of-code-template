# Advent of Code Template

A template with a nix flake and code snippets in multiple languages for getting started with Advent of Code

## Usage

1. Copy one of the templates, e.g.:
   ```shell
   cp -r template/ocaml day-01/
   ```
1. Enter the nix dev shell for your language, from anywhere inside this repository:
   ```shell
   nix develop .#ocaml -c fish # Replace `ocaml` with your language and `fish` with your shell
   ```

1. Save the problem input as `input.txt` in the folder

1. All templates have the following Make commands:
   ```shell
   make test
   make run
   make benchmark
   ```

> [!NOTE]
> Every dev environment is defined in the single root [`flake.nix`](./flake.nix) and selected by language (`.#ocaml`,
> `.#rust`, ...). `nix develop` on its own starts a minimal shell containing only the shared tooling. If you move a
> copied template out of this repository, install the toolchain listed in that flake yourself.
