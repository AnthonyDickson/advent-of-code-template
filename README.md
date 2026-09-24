# Advent of Code Template

A template with a nix flake and code snippets in multiple languages for getting started with Advent of Code.

## Usage

1. Copy one of the templates:
   ```shell
   cp -r template/ocaml day-01/
   ```
   The lottery below also copies a template for you.
1. Enter the nix dev shell for your language, from anywhere inside this repository:
   ```shell
   nix develop .#ocaml -c fish # Replace `ocaml` with your language and `fish` with your shell
   ```

1. Save the problem input as `input.txt` in the folder.

1. Run the shared Just recipes (run `just` to list every recipe):
   ```shell
   just test
   just run
   just benchmark
   ```

> [!NOTE]
> Every dev environment is defined in the single root [`flake.nix`](./flake.nix) and selected by language (`.#ocaml`,
> `.#rust`, ...). `nix develop` on its own starts a minimal shell containing only the shared tooling. If you move a
> copied template out of this repository, install the toolchain listed in that flake yourself.

## Picking a language

`just lottery` draws a language from a weighted wheel and shows each language's chance of winning. The draw can be
repeated before a language is accepted:

```shell
just lottery
```

The tool then bootstraps the day: it asks which day it is, copies `template/<lang>` into `<year>-day-<dd>` in the
repository root, and lists what is left to do (dev shell, `input.txt`, the two functions to implement, then `just
test`/`just run`/`just benchmark`).

> [!NOTE]
> Solution folders are written to the repository root so that a private repository created from this one keeps its
> solutions next to `template/`, one `<year>-day-<dd>/` folder per day.

The weights live in [`lottery.toml`](./lottery.toml), so you can make the languages you want to practise more likely and
take the ones you do not with a weight of `0`. `uv` fetches the tool's dependencies on the first run;
[`tools/lottery/README.md`](./tools/lottery/README.md) documents the flags and the TUI-free `--plain` mode.

## Recording results

Once a day is solved, `just record` adds it to `RESULTS.md` in the repository root:

```shell
nix develop .#rust -c just record 2026-day-05
```

Run it inside the drawn language's dev shell; [`tools/results/README.md`](./tools/results/README.md) documents the tool.
