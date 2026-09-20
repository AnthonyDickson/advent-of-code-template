import pytest

from aoc_lottery.config import (
    ConfigError,
    discover_repo,
    load_weights,
    resolve_weights,
    template_languages,
)


def test_discovers_repository_from_a_nested_directory(repo):
    nested = repo / "template" / "rust" / "src"
    assert discover_repo(nested) == repo


def test_missing_repository_is_reported(tmp_path):
    with pytest.raises(ConfigError):
        discover_repo(tmp_path)


def test_languages_are_sorted(repo):
    assert template_languages(repo) == ["python", "rust"]


def test_missing_weights_file_means_no_overrides(repo):
    assert load_weights(repo / "lottery.toml") == {}


def test_weights_are_read_from_the_table(repo):
    config = repo / "lottery.toml"
    config.write_text("[weights]\nrust = 3\npython = 0\n", encoding="utf-8")
    assert load_weights(config) == {"rust": 3.0, "python": 0.0}


def test_unparseable_config_is_reported(repo):
    config = repo / "lottery.toml"
    config.write_text("[weights]\nrust = \n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_weights(config)


@pytest.mark.parametrize("value", ["many", "true", "-1"])
def test_invalid_weight_is_reported(repo, value):
    config = repo / "lottery.toml"
    config.write_text(f"[weights]\nrust = {value}\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_weights(config)


def test_languages_default_to_weight_one(repo):
    assert resolve_weights(repo) == {"python": 1.0, "rust": 1.0}


def test_repo_config_overrides_weights(repo):
    (repo / "lottery.toml").write_text("[weights]\nrust = 5\n", encoding="utf-8")
    assert resolve_weights(repo) == {"python": 1.0, "rust": 5.0}


def test_unknown_language_in_config_is_reported(repo):
    (repo / "lottery.toml").write_text("[weights]\nfortran = 1\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="fortran"):
        resolve_weights(repo)


def test_explicit_config_must_exist(repo):
    with pytest.raises(ConfigError):
        resolve_weights(repo, repo / "missing.toml")


def test_this_repository_covers_every_template():
    """The shipped lottery.toml must keep working as templates are added.

    The weights themselves are the user's own tuning, so only their coverage is checked here.
    """
    root = discover_repo()
    weights = resolve_weights(root)
    assert set(weights) == set(template_languages(root))
