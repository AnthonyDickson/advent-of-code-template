"""Find the repository, list its templates and load the language weights."""

from __future__ import annotations

import tomllib
from pathlib import Path

CONFIG_FILENAME = "lottery.toml"
TEMPLATE_DIRNAME = "template"
REPO_MARKER = "flake.nix"
DEFAULT_WEIGHT = 1.0


class ConfigError(Exception):
    """Raised when the repository layout or the weights file cannot be used."""


def discover_repo(start: Path | None = None) -> Path:
    """Return the repository root containing ``template/``, walking up from *start*."""
    origin = (start or Path.cwd()).expanduser().resolve()
    for candidate in (origin, *origin.parents):
        if (candidate / TEMPLATE_DIRNAME).is_dir() and (candidate / REPO_MARKER).is_file():
            return candidate
    raise ConfigError(
        f"no Advent of Code repository (template/ plus {REPO_MARKER}) found above {origin}"
    )


def template_languages(repo: Path) -> list[str]:
    """Every language with a template, sorted so draws and displays stay stable."""
    root = repo / TEMPLATE_DIRNAME
    if not root.is_dir():
        raise ConfigError(f"{root} does not exist")
    return sorted(
        entry.name for entry in root.iterdir() if entry.is_dir() and not entry.name.startswith(".")
    )


def load_weights(path: Path) -> dict[str, float]:
    """Read the ``[weights]`` table of *path*, or return nothing when it is absent."""
    if not path.is_file():
        return {}
    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"{path} is not valid TOML: {error}") from error

    table = document.get("weights", {})
    if not isinstance(table, dict):
        raise ConfigError(f"{path}: `weights` must be a table of `language = number` entries")

    weights: dict[str, float] = {}
    for language, value in table.items():
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ConfigError(f"{path}: weight for {language!r} must be a number, got {value!r}")
        if value < 0:
            raise ConfigError(f"{path}: weight for {language!r} cannot be negative")
        weights[str(language)] = float(value)
    return weights


def resolve_weights(repo: Path, config: Path | None = None) -> dict[str, float]:
    """Weights for every template language, defaulting to 1 and rejecting unknown names."""
    languages = template_languages(repo)
    path = config if config is not None else repo / CONFIG_FILENAME
    if config is not None and not path.is_file():
        raise ConfigError(f"weights file not found: {path}")

    weights = load_weights(path)
    unknown = sorted(set(weights) - set(languages))
    if unknown:
        raise ConfigError(f"{path} names languages without a template: {', '.join(unknown)}")
    return {language: weights.get(language, DEFAULT_WEIGHT) for language in languages}
