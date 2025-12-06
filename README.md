# Advent of Code Template

A template with nix flakes and code snippets in multiple languages for getting started with Advent of Code

## Usage

1. Copy one of the templates, e.g.:
   ```shell
   cp -r template/ocaml day-01/
   ```
1. Enter the directory and activate the nix shell:
   ```shell
   cd day-01
   nix develop -c fish # Replace `fish` with your shell, e.g. `zsh`
   ```

1. Save the problem input as `input.txt` in the folder

1. All templates have the following Make commands:
   ```shell
   make test
   make run
   make benchmark
   ```
