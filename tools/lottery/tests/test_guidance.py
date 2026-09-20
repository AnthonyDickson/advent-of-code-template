import pytest

from aoc_lottery.bootstrap import bootstrap
from aoc_lottery.config import discover_repo, template_languages
from aoc_lottery.guidance import (
    GUIDES,
    bootstrap_steps,
    guide_for,
    next_steps_markdown,
    plain_steps,
    preferred_shell,
)


def test_every_template_has_a_guide():
    assert set(template_languages(discover_repo())) <= set(GUIDES)


def test_unknown_languages_fall_back_to_the_generic_names():
    guide = guide_for("cobol")
    assert (guide.part_one, guide.part_two) == ("solve_part_one", "solve_part_two")


def test_ocaml_guide_mentions_the_line_list():
    assert "string list" in " ".join(guide_for("ocaml").notes)


def test_steps_walk_from_the_copy_to_the_benchmark(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    commands = [step.command for step in bootstrap_steps(plan, repo, "fish")]

    assert commands[0] == "cd 2026-day-05"
    assert "nix develop .#rust -c fish" in commands
    assert commands[-3:] == ["just test", "just run", "just benchmark"]


def test_steps_point_at_the_right_functions_and_file(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    steps = bootstrap_steps(plan, repo, "fish")
    text = " ".join([step.title for step in steps] + [step.detail or "" for step in steps])

    assert "solve_part_one" in text
    assert "solve_part_two" in text
    assert "src/main.rs" in text
    assert "2026 day 5" in text


def test_markdown_renders_every_command(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    markdown = next_steps_markdown(plan, repo, "fish")

    assert "2026-day-05" in markdown
    assert "```shell" in markdown
    assert "nix develop .#rust -c fish" in markdown
    assert "just benchmark" in markdown


def test_plain_steps_are_numbered(repo):
    plan = bootstrap(repo, "rust", 2026, 5)
    lines = plain_steps(plan, repo, "fish")

    assert lines[0] == " 1. Open the new folder"
    assert "    $ cd 2026-day-05" in lines


def test_preferred_shell_falls_back_when_unset(monkeypatch):
    monkeypatch.delenv("SHELL", raising=False)
    assert preferred_shell() == "fish"
    monkeypatch.setenv("SHELL", "/run/current-system/sw/bin/zsh")
    assert preferred_shell() == "zsh"


@pytest.mark.parametrize("language", sorted(GUIDES))
def test_guides_are_filled_in(language):
    guide = GUIDES[language]
    assert guide.entry_point and not guide.entry_point.startswith("/")
    assert guide.part_one and guide.part_two
