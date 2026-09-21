"""Shared fixtures: a miniature repository and a session to drive the app with."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from aoc_lottery.lottery import Lottery
from aoc_lottery.session import Session

TEMPLATES: dict[str, dict[str, str]] = {
    "python": {
        "main.py": "def solve_part_one(data: str) -> int:\n    return 0\n",
        "tests/test_aoc.py": "def test_placeholder() -> None:\n    pass\n",
    },
    "rust": {
        "src/main.rs": "fn solve_part_one(input: &str) -> i64 {\n    0\n}\n",
    },
}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A miniature copy of this repository: ``template/`` next to a ``flake.nix``."""
    (tmp_path / "flake.nix").write_text("{ }\n", encoding="utf-8")
    for language, files in TEMPLATES.items():
        for relative, contents in files.items():
            path = tmp_path / "template" / language / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")

    # Working-tree noise that must never be copied into a solution folder.
    built = tmp_path / "template" / "rust" / "target"
    built.mkdir()
    (built / "cli").write_text("binary", encoding="utf-8")
    (tmp_path / "template" / "rust" / "input.txt").write_text("yesterday", encoding="utf-8")
    (tmp_path / "template" / "rust" / "cli").write_text("binary", encoding="utf-8")
    cached = tmp_path / "template" / "python" / "__pycache__"
    cached.mkdir()
    (cached / "main.cpython-314.pyc").write_text("cache", encoding="utf-8")
    return tmp_path


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """A miniature repository under version control, so the ignore rules come from git."""
    repo = tmp_path / "versioned"
    (repo / "template").mkdir(parents=True)
    (repo / "flake.nix").write_text("{ }\n", encoding="utf-8")
    # A repository-wide rule, the same shape as the `**/input.txt` entry in this repository.
    (repo / ".gitignore").write_text("**/input.txt\n", encoding="utf-8")

    fsharp = repo / "template" / "fsharp"
    write(fsharp / ".gitignore", "bin/\nobj/\n")
    write(fsharp / "src" / "Aoc.fsproj", "<Project />\n")
    write(fsharp / "src" / "bin" / "Debug" / "Aoc.dll", "binary\n")
    write(fsharp / "src" / "obj" / "project.assets.json", "{}\n")
    write(fsharp / "input.txt", "yesterday\n")

    # A template whose `bin/` holds source, as this repository's OCaml template does.
    ocaml = repo / "template" / "ocaml"
    write(ocaml / ".gitignore", "_build/\n")
    write(ocaml / "bin" / "main.ml", "let () = print_int 0\n")

    subprocess.run(("git", "init", "--quiet"), cwd=repo, check=True)
    subprocess.run(("git", "add", "--all"), cwd=repo, check=True)
    return repo


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


@pytest.fixture
def session(repo: Path) -> Session:
    return Session(repo=repo, lottery=Lottery({"python": 1, "rust": 1}), shell="bash")
