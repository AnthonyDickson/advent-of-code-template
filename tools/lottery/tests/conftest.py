"""Shared fixtures: a miniature repository and a session to drive the app with."""

from __future__ import annotations

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
def session(repo: Path) -> Session:
    return Session(repo=repo, lottery=Lottery({"python": 1, "rust": 1}), shell="bash")
