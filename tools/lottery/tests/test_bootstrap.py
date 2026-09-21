import shutil

import pytest

from aoc_lottery.bootstrap import (
    BootstrapError,
    bootstrap,
    default_destination,
    display_path,
    validate_day,
    validate_year,
)

# The ignore rules normally come from git; without it the fallback lists are used instead.
needs_git = pytest.mark.skipif(
    shutil.which("git") is None, reason="git is required to read the template's ignore rules"
)


def test_default_destination_is_the_day_folder_in_the_repository_root(repo):
    expected = repo / "2026-day-05"
    assert default_destination(repo, 2026, 5) == expected
    assert (repo / "template").is_dir()  # the solution folders sit next to template/


def test_bootstrap_copies_the_template(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    assert plan.destination == repo / "2026-day-05"
    assert (plan.destination / "src" / "main.rs").is_file()
    assert plan.file_count == 1
    assert plan.copied == ("src/main.rs",)


def test_bootstrap_skips_build_output_and_stale_input(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    assert not (plan.destination / "target").exists()
    assert not (plan.destination / "cli").exists()
    assert not (plan.destination / "input.txt").exists()
    assert plan.copied == ("src/main.rs",)


def test_bootstrap_skips_python_caches(repo):
    plan = bootstrap(repo, "python", 2026, 1)
    assert not (plan.destination / "__pycache__").exists()
    assert plan.copied == ("main.py", "tests/test_aoc.py")


def test_bootstrap_uses_an_explicit_relative_destination(repo):
    plan = bootstrap(repo, "rust", 2026, 5, "scratch/day-five")
    assert plan.destination == repo / "scratch" / "day-five"
    assert (plan.destination / "src" / "main.rs").is_file()


def test_bootstrap_uses_an_explicit_absolute_destination(repo, tmp_path):
    outside = tmp_path / "elsewhere" / "rust"
    plan = bootstrap(repo, "rust", 2026, 5, outside)
    assert plan.destination == outside.resolve()
    assert (outside / "src" / "main.rs").is_file()


def test_bootstrap_refuses_to_overwrite(repo):
    bootstrap(repo, "rust", 2026, 5)
    with pytest.raises(BootstrapError, match="already exists"):
        bootstrap(repo, "rust", 2026, 5)


def test_bootstrap_refuses_to_copy_into_the_template(repo):
    with pytest.raises(BootstrapError, match="inside the template"):
        bootstrap(repo, "rust", 2026, 5, repo / "template" / "rust" / "copy")


def test_bootstrap_rejects_an_unknown_language(repo):
    with pytest.raises(BootstrapError, match="no template"):
        bootstrap(repo, "cobol", 2026, 5)


@pytest.mark.parametrize("day", [0, 26, -3])
def test_bootstrap_rejects_impossible_days(repo, day):
    with pytest.raises(BootstrapError, match="day must be"):
        bootstrap(repo, "rust", 2026, day)


def test_bootstrap_rejects_impossible_years(repo):
    with pytest.raises(BootstrapError, match="year must be"):
        bootstrap(repo, "rust", 2000, 1)


def test_validation_helpers_pass_valid_values():
    assert validate_day(25) == 25
    assert validate_year(2015) == 2015


def test_paths_inside_the_repo_are_shortened(repo):
    inner = repo / "2026-day-05"
    assert display_path(inner, repo) == "2026-day-05"
    assert display_path(repo.parent / "elsewhere", repo) == str(repo.parent / "elsewhere")


@needs_git
def test_bootstrap_skips_whatever_the_template_gitignores(git_repo):
    plan = bootstrap(git_repo, "fsharp", 2026, 5)

    assert plan.copied == (".gitignore", "src/Aoc.fsproj")
    assert not (plan.destination / "src" / "bin").exists()
    assert not (plan.destination / "src" / "obj").exists()
    assert not (plan.destination / "input.txt").exists()


@needs_git
def test_bootstrap_keeps_a_source_directory_named_bin(git_repo):
    """`bin/` is build output for .NET and source for this repository's OCaml template."""
    plan = bootstrap(git_repo, "ocaml", 2026, 1)

    assert plan.copied == (".gitignore", "bin/main.ml")
