import json
import shutil
import subprocess
from pathlib import Path

import pytest

from aoc_results import lines

needs_tokei = pytest.mark.skipif(shutil.which("tokei") is None, reason="tokei is required")


@pytest.mark.parametrize(
    "path",
    [
        "tests/test_aoc.py",
        "test/aoc_test.clj",
        "aoc/aoc_test.go",
        "src/aoc_test.odin",
        "test/Tests.hs",
        "aoc.test.scala",
        "aoc-tests.lisp",
        "specs/aoc_spec.fs",
    ],
)
def test_test_files_are_recognised(path):
    assert lines.is_test_file(Path(path))


@pytest.mark.parametrize(
    "path",
    [
        "main.py",
        "lib/aoc.ex",
        "src/aoc.pl",
        "mix.exs",
        "aoc.py",
        "src/aoc.nu",
    ],
)
def test_application_files_are_not_tests(path):
    assert not lines.is_test_file(Path(path))


def test_count_adds_application_code_and_leaves_tests_and_build_files_out(tmp_path, monkeypatch):
    output = "\n".join(
        [
            _record("Python", tmp_path / "main.py", 11),
            _record("Python", tmp_path / "tests" / "test_aoc.py", 10),
            _record("Rust", tmp_path / "src" / "main.rs", 32),
            _record("Markdown", tmp_path / "README.md", 0),
            _record("Just", tmp_path / "justfile", 15),
            _record("TOML", tmp_path / "Cargo.toml", 9),
        ]
    )
    monkeypatch.setattr(lines, "_run_tokei", lambda directory: output)

    assert lines.count(tmp_path) == 43


def test_a_missing_tokei_is_reported(tmp_path, monkeypatch):
    def missing(*arguments, **keywords):
        raise FileNotFoundError

    monkeypatch.setattr(lines.subprocess, "run", missing)

    with pytest.raises(lines.LinesError, match="tokei"):
        lines._run_tokei(tmp_path)


def test_a_failing_tokei_is_reported(tmp_path, monkeypatch):
    completed = subprocess.CompletedProcess((), 1, stdout="", stderr="boom\n")
    monkeypatch.setattr(lines.subprocess, "run", lambda *arguments, **keywords: completed)

    with pytest.raises(lines.LinesError, match="failed"):
        lines._run_tokei(tmp_path)


def test_unreadable_output_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(lines, "_run_tokei", lambda directory: "not json")

    with pytest.raises(lines.LinesError, match="unexpected tokei output"):
        lines.count(tmp_path)


@needs_tokei
def test_counts_a_real_directory_without_tests(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "main.py").write_text("first = 1\nsecond = 2\n", encoding="utf-8")
    (tmp_path / "tests" / "test_aoc.py").write_text("first = 1\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# A solution\n", encoding="utf-8")
    (tmp_path / "justfile").write_text("default:\n    @just --list\n", encoding="utf-8")

    assert lines.count(tmp_path) == 2


def _record(language: str, path: Path, code: int) -> str:
    """One line of tokei's streaming JSON, as it prints it for a single file."""
    return json.dumps({"language": language, "stats": {"name": str(path), "stats": {"code": code}}})
