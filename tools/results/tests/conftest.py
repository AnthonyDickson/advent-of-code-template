"""Shared fixtures: a miniature git repository and a solution copied out of it."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

# Templates as the repository holds them: source files, a `.gitignore`, and any dotfiles.
TEMPLATES: dict[str, dict[str, str]] = {
    "python": {
        ".gitignore": "**/__pycache__/\n",
        "main.py": "def solve_part_one(data: str) -> int:\n    return 0\n",
        "tests/test_aoc.py": "def test_placeholder() -> None:\n    pass\n",
    },
    "rust": {
        ".gitignore": "target/\n",
        "src/main.rs": "fn solve_part_one(input: &str) -> i64 {\n    0\n}\n",
    },
    "haskell": {
        ".gitignore": "dist-newstyle/\n",
        "aoc.cabal": "name: aoc\n",
        "src/Aoc.hs": "module Aoc where\n",
    },
    "ocaml": {
        ".gitignore": "_build/\n",
        ".ocamlformat": "profile=default\n",
        "dune-project": "(lang dune 3.0)\n",
        "lib/aoc.ml": "let solve = 0\n",
    },
}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A miniature copy of this repository under version control, read through git."""
    if shutil.which("git") is None:
        pytest.skip("git is required to list a template's source files")
    root = tmp_path / "repo"
    write(root / ".gitignore", "**/input.txt\n")
    write(root / "flake.nix", "{ }\n")
    for language, files in TEMPLATES.items():
        for relative, contents in files.items():
            write(root / "template" / language / relative, contents)

    # Working-tree build output that git must not report as a template's source file.
    write(root / "template" / "rust" / "target" / "aoc", "binary")
    write(root / "template" / "python" / "__pycache__" / "main.cpython-314.pyc", "cache")

    subprocess.run(("git", "init", "--quiet"), cwd=root, check=True)
    subprocess.run(("git", "add", "--all"), cwd=root, check=True)
    return root


@pytest.fixture
def solution(repo: Path) -> Path:
    """A Rust solution folder, with its puzzle input, ready to benchmark."""
    destination = repo / "2026-day-05"
    copy_template("rust", destination)
    write(destination / "input.txt", "L68\nR48\n")
    return destination


def copy_template(language: str, destination: Path) -> None:
    """Copy a fixture template's source files into *destination*, the way a bootstrap would."""
    for relative, contents in TEMPLATES[language].items():
        write(destination / relative, contents)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")
