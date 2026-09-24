# Advent of Code - F#

An F# template for Advent of Code. A solution project in `src/` and an Expecto test project in `tests/`, tied together
by the `Aoc.slnx` solution.

## Getting Started

Refer to the repository's shared [flake.nix](../../flake.nix) for the packages needed to compile this project. If you
have `nix`, run `nix develop .#fsharp` from anywhere inside the repository to enter a dev shell with all of the
dependencies installed.

The dev shell pins the .NET SDK, restores the dotnet tools from `.config/dotnet-tools.json` (`fantomas` and
`fsautocomplete`), and exports `DOTNET_ROOT`.

## Layout

- `src/Aoc.fs` - `solvePartOne`, `solvePartTwo`, the two functions to implement. F# compiles files in the order listed
  in the `.fsproj`, so add new files before `Program.fs`.
- `src/Program.fs` - the CLI, which reads `input.txt` and prints part one, then part two.
- `tests/AocTests.fs` - the Expecto tests. Paste the example from the puzzle statement into the `input` bindings.
- `Directory.Build.props` / `Directory.Packages.props` - the target framework, the shared package versions, and
  `ManagePackageVersionsCentrally`, so a `PackageReference` carries no version.
- `global.json` - pins the SDK feature band the way `nix/devshells.nix` pins every other toolchain.
- `.editorconfig` - the `fantomas` spacing rules.

## Useful Commands

- Run against `input.txt`:

  ```shell
  just run
  ```

- Run the tests:

  ```shell
  just test
  ```

- Build a Release binary (`src/bin/Release/net10.0/Aoc`):

  ```shell
  just build
  ```

- Format with `fantomas`:

  ```shell
  just fmt
  ```

- Benchmark the Release binary:

  ```shell
  just benchmark
  ```

- Check for and upgrade dependencies:

  ```shell
  just outdated
  just update
  ```
