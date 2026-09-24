from pathlib import Path

import pytest
from conftest import TEMPLATES, copy_template, write

from aoc_results import repository


def test_discovers_repository_from_a_nested_directory(repo):
    nested = repo / "template" / "rust" / "src"
    assert repository.discover(nested) == repo


def test_missing_repository_is_reported(tmp_path):
    with pytest.raises(repository.RepositoryError):
        repository.discover(tmp_path)


def test_languages_are_sorted(repo):
    assert repository.languages(repo) == ["haskell", "ocaml", "python", "rust"]


def test_detects_the_template_a_solution_came_from(repo, solution):
    assert repository.detect_language(repo, solution) == "rust"

    python = repo / "2026-day-01"
    copy_template("python", python)
    assert repository.detect_language(repo, python) == "python"


def test_build_output_is_ignored_when_detecting(repo, solution):
    write(solution / "target" / "release" / "aoc", "binary")
    assert repository.detect_language(repo, solution) == "rust"


def test_an_ambiguous_folder_asks_for_the_language(repo):
    twin = repo / "template" / "twin"
    for relative, contents in TEMPLATES["python"].items():
        write(twin / relative, contents)

    folder = repo / "2026-day-01"
    copy_template("python", folder)
    with pytest.raises(repository.RepositoryError, match="--language"):
        repository.detect_language(repo, folder)


def test_an_unrecognised_folder_asks_for_the_language(repo):
    folder = repo / "elsewhere"
    write(folder / "notes.txt", "hello\n")
    with pytest.raises(repository.RepositoryError, match="--language"):
        repository.detect_language(repo, folder)


def test_reads_the_day_from_the_folder_name():
    assert repository.detect_day(Path("/repo/2026-day-05")) == 5
    assert repository.detect_day(Path("2015-day-25")) == 25


def test_an_unreadable_day_is_reported():
    with pytest.raises(repository.RepositoryError, match="--day"):
        repository.detect_day(Path("/repo/day-five"))


def test_detects_templates_whose_dotfiles_are_tracked(repo):
    """A template's `.gitignore` or `.ocamlformat` must not make detection ambiguous."""
    haskell = repo / "2026-day-01"
    copy_template("haskell", haskell)
    assert (haskell / ".gitignore").is_file()
    assert repository.detect_language(repo, haskell) == "haskell"

    ocaml = repo / "2026-day-02"
    copy_template("ocaml", ocaml)
    assert repository.detect_language(repo, ocaml) == "ocaml"


def test_detects_the_checked_in_examples_against_the_real_templates():
    root = repository.discover()
    checked = 0
    for language in repository.languages(root):
        example = root / "examples" / "2015-day-01" / language
        if example.is_dir():
            checked += 1
            assert repository.detect_language(root, example) == language
    assert checked > 0
